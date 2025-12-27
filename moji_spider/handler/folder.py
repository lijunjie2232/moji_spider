# main.py
import httpx
from loguru import logger

from .. import schemas
from ..configs import __HEADERS__
from ..models import OfficialFolder, SharedFolder
from ..routes import __ROUTES__


async def share_folder_to_db():
    """
    get shared folder (type: [4|6])
    """
    with httpx.Client() as client:
        for folder_type in [4, 6]:
            response = client.post(
                __ROUTES__.get("FOLDER_BY_TYPE", ""),
                json=getattr(schemas, "FOLDER_BY_TYPE")(type=4).model_dump(
                    by_alias=True
                ),
                headers=__HEADERS__,
            )
            object = getattr(
                schemas, "FetchSharedFoldersWithTypeResponse"
            ).model_validate(
                response.json(),
                by_alias=True,
            )
            logger.debug(
                f"get shared folders with type {folder_type}, size: {len(object.result.result)}"
            )
            for item in object.result.result:
                folder, is_created = await SharedFolder.get_or_create(
                    **item.model_dump(),
                )
                logger.debug(
                    f"shared folder: {folder.title} - {folder.id}"
                    + f" {'created' if is_created else 'skipped'}"
                )


async def offical_folder_to_db():
    with httpx.Client() as client:
        response = client.post(
            __ROUTES__.get("FOLDER_BY_TYPE", ""),
            json=getattr(schemas, "FOLDER_BY_TYPE")(type=1).model_dump(by_alias=True),
            headers=__HEADERS__,
        )
        object = getattr(schemas, "FetchOfficialFoldersResponse").model_validate(
            response.json(),
            by_alias=True,
        )
        logger.debug(f"get offical folders size: {len(object.result.result)}")

        for item in object.result.result:
            folder, is_created = await OfficialFolder.get_or_create(
                **item.model_dump(),
            )
            logger.debug(
                f"offical folder: {folder.title} - {folder.id}"
                + f" {'created' if is_created else 'skipped'}"
            )
