from fastapi import Query
from pydantic import AfterValidator
from typing_extensions import Annotated

from .custom_validators import (
    password_validator,
    is_alpha_validator,
    is_positive_int_list
)


PasswordStr = Annotated[str, AfterValidator(password_validator)]
AlphaStr = Annotated[str, AfterValidator(is_alpha_validator)]
ListPositiveInt = Annotated[list[int], AfterValidator(is_positive_int_list)]
