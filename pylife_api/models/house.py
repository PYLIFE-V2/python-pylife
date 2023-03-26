from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Field, validator


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

    @validator("position", pre=True)
    def position_as_str(cls, value):
        if isinstance(value, str):
            x, y, z = value.split(",")
            return Position(x=x, y=y, z=z)

        return value
