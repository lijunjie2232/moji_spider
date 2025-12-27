# models.py
from datetime import datetime
from typing import List, Optional, Reversible, Union

from tortoise import Model, fields
from tortoise.fields import (
    BooleanField,
    CharField,
    DatetimeField,
    ForeignKeyField,
    IntField,
    JSONField,
    ManyToManyField,
    ManyToManyRelation,
    TextField,
)


class SharedFolder(Model):
    # Primary key using the id from the schema
    id = CharField(max_length=255, pk=True)  # corresponds to _id field

    # Basic fields
    created_by = CharField(max_length=255)
    updated_by = CharField(max_length=255)
    is_trash = BooleanField()
    is_shared = BooleanField()
    is_product = BooleanField(null=True)
    title = CharField(max_length=500)  # assuming reasonable max length
    lang_env = CharField(max_length=50, null=True)
    has_cover = BooleanField()
    type = IntField(null=True)
    viewed_num = IntField()
    root_folder_id = CharField(max_length=255)

    # Date/time fields
    content_updated_at = DatetimeField(null=True)

    # Numeric fields
    items_num = IntField()
    total_words_num = IntField()
    words_num = IntField()

    # Array/JSON fields
    category = JSONField(null=True)  # List[str]
    img_ver = IntField(null=True)
    cover_path = CharField(max_length=500, null=True)
    attachments = JSONField(null=True)  # List[Any]

    # Text fields
    brief = TextField(null=True)
    brief_rich = TextField(null=True)
    price_mo = IntField(null=True)
    version = IntField()

    # Additional ID field
    id2 = CharField(max_length=255)  # corresponds to id field
    object_id = CharField(max_length=255)

    # Timestamps
    created_at = DatetimeField(null=True)
    updated_at = DatetimeField(null=True)

    # Additional fields
    tags = JSONField(null=True)  # List[str]
    followed_num = IntField(null=True)
    v_tag = CharField(max_length=100, null=True)
    sort_type = IntField(null=True)
    commented_num = IntField(null=True)
    sample_id = CharField(max_length=255, null=True)
    base_sort_type = IntField(null=True)

    # Meta configuration
    class Meta:
        table = "shared_folders"  # specify table name


class OfficialFolder(Model):
    # Primary key using the id from the schema
    id = CharField(max_length=255, pk=True)  # corresponds to _id field

    # Basic fields
    created_by = CharField(max_length=255)
    updated_by = CharField(max_length=255)
    is_trash = BooleanField()
    is_shared = BooleanField()
    is_product = BooleanField()
    title = CharField(max_length=500)  # assuming reasonable max length
    viewed_num = IntField()
    brief = TextField()

    # Numeric fields
    items_num = IntField()
    followed_num = IntField()

    # Date/time fields
    content_updated_at = DatetimeField(null=True)

    # Boolean fields
    has_cover = BooleanField()
    v_tag = CharField(max_length=100)  # assuming vTag is a string
    commented_num = IntField()
    words_num = IntField()
    root_folder_id = CharField(max_length=255)
    total_words_num = IntField()

    # Additional ID fields
    id2 = CharField(max_length=255)  # corresponds to id field
    object_id = CharField(max_length=255)

    # Timestamps
    created_at = DatetimeField(null=True)
    updated_at = DatetimeField(null=True)

    # Optional fields
    category = JSONField(null=True)  # List[str]
    version = IntField(null=True)

    # Meta configuration
    class Meta:
        table = "official_folders"  # specify table name


class ContentTarget(Model):
    """
    Model representing a content target with various linguistic information.
    """

    excerpt = TextField(null=True)
    spell = CharField(max_length=255, null=True)
    accent = CharField(max_length=255, null=True)
    pron = CharField(max_length=255, null=True)
    romaji = CharField(max_length=255, null=True)
    reported_num = IntField(null=True)
    out_shared_num = IntField(null=True)
    is_free = BooleanField(null=True)
    is_checked = BooleanField(null=True)
    content_updated_at = DatetimeField(null=True)
    updated_by = CharField(max_length=255, null=True)
    v_tag = IntField(null=True)
    quality = IntField(null=True)
    tags = TextField(null=True)
    viewed_num = IntField(null=True)
    example_ids = JSONField(null=True)
    is_shared = BooleanField(null=True)
    status = CharField(max_length=50, null=True)
    subdetails_ids = JSONField(null=True)
    type = IntField(null=True)
    romaji_hepburn = CharField(max_length=255, null=True)
    romaji_hepburn_cn = CharField(max_length=255, null=True)
    romaji_nippon = CharField(max_length=255, null=True)
    romaji_nippon_cn = CharField(max_length=255, null=True)
    created_at = DatetimeField(null=True)
    updated_at = DatetimeField(null=True)
    object_id = CharField(max_length=255, pk=True)

    # Many-to-many relationship with ContentResult
    content_results = ManyToManyRelation["ContentResult"]

    class Meta:
        table = "content_target"


