# models.py
from tortoise import fields, models
from tortoise.fields import (
    DatetimeField,
    IntField,
    CharField,
    BooleanField,
    TextField,
    ForeignKeyField,
)


if __name__ == "__main__":
    # test connection
    from configs import __TORTOISE_ORM__
    from tortoise import Tortoise, run_async

    async def init():
        await Tortoise.init(
            db_url="mysql://moji:moji@localhost:13306/moji_test",
            modules={"models": ["models"]},
        )
        await Tortoise.generate_schemas()

    run_async(init())
