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

parrel_num = 7


async def main():
    """
    main entry
    """
    # Run the async function
    task = asyncio.create_task(EXECUTOR())
    task_t = [asyncio.create_task(TASK_EXECUTOR()) for _ in range(parrel_num)]
    task_i = [asyncio.create_task(ITEM_EXECUTOR()) for _ in range(parrel_num)]
    await asyncio.gather(task, *task_t, *task_i)
