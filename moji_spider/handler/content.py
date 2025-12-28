import asyncio
from asyncio import Queue

import httpx
from loguru import logger

from .. import models, schemas
from ..configs import __HEADERS__, __HTTPX_CONFIG__
from ..routes import __ROUTES__

SCHEMA_MODEL_MAP = {
    "IgnoredTarget": (None, None),
    "ContentTarget": (models.ContentTarget, models.ContentResultContentTarget),
    "CollectionTarget": (models.CollectionTarget, models.ContentResultCollectionTarget),
    "SentenceTarget": (models.SentenceTarget, models.ContentResultSentenceTarget),
}

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
ITEM_QUEUE = Queue()


async def item_handler(item):
    logger.debug(f"Handling item: {item}")
    try:
        target_cls, junction_cls = SCHEMA_MODEL_MAP[item.target.__class__.__name__]
        if target_cls == None:
            logger.warning(f"Skipping item: {item}")
            return
        target, created = await target_cls.get_or_create(
            **item.target.model_dump(),
        )
        logger.debug(f"Created/Retrieved target: {target}, created: {created}")

        model, created = await getattr(models, "ContentResult").get_or_create(
            **item.model_dump(exclude={"target"}),
        )
        logger.debug(
            f"Created/Retrieved content result model: {model}, created: {created}"
        )

        junction, created = await junction_cls.get_or_create(
            content_result=model,
            target=target,
        )
        logger.debug(f"Created/Retrieved junction: {junction}, created: {created}")

        if isinstance(item.target, schemas.CollectionTarget):
            await TASK_QUEUE.put(item)
            logger.debug(
                f"Added collection target to task queue: {item.target.object_id}"
            )

        logger.success(f"Successfully handled item: {item.target.object_id}")
    except Exception as e:
        logger.error(f"Error handling item {item}: {e}")
        raise


async def pre_process_response(response: dict):
    for i in ["1", "411", "1000"]:
        if i in response["result"]:
            response["result"].pop(i)
    return response


async def fetch_item_by_id(id: str):
    logger.info(f"Fetching item by ID: {id}")

    async def _fetch(
        fetch_client: httpx.AsyncClient,
        fetch_id: str,
        fetch_page_index: int,
    ):
        logger.debug(f"Fetching data for ID: {fetch_id}, page: {fetch_page_index}")
        try:
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
            response_json = response.json()
            response_json = await pre_process_response(response_json)

            object = getattr(
                schemas, "FetchContentWithRelativesResponse"
            ).model_validate(
                response_json,
                by_alias=True,
            )
            return object
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
            await add_item_to_queue(object.result.result)
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
        logger.error(f"Error in fetch_item_by_id for {id}: {e}")
        raise


async def add_item_to_queue(items: list):
    logger.debug(f"Adding {len(items)} items to queue")
    try:
        for item in items:
            if item.target == None:
                logger.debug(f"the share of {item.title} has been cancelled, skip it")
                continue
            else:
                await ITEM_QUEUE.put(item)
        logger.success(f"Successfully added {len(items)} items to queue")
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


_RUNNING = True
_TASK_COMPLETE = False
_ITEM_COMPLETE = True


async def TASK_EXECUTOR():
    logger.info("TASK_EXECUTOR started")
    try:
        while _RUNNING:
            if not TASK_QUEUE.empty():
                _TASK_COMPLETE = False
                logger.debug("Getting task from TASK queue")
                item = await TASK_QUEUE.get()
                logger.info(f"Processing task: {item}")
                await fetch_item_by_id(item.object_id)
                await asyncio.sleep(1)
            else:
                _TASK_COMPLETE = True
                await asyncio.sleep(1)
        logger.info("TASK_EXECUTOR finished")
    except Exception as e:
        logger.error(f"Error in TASK_EXECUTOR: {e}")
        raise


async def ITEM_EXECUTOR():
    logger.info("ITEM_EXECUTOR started")
    try:
        while _RUNNING:
            if not ITEM_QUEUE.empty():
                _ITEM_COMPLETE = False
                logger.debug("Getting item from ITEM queue")
                item = await ITEM_QUEUE.get()
                logger.debug(f"Processing item: {item}")
                await item_handler(item)
            else:
                _ITEM_COMPLETE = True
                await asyncio.sleep(1)
        logger.info("ITEM_EXECUTOR finished")
    except Exception as e:
        logger.error(f"Error in ITEM_EXECUTOR: {e}")
        raise


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
        # await query_shared_folders()
        await query_official_folders()

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
