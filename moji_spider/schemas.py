# schemas.py
from typing import List, Optional, Dict, Any, Union
from pydantic import BaseModel, Field, model_validator
from datetime import datetime
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


class MojiDate(BaseModel):
    # {
    #     "__type": "Date",
    #     "iso": "2024-10-11T03:54:04.608Z"
    # },
    type: str = Field(..., alias="__type")
    iso: datetime


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
    excerpt: Optional[str] = None
    spell: Optional[str] = None
    accent: Optional[str] = None
    pron: Optional[str] = None
    romaji: Optional[str] = None
    reportedNum: Optional[int] = None
    outSharedNum: Optional[int] = None
    isFree: Optional[bool] = None
    isChecked: Optional[bool] = None
    contentUpdatedAt: Optional[Union[datetime, MojiDate]] = None
    updatedBy: Optional[str] = None
    vTag: Optional[int] = None
    quality: Optional[int] = None
    tags: Optional[str] = None
    viewedNum: Optional[int] = None
    exampleIds: Optional[List[str]] = None
    isShared: Optional[bool] = None
    status: Optional[str] = None
    subdetailsIds: Optional[List[str]] = None
    type: Optional[int] = None
    romaji_hepburn: Optional[str] = None
    romaji_hepburn_CN: Optional[str] = None
    romaji_nippon: Optional[str] = None
    romaji_nippon_CN: Optional[str] = None
    createdAt: Optional[Union[datetime, MojiDate]]
    updatedAt: Optional[Union[datetime, MojiDate]]
    objectId: str


class CollectionTarget(BaseModel):
    createdAt: Optional[Union[datetime, MojiDate]] = None
    updatedAt: Optional[Union[datetime, MojiDate]] = None
    createdBy: Optional[str] = None
    updatedBy: Optional[str] = None
    isShared: Optional[bool] = None
    isProduct: Optional[bool] = None
    title: str
    contentUpdatedAt: Optional[Union[datetime, MojiDate]] = None
    viewedNum: Optional[int] = None
    itemsNum: Optional[int] = None
    followedNum: Optional[int] = None
    hasCover: Optional[bool] = None
    commentedNum: Optional[int] = None
    wordsNum: Optional[int] = None
    rootFolderId: Optional[str] = None
    totalWordsNum: Optional[int] = None
    category: Optional[List[str]] = None
    version: Optional[int] = None
    objectId: str

    class Config:
        allow_population_by_field_name = True


class SentenceTarget(BaseModel):
    wordId: str
    subdetailsId: Optional[str]
    title: str
    lang: Optional[str]
    index: Optional[int]
    isShared: Optional[bool] = None
    status: Optional[str] = None
    createdBy: str
    updatedAt: Optional[Union[datetime, MojiDate]] = None
    updatedBy: Optional[str] = None
    relaId: str
    trans: Optional[str]
    createdAt: Optional[Union[datetime, MojiDate]]
    objectId: str


class IgnoredTarget(BaseModel):
    pass


class ContentResult(BaseModel):
    createdAt: Optional[Union[datetime, MojiDate]] = None
    updatedAt: Optional[Union[datetime, MojiDate]] = None
    createdBy: str
    title: str
    updatedBy: Optional[str] = None
    targetType: int
    targetId: str
    parentFolderId: Optional[str] = None
    rootFolderId: Optional[str] = None
    targetUserId: Optional[str] = None
    appId: Optional[str] = None
    version: Optional[int] = None
    id: str
    objectId: str
    target: Optional[
        Union[ContentTarget, CollectionTarget, SentenceTarget, IgnoredTarget]
    ]

    @model_validator(mode="before")
    @classmethod
    def parse_target(cls, values):
        t = values.get("targetType")
        data = values.get("target")

        if t == 1000:
            values["target"] = CollectionTarget.model_validate(data)
        elif t in [102, 104]:
            values["target"] = ContentTarget.model_validate(data)
        elif t == 103:
            values["target"] = SentenceTarget.model_validate(data)
        elif t == 431:
            values["target"] = IgnoredTarget.model_validate(data)
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
