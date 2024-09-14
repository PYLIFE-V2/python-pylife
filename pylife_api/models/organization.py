from datetime import datetime
from typing import List, Optional

from pydantic import field_validator, BaseModel, Field, ValidationError, parse_obj_as
from pydantic.networks import HttpUrl


class Member(BaseModel):
    id: int = Field(alias="uid")
    rank: int = Field(alias="rank")
    join_date: datetime = Field(alias="joinDate")


class Organization(BaseModel):
    id: int = Field(alias="id")
    name: str = Field(alias="name")
    tag: str = Field(alias="tag")
    logo: Optional[HttpUrl] = Field(None, alias="logo")
    website: Optional[HttpUrl] = Field(None, alias="website")
    ranks: List[str] = Field(alias="ranks")
    leader: int = Field(alias="leader")
    registered: datetime = Field(alias="registerDate")
    money: int = Field(alias="money")
    members: Optional[List[Member]] = Field(None, alias="members")

    @field_validator("logo", "website", mode="before")
    def validate_urls(cls, value):
        try:
            return parse_obj_as(HttpUrl, value)
        except ValidationError:
            return None