class CollectionTarget(Model):
    """
    Model representing a collection target with metadata about collections.
    """

    created_at = DatetimeField(null=True)
    updated_at = DatetimeField(null=True)
    created_by = CharField(max_length=255, null=True)
    updated_by = CharField(max_length=255, null=True)
    is_shared = BooleanField(null=True)
    is_product = BooleanField(null=True)
    title = TextField()
    content_updated_at = DatetimeField(null=True)
    viewed_num = IntField(null=True)
    items_num = IntField(null=True)
    followed_num = IntField(null=True)
    has_cover = BooleanField(null=True)
    commented_num = IntField(null=True)
    words_num = IntField(null=True)
    root_folder_id = CharField(max_length=255, null=True)
    total_words_num = IntField(null=True)
    category = JSONField(null=True)
    version = IntField(null=True)
    object_id = CharField(max_length=255, pk=True)

    # Many-to-many relationship with ContentResult
    content_results = ManyToManyRelation["ContentResult"]

    class Meta:
        table = "collection_target"


class SentenceTarget(Model):
    """
    Model representing a sentence target with word and sentence details.
    """

    word_id = CharField(max_length=255)
    subdetails_id = CharField(max_length=255, null=True)
    title = TextField()
    lang = CharField(max_length=50, null=True)
    index = IntField(null=True)
    is_shared = BooleanField(null=True)
    status = CharField(max_length=50, null=True)
    created_by = CharField(max_length=255)
    updated_at = DatetimeField(null=True)
    updated_by = CharField(max_length=255, null=True)
    rela_id = CharField(max_length=255)
    trans = TextField(null=True)
    created_at = DatetimeField(null=True)
    object_id = CharField(max_length=255, pk=True)

    # Many-to-many relationship with ContentResult
    content_results = ManyToManyRelation["ContentResult"]

    class Meta:
        table = "sentence_target"


class ContentResult(Model):
    """
    Model representing a content result that can be associated with multiple targets.
    One ContentResult can have many targets of different types.
    """

    id = CharField(max_length=255, pk=True)
    created_at = DatetimeField(null=True)
    updated_at = DatetimeField(null=True)
    created_by = CharField(max_length=255)
    title = TextField()
    updated_by = CharField(max_length=255, null=True)
    target_type = IntField()  # 1000: collection; 102/104: word/grammar; 103: sentence
    target_id = CharField(max_length=255)
    parent_folder_id = CharField(max_length=255, null=True)
    root_folder_id = CharField(max_length=255, null=True)
    target_user_id = CharField(max_length=255, null=True)
    app_id = CharField(max_length=255, null=True)
    version = IntField(null=True)
    object_id = CharField(max_length=255)

    # Many-to-many relationships to targets
    content_targets = ManyToManyField(
        "models.ContentTarget",
        related_name="content_results",
        through="contentresult_contenttarget",
    )
    collection_targets = ManyToManyField(
        "models.CollectionTarget",
        related_name="content_results",
        through="contentresult_collectiontarget",
    )
    sentence_targets = ManyToManyField(
        "models.SentenceTarget",
        related_name="content_results",
        through="contentresult_sentencetarget",
    )

    class Meta:
        table = "content_result"


# Junction tables for many-to-many relationships
# class ContentResultContentTarget(Model):
#     """
#     Junction table for many-to-many relationship between ContentResult and ContentTarget
#     """

#     content_result = ForeignKeyField("models.ContentResult", on_delete=fields.CASCADE)
#     content_target = ForeignKeyField("models.ContentTarget", on_delete=fields.CASCADE)

#     class Meta:
#         table = "contentresult_contenttarget"


# class ContentResultCollectionTarget(Model):
#     """
#     Junction table for many-to-many relationship between ContentResult and CollectionTarget
#     """

#     content_result = ForeignKeyField("models.ContentResult", on_delete=fields.CASCADE)
#     collection_target = ForeignKeyField(
#         "models.CollectionTarget", on_delete=fields.CASCADE
#     )

#     class Meta:
#         table = "contentresult_collectiontarget"


# class ContentResultSentenceTarget(Model):
#     """
#     Junction table for many-to-many relationship between ContentResult and SentenceTarget
#     """

#     content_result = ForeignKeyField("models.ContentResult", on_delete=fields.CASCADE)
#     sentence_target = ForeignKeyField("models.SentenceTarget", on_delete=fields.CASCADE)

#     class Meta:
#         table = "contentresult_sentencetarget"


if __name__ == "__main__":
    # test connection
    from tortoise import Tortoise, run_async

    from moji_spider.configs import __TORTOISE_ORM__

    async def init():
        await Tortoise.init(
            db_url="mysql://moji:moji@127.0.0.1:13306/moji_test",
            modules={"models": ["moji_spider.models"]},
        )
        await Tortoise.generate_schemas()

    run_async(init())
