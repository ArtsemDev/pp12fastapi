from pydantic import BaseModel, ConfigDict


class DTO(BaseModel):
    model_config = ConfigDict(
        str_strip_whitespace=True,
        from_attributes=True
    )
