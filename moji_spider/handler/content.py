import asyncio
from asyncio import Queue
from msilib import schema

import httpx
from loguru import logger

from .. import models, schemas
from ..configs import __HEADERS__
from ..routes import __ROUTES__

SCHEMA_MODEL_MAP = {
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
    target_cls, junction_cls = SCHEMA_MODEL_MAP[item.target.__class__.__name__]
    target, created = await target_cls.get_or_create(
        **item.target.model_dump(),
    )
    model, created = await getattr(models, "ContentResultModel").get_or_create(
        **item.model_dump(exclude={"target"}),
    )
    junction, created = await junction_cls.get_or_create(
        content_result=model,
        target=target,
    )
    if isinstance(item.target, schemas.CollectionTarget):
        await TASK_QUEUE.put(item)


async def fetch_item_by_id(id: str):
    async def _fetch(
        fetch_client: httpx.AsyncClient,
        fetch_id: str,
        fetch_page_index: int,
    ):

        response = await fetch_client.post(
            __ROUTES__.get("FOLDER_BY_ID", ""),
            json=getattr(schemas, "FOLDER_BY_ID")(
                fid=fetch_id,
                count=count,
                page_index=fetch_page_index,
            ).model_dump(by_alias=True),
            headers=__HEADERS__,
        )
        object = getattr(schemas, "FetchContentWithRelativesResponse").model_validate(
            response.json(),
            by_alias=True,
        )
        return object

    async def _handle(
        client,
        id,
        page_index,
    ):
        object = await _fetch(
            client,
            id,
            page_index,
        )
        await add_item_to_queue(object.result.result)
        return object

    # test FOLDER_BY_ID
    # gjdWQCjLGX
    count = 3000
    page_index = 1  # page start from 1
    async with httpx.AsyncClient() as client:
        result_obj = await _handle(
            client,
            id,
            page_index,
        )
        # total_size = result_obj.result.size
        total_page = result_obj.result.totalPage
        count = len(result_obj.result.result)
        page_index += 1
        if page_index > total_page:
            return
        for idx in range(page_index, total_page + 1):
            result_obj = await _handle(
                client,
                id,
                idx,
            )


async def add_item_to_queue(items: list):
    for item in items:
        await ITEM_QUEUE.put(item)


async def query_shared_folders():
    for folder in await models.SharedFolder.all():
        await TASK_QUEUE.put(folder)


async def query_official_folders():
    for folder in await models.OfficialFolder.all():
        await TASK_QUEUE.put(folder)


_RUNNING = True
_task_complete = False
_item_complete = True


async def TASK_EXECUTOR():
    while _RUNNING:
        while not TASK_QUEUE.empty():
            _task_complete = False
            logger.debug("GETTING TASK FROM TASK QUEUE")
            item = await ITEM_QUEUE.get()
            logger.debug(f"GET TASK: {item}")
            await fetch_item_by_id(item.object_id)
        _task_complete = True
        await asyncio.sleep(1)


async def ITEM_EXECUTOR():
    while _RUNNING:
        while not ITEM_QUEUE.empty():
            _item_complete = False
            logger.debug("GETTING ITEM FROM ITEM QUEUE")
            item = await ITEM_QUEUE.get()
            logger.debug(f"GET ITEM: {item}")
            await item_handler(item)
        _item_complete = True
        await asyncio.sleep(1)


async def EXECUTOR():
    await query_shared_folders()
    await query_official_folders()
    while not _item_complete or not _task_complete:
        await asyncio.sleep(5)
        while ITEM_QUEUE.empty() and TASK_QUEUE.empty():
            await asyncio.sleep(5)
            while ITEM_QUEUE.empty() and TASK_QUEUE.empty():
                await asyncio.sleep(5)
                while not _item_complete or not _task_complete:
                    await asyncio.sleep(5)
