from datetime import datetime
from typing import Optional

from pydantic import field_validator, BaseModel, Field


class Position(BaseModel):
    x: float
    y: float
    z: float


class House(BaseModel):
    id: int = Field(alias="id")
    title: str = Field(alias="title")
    position: Position = Field(alias="pos")
    owner: Optional[int] = Field(alias="owner")
    organization: Optional[int] = Field(alias="organization")
    expires: Optional[datetime] = Field(alias="expires")
    price: float = Field(alias="price")

    @field_validator("position", mode="before")
    def position_as_str(cls, value):
        if isinstance(value, str):
            x, y, z = value.split(",")
            return Position(x=x, y=y, z=z)

        return value
