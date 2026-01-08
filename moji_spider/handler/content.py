import asyncio
from asyncio import Queue
import traceback
import httpx
from loguru import logger
from tortoise.transactions import in_transaction

from .. import models, schemas
from ..configs import __HEADERS__, __HTTPX_CONFIG__
from ..routes import __ROUTES__

# SCHEMA_MODEL_MAP = {
#     "IgnoredTarget": (models.IgnoredTarget, models.ContentResultIgnoredTarget),
#     "ContentTarget": (models.ContentTarget, models.ContentResultContentTarget),
#     "CollectionTarget": (models.CollectionTarget, models.ContentResultCollectionTarget),
#     "SentenceTarget": (models.SentenceTarget, models.ContentResultSentenceTarget),
#     "TranslateTarget": (models.TranslateTarget, models.ContentResultTranslationTarget),
# }

SCHEMA_MODEL_MAP = {
    "IgnoredTarget": (
        models.IgnoredTarget,
        models.ContentResultIgnoredTarget,
        "ignored_targets",
    ),
    "ContentTarget": (
        models.ContentTarget,
        models.ContentResultContentTarget,
        "content_targets",
    ),
    "CollectionTarget": (
        models.CollectionTarget,
        models.ContentResultCollectionTarget,
        "collection_targets",
    ),
    "SentenceTarget": (
        models.SentenceTarget,
        models.ContentResultSentenceTarget,
        "sentence_targets",
    ),
    "TranslateTarget": (
        models.TranslateTarget,
        models.ContentResultTranslationTarget,
        "translation_targets",
    ),
}

data = {}

"""
if t == 1000:
    values["target"] = CollectionTarget.model_validate(data, by_alias=True)
elif t in [102, 104]:
    values["target"] = ContentTarget.model_validate(data, by_alias=True)
elif t == 103:
    values["target"] = SentenceTarget.model_validate(data, by_alias=True)
elif t == 431:
    values["target"] = IgnoredTarget.model_validate(data, by_alias=True)
else:
    raise ValueError("Invalid targetType")
"""

TARGET_TYPE_MAP = {
    1000: schemas.CollectionTarget,
    102: schemas.ContentTarget,
    103: schemas.SentenceTarget,
    104: schemas.ContentTarget,
}

TASK_QUEUE = Queue()
ITEM_QUEUE = Queue(maxsize=200)

import asyncio
from collections import defaultdict

from loguru import logger
from tortoise.exceptions import DoesNotExist, IntegrityError

# Global lock dictionary to prevent concurrent operations on same object
_target_locks = defaultdict(asyncio.Lock)


# Updated item_handler function using the safe_get_or_create
async def item_handler(fetch_result):
    async with in_transaction():
        logger.debug(f"Handling fetch result: {fetch_result}")
        fetch_result_model, created = await models.FetchResult.get_or_create(
            {k: v for k, v in fetch_result.model_dump(exclude={"result"}).items()},
            fid=fetch_result.fid,
        )

    for item in fetch_result.result:
        async with in_transaction():
            logger.debug(f"Handling item: {item}")
            try:
                model, created = await models.ContentResult.get_or_create(
                    {
                        k: v
                        for k, v in item.model_dump(exclude={"target"}).items()
                        if hasattr(models.ContentResult(), k)
                    },
                    id=item.id,
                )
                logger.debug(
                    f"Created/Retrieved content result model: {model}, created: {created}"
                )

                f_c_junc, created = await models.FetchResultContentResult.get_or_create(
                    fetch_result=fetch_result_model, content_result=model
                )

                target_cls, junction_cls, field_name = SCHEMA_MODEL_MAP[
                    item.target.__class__.__name__
                ]
                id_filter = {}

                if isinstance(item.target, schemas.IgnoredTarget):
                    # if item.target.data == None:
                    logger.warning(f"Skipping item: {item}")
                    model.is_cancelled = True
                    await model.save()
                    continue
                else:
                    id_filter["object_id"] = item.target.object_id

                target, created = await target_cls.get_or_create(
                    {
                        k: v
                        for k, v in item.target.model_dump().items()
                        if hasattr(target_cls(), k)
                    },
                    **id_filter,
                )
                logger.debug(
                    f"Created/Retrieved target model: {target}, created: {created}"
                )

                junction, created = await junction_cls.get_or_create(
                    content_result=model, target=target
                )
                logger.debug(
                    f"Created/Retrieved junction: {junction}, created: {created}"
                )

                if created and isinstance(item.target, schemas.CollectionTarget):
                    await TASK_QUEUE.put(item)
                    logger.debug(
                        f"Added collection target to task queue: {item.target.object_id}"
                    )

                logger.success(
                    f"Successfully handled item: {getattr(item.target, 'object_id', item.object_id)}"
                )
            except Exception as e:
                traceback.print_exc()
                logger.error(f"Error handling item {item}: {e}")
                raise


