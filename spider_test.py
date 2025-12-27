from calendar import c
import httpx
from tqdm import tqdm

# test connection
from tortoise import Tortoise, run_async


async def init():
    await Tortoise.init(
        db_url="mysql://moji:moji@127.0.0.1:13306/moji_test",
        modules={"models": ["moji_spider.models"]},
    )
    await Tortoise.generate_schemas()


run_async(init())

from moji_spider import schemas
from moji_spider import models
from moji_spider.configs import __HEADERS__
from moji_spider.routes import __ROUTES__
from moji_spider.models import (
    ContentResult as ContentResultModel,
    CollectionTarget as CollectionTargetModel,
    ContentTarget as ContentTargetModel,
    SentenceTarget as SentenceTargetModel,
    SharedFolder,
    OfficialFolder,
)

SCHEMA_MODEL_MAP = {
    "ContentTarget": (ContentTargetModel, "content_targets"),
    "CollectionTarget": (CollectionTargetModel, "collection_targets"),
    "SentenceTarget": (SentenceTargetModel, "sentence_targets"),
}


async def test_folder_by_type():
    # test FOLDER_BY_TYPE
    with httpx.Client() as client:
        # test share folder
        response = client.post(
            __ROUTES__.get("FOLDER_BY_TYPE", ""),
            json=getattr(schemas, "FOLDER_BY_TYPE")(perPageCount=3, type=4).model_dump(
                by_alias=True
            ),
            headers=__HEADERS__,
        )
        object = schemas.FetchSharedFoldersWithTypeResponse.model_validate(
            response.json(),
            by_alias=True,
        )
        for item in object.result.result:
            share_folder, is_created = await SharedFolder.get_or_create(
                **item.model_dump(),
            )

        print(object)

        # test official folder
        response = client.post(
            __ROUTES__.get("FOLDER_BY_TYPE", ""),
            json=getattr(schemas, "FOLDER_BY_TYPE")(perPageCount=3, type=1).model_dump(
                by_alias=True
            ),
            headers=__HEADERS__,
        )
        object = schemas.FetchOfficialFoldersResponse.model_validate(
            response.json(),
            by_alias=True,
        )
        for item in object.result.result:
            share_folder, is_created = await OfficialFolder.get_or_create(
                **item.model_dump(),
            )

        print(object)


async def test_folder_by_id():
    # test FOLDER_BY_ID
    # gjdWQCjLGX
    with httpx.Client() as client:
        response = client.post(
            __ROUTES__.get("FOLDER_BY_ID", ""),
            json=getattr(schemas, "FOLDER_BY_ID")(fid="gjdWQCjLGX").model_dump(
                by_alias=True
            ),
            headers=__HEADERS__,
        )
        object = schemas.FetchContentWithRelativesResponse.model_validate(
            response.json(),
            by_alias=True,
        )
        size = object.result.size
        for item in tqdm(object.result.result):
            target_cls, target_col = SCHEMA_MODEL_MAP[item.target.__class__.__name__]
            # target = target_cls(**item.target.model_dump())
            # run_async(target.save())
            target, created = await target_cls.get_or_create(
                **item.target.model_dump(),
            )
            # model = ContentResultModel(**item.model_dump())
            model, created = await ContentResultModel.get_or_create(
                **item.model_dump(exclude={"target"}),
            )
            print(f"model created: {created}")
            await getattr(model, target_col).add(target)
            pass
        # print(object)

    # q6ip0foN4s
    with httpx.Client() as client:
        response = client.post(
            __ROUTES__.get("FOLDER_BY_ID", ""),
            json=getattr(schemas, "FOLDER_BY_ID")(fid="q6ip0foN4s").model_dump(
                by_alias=True
            ),
            headers=__HEADERS__,
        )
        object = schemas.FetchContentWithRelativesResponse.model_validate(
            response.json(),
            by_alias=True,
        )
        for item in tqdm(object.result.result):
            target_cls, target_col = SCHEMA_MODEL_MAP[item.target.__class__.__name__]
            # target = target_cls(**item.target.model_dump())
            # run_async(target.save())
            target, created = await target_cls.get_or_create(
                **item.target.model_dump(),
            )
            # model = ContentResultModel(**item.model_dump())
            model, created = await ContentResultModel.get_or_create(
                **item.model_dump(exclude={"target"}),
            )
            print(f"model created: {created}")
            await getattr(model, target_col).add(target)
            pass
        # print(object)

    # test official folder
    # 0EhuEs7G6E
    with httpx.Client() as client:
        response = client.post(
            __ROUTES__.get("FOLDER_BY_ID", ""),
            json=getattr(schemas, "FOLDER_BY_ID")(fid="0EhuEs7G6E").model_dump(
                by_alias=True
            ),
            headers=__HEADERS__,
        )
        object = schemas.FetchContentWithRelativesResponse.model_validate(
            response.json(),
            by_alias=True,
        )
        for item in tqdm(object.result.result):
            target_cls, target_col = SCHEMA_MODEL_MAP[item.target.__class__.__name__]
            # target = target_cls(**item.target.model_dump())
            # run_async(target.save())
            target, created = await target_cls.get_or_create(
                **item.target.model_dump(),
            )
            # model = ContentResultModel(**item.model_dump())
            model, created = await ContentResultModel.get_or_create(
                **item.model_dump(exclude={"target"}),
            )
            print(f"model created: {created}")
            await getattr(model, target_col).add(target)
            pass

        print(object)


if __name__ == "__main__":

    # # test ME
    # with httpx.Client() as client:
    #     response = client.post(
    #         __ROUTES__.get("ME", ""),
    #         json=getattr(schemas, "ME")().model_dump(by_alias=True),
    #         headers=__HEADERS__,
    #     )
    #     print(response.json())

    # from pydantic import BaseModel
    # from datetime import datetime

    # class TimeTest(BaseModel):
    #     t: datetime

    # data = {
    #     "t": "2020-10-27T06:18:23.330Z",
    # }

    # tt = TimeTest.model_validate(data)
    # print(tt)

    # run_async(test_folder_by_type())
    # run_async(test_folder_by_id())

    exit(0)
