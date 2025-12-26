# schemas.py
from datetime import datetime
from typing import Any, Dict, List, Optional, Union

from pydantic import BaseModel, Field, model_validator

from .configs import __CONFIG__


class ME(BaseModel):
    # __data__ = {
    #     "_method": "GET",
    #     "_ApplicationId": "E62VyFVLMiW7kvbtVq3p",
    #     "_ClientVersion": "js4.3.1",
    #     "_InstallationId": "7597f959-0937-4c47-b447-6153a0048e13",
    #     "_SessionToken": "69475e7dd7150c276816bc30",
    # }
    method: str = Field("GET", alias="_method")
    ApplicationId: str = Field(
        __CONFIG__.get("_ApplicationId", ""), alias="_ApplicationId"
    )
    ClientVersion: str = Field(
        __CONFIG__.get("_ClientVersion", ""), alias="_ClientVersion"
    )
    InstallationId: str = Field(
        __CONFIG__.get("_InstallationId", ""), alias="_InstallationId"
    )

    SessionToken: str = Field(
        __CONFIG__.get("_SessionToken", ""), alias="_SessionToken"
    )


class FOLDER_BY_TYPE(BaseModel):
    # __data__ = {
    #     "type": 1,
    #     "pageIndex": 1,
    #     "perPageCount": 3000,
    #     "_SessionToken": "69475e7dd7150c276816bc30",
    #     "_ClientVersion": "js4.3.1",
    #     "_ApplicationId": "E62VyFVLMiW7kvbtVq3p",
    #     "g_os": "PCWeb",
    #     "g_ver": "4.13.3",
    #     "_InstallationId": "7597f959-0937-4c47-b447-6153a0048e13",
    # }
    type: int = Field(1, alias="type")
    page_index: int = Field(1, alias="pageIndex")
    per_page_count: int = Field(3000, alias="perPageCount")
    SessionToken: str = Field(
        __CONFIG__.get("_SessionToken", ""), alias="_SessionToken"
    )
    ClientVersion: str = Field(
        __CONFIG__.get("_ClientVersion", ""), alias="_ClientVersion"
    )
    ApplicationId: str = Field(
        __CONFIG__.get("_ApplicationId", ""), alias="_ApplicationId"
    )
    g_os: str = Field(__CONFIG__.get("g_os", ""), alias="g_os")
    g_ver: str = Field(__CONFIG__.get("g_ver", ""), alias="g_ver")
    InstallationId: str = Field(
        __CONFIG__.get("_InstallationId", ""), alias="_InstallationId"
    )


class FOLDER_BY_ID(BaseModel):
    # __data__ = {
    #     "fid": "0EhuEs7G6E",
    #     "count": 3000,
    #     "sortType": 0,
    #     "pageIndex": 1,
    #     "_SessionToken": "69475e7dd7150c276816bc30",
    #     "_ClientVersion": "js4.3.1",
    #     "_ApplicationId": "E62VyFVLMiW7kvbtVq3p",
    #     "g_os": "PCWeb",
    #     "g_ver": "4.13.3",
    #     "_InstallationId": "7597f959-0937-4c47-b447-6153a0048e13",
    # }

    fid: str = Field(..., alias="fid")
    count: int = Field(3000, alias="count")
    sort_type: int = Field(0, alias="sortType")
    page_index: int = Field(1, alias="pageIndex")
    SessionToken: str = Field(
        __CONFIG__.get("_SessionToken", ""), alias="_SessionToken"
    )
    ClientVersion: str = Field(
        __CONFIG__.get("_ClientVersion", ""), alias="_ClientVersion"
    )
    ApplicationId: str = Field(
        __CONFIG__.get("_ApplicationId", ""), alias="_ApplicationId"
    )
    g_os: str = Field(__CONFIG__.get("g_os", ""), alias="g_os")
    g_ver: str = Field(__CONFIG__.get("g_ver", ""), alias="g_ver")
    InstallationId: str = Field(
        __CONFIG__.get("_InstallationId", ""), alias="_InstallationId"
    )


from datetime import datetime
from typing import Any
from pydantic import BaseModel, Field


class MojiDate(BaseModel):
    # {
    #     "__type": "Date",
    #     "iso": "2024-10-11T03:54:04.608Z"
    # },
    type: str = Field(..., alias="__type")
    iso: datetime

    def model_dump(self, *args, **kwargs):
        """Override model_dump to return the datetime directly"""
        # If we want to return just the datetime when dumping
        if kwargs.pop("mojidate2datetime", True):
            return self.iso
        return super().model_dump(*args, **kwargs)

    @classmethod
    def __get_pydantic_core_schema__(cls, source_type, handler):
        """Custom schema to handle datetime conversion"""
        from pydantic_core import core_schema

        return core_schema.no_info_after_validator_function(
            cls._convert_to_datetime, handler(source_type)
        )

    @classmethod
    def _convert_to_datetime(cls, v):
        """Convert the MojiDate to datetime if needed"""
        if isinstance(v, cls):
            return v.iso
        elif isinstance(v, dict) and "__type" in v and "iso" in v:
            return datetime.fromisoformat(v["iso"].replace("Z", "+00:00"))
        return v


