from pydantic import AfterValidator
from typing_extensions import Annotated

from .custom_validators import (
    password_validator,
    is_alpha_validator
)


PasswordStr = Annotated[str, AfterValidator(password_validator)]
AlphaStr = Annotated[str, AfterValidator(is_alpha_validator)]
