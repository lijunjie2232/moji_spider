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


async def test_folder_by_id(id: str):
    # test FOLDER_BY_ID
    # gjdWQCjLGX
    with httpx.Client() as client:
        response = client.post(
            __ROUTES__.get("FOLDER_BY_ID", ""),
            json=getattr(schemas, "FOLDER_BY_ID")(fid=id).model_dump(by_alias=True),
            headers=__HEADERS__,
        )
        object = getattr(schemas, "FetchContentWithRelativesResponse").model_validate(
            response.json(),
            by_alias=True,
        )
        size = object.result.size
        for item in object.result.result:
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
            pass
