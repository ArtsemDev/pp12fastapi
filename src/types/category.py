from typing import Self

from pydantic import Field, model_validator, PositiveInt
from slugify import slugify

from .base import DTO
from .custom_types import AlphaStr


class CategoryBasic(DTO):
    name: AlphaStr = Field(
        default=...,
        min_length=4,
        max_length=64,
        title='Category name',
        description='Unique category name'
    )


class CategoryAddForm(CategoryBasic):
    ...


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

    @model_validator(mode='after')
    def validator(self) -> Self:
        if self.slug is None:
            self.slug = slugify(self.name)
        return self
