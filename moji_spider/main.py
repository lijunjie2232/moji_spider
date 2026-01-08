import asyncio
from threading import Thread, main_thread

from loguru import logger

from .handler import (
    EXECUTOR,
    ITEM_EXECUTOR,
    TASK_EXECUTOR,
    content,
    offical_folder_to_db,
    share_folder_to_db,
)

__LOOP__ = asyncio.get_event_loop()

parrel_num = 10


async def main():
    """
    main entry
    """
    # await offical_folder_to_db()
    # await share_folder_to_db()

    # exit(0)

    # Run the async function
    task = asyncio.create_task(EXECUTOR())
    task_t = [asyncio.create_task(TASK_EXECUTOR(id)) for id in range(parrel_num)]
    # task_i = [asyncio.create_task(ITEM_EXECUTOR(id)) for id in range(parrel_num)]
    task_i = [asyncio.create_task(ITEM_EXECUTOR())]
    await asyncio.gather(task, *task_t, *task_i)