async def pre_process_response(response: dict):
    for i in ["1", "411", "1000"]:
        if i in response["result"]:
            response["result"].pop(i)
    return response


async def fetch_item(id):
    return await models.ContentResult.get_or_none(object_id=id)


async def fetch_item_by_id(id: str):
    logger.info(f"Fetching item by ID: {id}")

    item = await fetch_item(id)

    if item:
        logger.info(f"Item found: {item}")
        return

    async def _fetch(
        fetch_client: httpx.AsyncClient,
        fetch_id: str,
        fetch_page_index: int,
        retry=3,
    ):
        logger.debug(f"Fetching data for ID: {fetch_id}, page: {fetch_page_index}")
        try:
            while retry:
                response = await fetch_client.post(
                    __ROUTES__.get("FOLDER_BY_ID", ""),
                    json=getattr(schemas, "FOLDER_BY_ID")(
                        fid=fetch_id,
                        count=count,
                        page_index=fetch_page_index,
                    ).model_dump(by_alias=True),
                    headers=__HEADERS__,
                )
                logger.debug(f"Response status for {fetch_id}: {response.status_code}")

                if response.status_code != 200:
                    retry -= 1
                    await asyncio.sleep(1)
                    continue
                response_json = response.json()
                # response_json = await pre_process_response(response_json)

                object = getattr(
                    schemas, "FetchContentWithRelativesResponse"
                ).model_validate(
                    response_json,
                    by_alias=True,
                )
                return object
            logger.error(f"Failed to fetch data for {fetch_id}")
            raise Exception(
                f"Failed to fetch data for ID {fetch_id} for response code {response.status_code}"
            )
        except httpx.HTTPStatusError as e:
            logger.error(f"HTTP error when fetching data for {fetch_id}: {e}")
            raise
        except Exception as e:
            logger.error(f"Error when fetching data for {fetch_id}: {e}")
            raise

    async def _handle(
        client,
        id,
        page_index,
    ):
        logger.debug(f"Handling fetch for ID: {id}, page: {page_index}")
        try:
            object = await _fetch(
                client,
                id,
                page_index,
            )
            await add_item_to_queue(object.result)
            logger.debug(f"Added {len(object.result.result)} items to queue from {id}")
            return object
        except Exception as e:
            logger.error(f"Error handling fetch for {id}: {e}")
            raise

    # test FOLDER_BY_ID
    # gjdWQCjLGX
    count = 3000
    page_index = 1  # page start from 1
    try:
        async with httpx.AsyncClient(**__HTTPX_CONFIG__) as client:
            logger.debug(f"Starting fetch for ID: {id}")
            result_obj = await _handle(
                client,
                id,
                page_index,
            )
            logger.info(f"Initial fetch completed for ID: {id}")

            # total_size = result_obj.result.size
            total_page = result_obj.result.totalPage
            count = len(result_obj.result.result)
            logger.info(f"Total pages for {id}: {total_page}, count: {count}")

            page_index += 1
            if page_index > total_page:
                logger.info(f"All pages processed for ID: {id}")
                return

            for idx in range(page_index, total_page + 1):
                logger.info(f"Processing page {idx}/{total_page} for ID: {id}")
                result_obj = await _handle(
                    client,
                    id,
                    idx,
                )
                logger.debug(f"Completed page {idx} for ID: {id}")

            logger.success(f"Successfully fetched all pages for ID: {id}")
    except Exception as e:
        import traceback

        traceback.print_exc()
        logger.error(f"Error in fetch_item_by_id for {id}: {e}")
        raise e


async def add_item_to_queue(fetch_result):
    logger.debug(f"Adding {len(fetch_result.result)} items to queue")
    try:
        await ITEM_QUEUE.put(fetch_result)
        logger.success(
            f"Successfully added fetch item {fetch_result.fid} to queue with {len(fetch_result.result)} items"
        )
    except Exception as e:
        logger.error(f"Error adding items to queue: {e}")
        raise


async def query_shared_folders():
    logger.info("Querying shared folders")
    try:
        folders = await models.SharedFolder.all()
        logger.debug(f"Found {len(folders)} shared folders")
        for folder in folders:
            await TASK_QUEUE.put(folder)
            logger.debug(f"Added shared folder to task queue: {folder.object_id}")
        logger.success(
            f"Successfully added {len(folders)} shared folders to task queue"
        )
    except Exception as e:
        logger.error(f"Error querying shared folders: {e}")
        raise


