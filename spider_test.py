import httpx

from moji_spider import schemas
from moji_spider.configs import __HEADERS__
from moji_spider.routes import __ROUTES__


def test_folder_by_type():
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
        print(object)


def test_folder_by_id():
    # # test FOLDER_BY_ID
    # # gjdWQCjLGX
    # with httpx.Client() as client:
    #     response = client.post(
    #         __ROUTES__.get("FOLDER_BY_ID", ""),
    #         json=getattr(schemas, "FOLDER_BY_ID")(fid="gjdWQCjLGX").model_dump(
    #             by_alias=True
    #         ),
    #         headers=__HEADERS__,
    #     )
    #     object = schemas.FetchContentWithRelativesResponse.model_validate(
    #         response.json(),
    #         by_alias=True,
    #     )
    #     print(object)

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
        print(object)

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
        for item in object.result.result:
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

    # test_folder_by_type()
    # test_folder_by_id()

    exit(0)