class SharedFolderSchema(BaseModel):
    """
    _id: required
    createdBy: required
    updatedBy: required
    isTrash: required
    isShared: required
    isProduct: optional
    title: required
    langEnv: optional
    hasCover: required
    type: optional
    viewedNum: required
    rootFolderId: required
    contentUpdatedAt: required
    itemsNum: required
    totalWordsNum: required
    wordsNum: required
    category: optional
    imgVer: optional
    coverPath: optional
    attachments: optional
    brief: optional
    brief_rich: optional
    price_mo: optional
    version: required
    id: required
    objectId: required
    createdAt: required
    updatedAt: required
    followedNum: optional
    vTag: optional
    tags: optional
    sortType: optional
    commentedNum: optional
    sampleId: optional
    baseSortType: optional
    """

    id: str = Field(..., alias="_id")
    createdBy: str
    updatedBy: str
    isTrash: bool
    isShared: bool
    isProduct: Optional[bool] = None
    title: str
    langEnv: Optional[str] = None
    hasCover: bool
    type: Optional[int] = None
    viewedNum: int
    rootFolderId: str
    contentUpdatedAt: Optional[Union[datetime, MojiDate]] = None
    itemsNum: int
    totalWordsNum: int
    wordsNum: int
    category: Optional[List[str]] = None
    imgVer: Optional[int] = None
    coverPath: Optional[str] = None
    attachments: Optional[List[Any]] = None
    brief: Optional[str] = None
    brief_rich: Optional[str] = None
    price_mo: Optional[int] = None
    version: int
    id2: str = Field(..., alias="id")
    objectId: str
    createdAt: Optional[Union[datetime, MojiDate]] = None
    updatedAt: Optional[Union[datetime, MojiDate]] = None
    tags: Optional[List[str]] = None
    followedNum: Optional[int] = None
    vTag: Optional[str] = None
    sortType: Optional[int] = None
    commentedNum: Optional[int] = None
    sampleId: Optional[str] = None
    baseSortType: Optional[int] = None


class FetchSharedFoldersWithTypeResult(BaseModel):
    result: List[SharedFolderSchema]
    userInfo: Optional[list[dict]] = Field(None, alias="1")
    perPageCount: int
    pageIndex: int
    type: int
    code: int


class FetchSharedFoldersWithTypeResponse(BaseModel):
    result: FetchSharedFoldersWithTypeResult


class OfficialFolderSchema(BaseModel):
    """
    _id: required
    createdBy: required
    updatedBy: required
    isTrash: required
    isShared: required
    isProduct: required
    title: required
    viewedNum: required
    brief: required
    itemsNum: required
    followedNum: required
    contentUpdatedAt: required
    hasCover: required
    vTag: required
    commentedNum: required
    wordsNum: required
    rootFolderId: required
    totalWordsNum: required
    id: required
    objectId: required
    createdAt: required
    updatedAt: required
    category: optional
    version: optional
    """

    id: str = Field(..., alias="_id")
    createdBy: str
    updatedBy: str
    isTrash: bool
    isShared: bool
    isProduct: bool
    title: str
    viewedNum: int
    brief: str
    itemsNum: int
    followedNum: int
    contentUpdatedAt: Optional[Union[datetime, MojiDate]] = None
    hasCover: bool
    vTag: str
    commentedNum: int
    wordsNum: int
    rootFolderId: str
    totalWordsNum: int
    id2: str = Field(..., alias="id")
    objectId: str
    createdAt: Optional[Union[datetime, MojiDate]] = None
    updatedAt: Optional[Union[datetime, MojiDate]] = None
    category: Optional[List[str]] = None
    version: Optional[int] = None


class FetchOfficialFoldersResult(BaseModel):
    result: List[OfficialFolderSchema]
    userInfo: Optional[list[dict]] = Field(None, alias="1")
    perPageCount: int
    pageIndex: int
    type: int
    code: int


class FetchOfficialFoldersResponse(BaseModel):
    result: FetchOfficialFoldersResult


