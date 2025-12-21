# models.py
from datetime import datetime
from typing import List, Optional, Union

from tortoise import fields, models
from tortoise.fields import (
    BooleanField,
    CharField,
    DatetimeField,
    ForeignKeyField,
    IntField,
    JSONField,
    ManyToManyField,
    TextField,
)


class ContentTarget(models.Model):
    """
    Model representing a content target with various linguistic information.
    """

    id = fields.IntField(pk=True)
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
    object_id = CharField(max_length=255)

    # Many-to-many relationship with ContentResult
    content_results = ManyToManyField(
        "models.ContentResult",
        related_name="content_targets",
        through="contentresult_contenttarget",
    )

    class Meta:
        table = "content_target"


class CollectionTarget(models.Model):
    """
    Model representing a collection target with metadata about collections.
    """

    id = fields.IntField(pk=True)
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
    object_id = CharField(max_length=255)

    # Many-to-many relationship with ContentResult
    content_results = ManyToManyField(
        "models.ContentResult",
        related_name="collection_targets",
        through="contentresult_collectiontarget",
    )

    class Meta:
        table = "collection_target"


class SentenceTarget(models.Model):
    """
    Model representing a sentence target with word and sentence details.
    """

    id = fields.IntField(pk=True)
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
    object_id = CharField(max_length=255)

    # Many-to-many relationship with ContentResult
    content_results = ManyToManyField(
        "models.ContentResult",
        related_name="sentence_targets",
        through="contentresult_sentencetarget",
    )

    class Meta:
        table = "sentence_target"


class ContentResult(models.Model):
    """
    Model representing a content result that can be associated with multiple targets.
    One ContentResult can have many targets of different types.
    """

    id = fields.IntField(pk=True)
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
class ContentResultContentTarget(models.Model):
    """
    Junction table for many-to-many relationship between ContentResult and ContentTarget
    """

    content_result = ForeignKeyField("models.ContentResult", on_delete=fields.CASCADE)
    content_target = ForeignKeyField("models.ContentTarget", on_delete=fields.CASCADE)

    class Meta:
        table = "contentresult_contenttarget"


class ContentResultCollectionTarget(models.Model):
    """
    Junction table for many-to-many relationship between ContentResult and CollectionTarget
    """

    content_result = ForeignKeyField("models.ContentResult", on_delete=fields.CASCADE)
    collection_target = ForeignKeyField(
        "models.CollectionTarget", on_delete=fields.CASCADE
    )

    class Meta:
        table = "contentresult_collectiontarget"


class ContentResultSentenceTarget(models.Model):
    """
    Junction table for many-to-many relationship between ContentResult and SentenceTarget
    """

    content_result = ForeignKeyField("models.ContentResult", on_delete=fields.CASCADE)
    sentence_target = ForeignKeyField("models.SentenceTarget", on_delete=fields.CASCADE)

    class Meta:
        table = "contentresult_sentencetarget"


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
