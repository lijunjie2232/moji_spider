import logging

from loguru import logger
from tortoise import Tortoise, run_async

from .configs import __SQL_ADDRESS__


async def init():
    logger.info(f"Initializing database connection to: {__SQL_ADDRESS__}")
    try:
        await Tortoise.init(
            db_url=__SQL_ADDRESS__,
            modules={"models": ["moji_spider.models"]},
        )
        logger.success("Tortoise ORM initialized successfully")

        logger.info("Generating database schemas...")
        await Tortoise.generate_schemas()
        logger.success("Database schemas generated successfully")

    except Exception as e:
        logger.error(f"Error during database initialization: {e}")
        raise


logger.info("Starting database initialization...")
run_async(init())
logger.info("Database initialization completed")