class ContentTarget(BaseModel):
    excerpt: Optional[str] = Field(None, alias="excerpt")
    spell: Optional[str] = Field(None, alias="spell")
    accent: Optional[str] = Field(None, alias="accent")
    pron: Optional[str] = Field(None, alias="pron")
    romaji: Optional[str] = Field(None, alias="romaji")
    reported_num: Optional[int] = Field(None, alias="reportedNum")
    out_shared_num: Optional[int] = Field(None, alias="outSharedNum")
    is_free: Optional[bool] = Field(None, alias="isFree")
    is_checked: Optional[bool] = Field(None, alias="isChecked")
    content_updated_at: Optional[Union[datetime, MojiDate]] = Field(
        None, alias="contentUpdatedAt"
    )
    updated_by: Optional[str] = Field(None, alias="updatedBy")
    v_tag: Optional[int] = Field(None, alias="vTag")
    quality: Optional[int] = Field(None, alias="quality")
    tags: Optional[str] = Field(None, alias="tags")
    viewed_num: Optional[int] = Field(None, alias="viewedNum")
    example_ids: Optional[List[str]] = Field(None, alias="exampleIds")
    is_shared: Optional[bool] = Field(None, alias="isShared")
    status: Optional[str] = Field(None, alias="status")
    subdetails_ids: Optional[List[str]] = Field(None, alias="subdetailsIds")
    type: Optional[int] = Field(None, alias="type")
    romaji_hepburn: Optional[str] = Field(None, alias="romaji_hepburn")
    romaji_hepburn_cn: Optional[str] = Field(None, alias="romaji_hepburn_CN")
    romaji_nippon: Optional[str] = Field(None, alias="romaji_nippon")
    romaji_nippon_cn: Optional[str] = Field(None, alias="romaji_nippon_CN")
    created_at: Optional[Union[datetime, MojiDate]] = Field(None, alias="createdAt")
    updated_at: Optional[Union[datetime, MojiDate]] = Field(None, alias="updatedAt")
    object_id: str = Field(..., alias="objectId")


class CollectionTarget(BaseModel):
    created_at: Optional[Union[datetime, MojiDate]] = Field(None, alias="createdAt")
    updated_at: Optional[Union[datetime, MojiDate]] = Field(None, alias="updatedAt")
    created_by: Optional[str] = Field(None, alias="createdBy")
    updated_by: Optional[str] = Field(None, alias="updatedBy")
    is_shared: Optional[bool] = Field(None, alias="isShared")
    is_product: Optional[bool] = Field(None, alias="isProduct")
    title: str
    content_updated_at: Optional[Union[datetime, MojiDate]] = Field(
        None, alias="contentUpdatedAt"
    )
    viewed_num: Optional[int] = Field(None, alias="viewedNum")
    items_num: Optional[int] = Field(None, alias="itemsNum")
    followed_num: Optional[int] = Field(None, alias="followedNum")
    has_cover: Optional[bool] = Field(None, alias="hasCover")
    commented_num: Optional[int] = Field(None, alias="commentedNum")
    words_num: Optional[int] = Field(None, alias="wordsNum")
    root_folder_id: Optional[str] = Field(None, alias="rootFolderId")
    total_words_num: Optional[int] = Field(None, alias="totalWordsNum")
    category: Optional[List[str]] = Field(None, alias="category")
    version: Optional[int] = Field(None, alias="version")
    object_id: str = Field(..., alias="objectId")

    class Config:
        allow_population_by_field_name = True


class SentenceTarget(BaseModel):
    word_id: str = Field(..., alias="wordId")
    subdetails_id: Optional[str] = Field(None, alias="subdetailsId")
    title: str
    lang: Optional[str] = Field(None, alias="lang")
    index: Optional[int] = Field(None, alias="index")
    is_shared: Optional[bool] = Field(None, alias="isShared")
    status: Optional[str] = Field(None, alias="status")
    created_by: str = Field(..., alias="createdBy")
    updated_at: Optional[Union[datetime, MojiDate]] = Field(None, alias="updatedAt")
    updated_by: Optional[str] = Field(None, alias="updatedBy")
    rela_id: str = Field(..., alias="relaId")
    trans: Optional[str] = Field(None, alias="trans")
    created_at: Optional[Union[datetime, MojiDate]] = Field(None, alias="createdAt")
    object_id: str = Field(..., alias="objectId")


class IgnoredTarget(BaseModel):
    pass


class ContentResult(BaseModel):
    created_at: Optional[Union[datetime, MojiDate]] = Field(None, alias="createdAt")
    updated_at: Optional[Union[datetime, MojiDate]] = Field(None, alias="updatedAt")
    created_by: str = Field(..., alias="createdBy")
    title: str
    updated_by: Optional[str] = Field(None, alias="updatedBy")
    target_type: int = Field(..., alias="targetType")
    target_id: str = Field(..., alias="targetId")
    parent_folder_id: Optional[str] = Field(None, alias="parentFolderId")
    root_folder_id: Optional[str] = Field(None, alias="rootFolderId")
    target_user_id: Optional[str] = Field(None, alias="targetUserId")
    app_id: Optional[str] = Field(None, alias="appId")
    version: Optional[int] = Field(None, alias="version")
    id: str
    object_id: str = Field(..., alias="objectId")
    target: Optional[
        Union[ContentTarget, CollectionTarget, SentenceTarget, IgnoredTarget]
    ]

    @model_validator(mode="before")
    @classmethod
    def parse_target(cls, values):
        t = values.get("targetType")
        data = values.get("target")

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

        return values


class FetchContentWithRelativesResult(BaseModel):
    result: List[ContentResult]
    info1: Optional[list[dict]] = Field(None, alias="1")
    info411: Optional[list[dict]] = Field(None, alias="411")
    info1000: Optional[list[dict]] = Field(None, alias="1000")
    fid: str
    pageIndex: int
    sortType: int
    size: int
    totalPage: int
    code: int


class FetchContentWithRelativesResponse(BaseModel):
    result: FetchContentWithRelativesResult