async def query_official_folders():
    logger.info("Querying official folders")
    try:
        folders = await models.OfficialFolder.all()
        logger.debug(f"Found {len(folders)} official folders")
        for folder in folders:
            await TASK_QUEUE.put(folder)
            logger.debug(f"Added official folder to task queue: {folder.object_id}")
        logger.success(
            f"Successfully added {len(folders)} official folders to task queue"
        )
    except Exception as e:
        logger.error(f"Error querying official folders: {e}")
        raise


async def query_collection_targets():
    logger.info("Querying collection targets")
    try:
        collection_targets = await models.CollectionTarget.all()
        logger.debug(f"Found {len(collection_targets)} collection targets")
        for collection_target in collection_targets:
            await TASK_QUEUE.put(collection_target)
            logger.debug(
                f"Added collection target to task queue: {collection_target.object_id}"
            )
        logger.success(
            f"Successfully added {len(collection_targets)} collection targets to task queue"
        )
    except Exception as e:
        logger.error(f"Error querying collection targets: {e}")
        raise


_RUNNING = True
_TASK_COMPLETE = False
_ITEM_COMPLETE = True


async def TASK_EXECUTOR(id):
    exec_id = id
    await asyncio.sleep(int(id))
    logger.info("TASK_EXECUTOR started")
    while _RUNNING:
        item = None
        try:
            if not TASK_QUEUE.empty():
                global _TASK_COMPLETE
                _TASK_COMPLETE = False
                logger.debug(
                    f"Getting task from TASK queue, rest: {TASK_QUEUE.qsize()}"
                )
                item = await TASK_QUEUE.get()
                logger.info(f"Processing task: {item}")
                await fetch_item_by_id(getattr(item, "target_id", item.object_id))
            else:
                await asyncio.sleep(1)
        except Exception as e:
            traceback.print_exc()
            print(item)
            logger.error(
                f"Feth item {getattr(item, 'target_id', getattr(item,'object_id'))} error: {e}"
            )
            raise (e)
            logger.error(f"Error in TASK_EXECUTOR: {e}")
            if item != None:
                await TASK_QUEUE.put(item)
        finally:
            await asyncio.sleep(0.5)
    logger.info("TASK_EXECUTOR finished")
    _TASK_COMPLETE = True


async def ITEM_EXECUTOR(id=0):
    exec_id = id
    await asyncio.sleep(int(id))
    logger.info("ITEM_EXECUTOR started")

    while _RUNNING:
        try:
            if not ITEM_QUEUE.empty():
                global _ITEM_COMPLETE
                _ITEM_COMPLETE = False
                logger.debug(
                    f"Getting item from ITEM queue, rest: {ITEM_QUEUE.qsize()}"
                )
                item = await ITEM_QUEUE.get()
                logger.debug(f"Processing item: {item}")
                await item_handler(item)
                # __ITEM_EXCUTOR_POOL__.apply_async(
                #     asyncio.run, args=(item_handler, item)
                # )
            else:
                await asyncio.sleep(2)
        except Exception as e:
            logger.error(f"Error in ITEM_EXECUTOR: {e}")
            raise e
        # finally:
        # await asyncio.sleep()
    logger.info("ITEM_EXECUTOR finished")
    _ITEM_COMPLETE = True


async def EXECUTOR():
    async def _wait(sec=5):
        logger.debug(f"ITEM QUEUE SIZE: {ITEM_QUEUE.qsize()}")
        logger.debug(f"TASK QUEUE SIZE: {TASK_QUEUE.qsize()}")
        logger.debug(
            f"Still waiting - Item complete: {_ITEM_COMPLETE}, Task complete: {_TASK_COMPLETE}"
        )
        await asyncio.sleep(5)

    logger.info("EXECUTOR started")
    try:
        await query_official_folders()
        await query_shared_folders()
        # await query_collection_targets()

        while not _ITEM_COMPLETE or not _TASK_COMPLETE:
            await _wait()
            while ITEM_QUEUE.empty() and TASK_QUEUE.empty():
                await _wait()
                while ITEM_QUEUE.empty() and TASK_QUEUE.empty():
                    await _wait()
                    while not _ITEM_COMPLETE or not _TASK_COMPLETE:
                        await _wait()
        _RUNNING = False
        logger.success("EXECUTOR finished - all tasks completed")
    except Exception as e:
        logger.error(f"Error in EXECUTOR: {e}")
        raise
