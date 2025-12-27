from tortoise import Tortoise, run_async

from .configs import __SQL_ADDRESS__


async def init():
    await Tortoise.init(
        db_url=__SQL_ADDRESS__,
        modules={"models": ["moji_spider.models"]},
    )
    await Tortoise.generate_schemas()


run_async(init())
