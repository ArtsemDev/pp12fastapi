from typing import Self, List, Optional

from pydantic import Field, model_validator, PositiveInt, field_validator
from slugify import slugify
from sqlalchemy import select

from .base import DTO
from .custom_types import AlphaStr
from .post import PostDetail
from src.database import Category


class CategoryBasic(DTO):
    name: AlphaStr = Field(
        default=...,
        min_length=4,
        max_length=64,
        title='Category name',
        description='Unique category name'
    )


class CategoryAddForm(CategoryBasic):

    @field_validator('name', mode='after')
    def name_validator(cls, name: str) -> str:
        with Category.session() as session:
            category = session.scalar(select(Category).filter_by(name=name))
            if category is not None:
                raise ValueError('category name is not unique')
            return name


class CategoryDetail(CategoryBasic):
    id: PositiveInt = Field(
        default=None,
        title='Category ID',
        description='Category Unique Identify'
    )
    slug: str = Field(
        default=None,
        min_length=4,
        max_length=64,
        title='Category slug'
    )
    # posts: Optional[List[PostDetail]]

    @model_validator(mode='after')
    def validator(self) -> Self:
        if self.slug is None:
            self.slug = slugify(self.name)
        return self
