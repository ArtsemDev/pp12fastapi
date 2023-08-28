from datetime import datetime
from typing import Self

from pydantic import Field, PositiveInt, model_validator
from slugify import slugify
from ulid import new

from .base import DTO


class PostBasic(DTO):
    title: str = Field(
        default=...,
        min_length=4,
        max_length=128,
        title='Post title'
    )
    body: str = Field(
        default=...
    )
    category_id: PositiveInt = Field(
        default=...
    )


class PostAddForm(PostBasic):
    ...


class PostDetail(PostBasic):
    slug: str = Field(
        default=...,
        min_length=4,
        max_length=164,
        title='Post slug'
    )
    author_id: str = Field(
        default_factory=lambda: new().str,
        min_length=26,
        max_length=26,
        title='User unique identify',
        description='Universally Unique Lexicographically Sortable Identifier'
    )
    date_created: datetime = Field(
        default_factory=datetime.utcnow
    )
    id: PositiveInt = Field(
        default=...
    )
    is_published: bool = Field(
        default=False
    )

    @model_validator(mode='after')
    def validator(self) -> Self:
        if self.slug is None:
            self.slug = slugify(f'{self.title}-{self.date_created.timestamp()}')
        return self
