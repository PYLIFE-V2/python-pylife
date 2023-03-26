from datetime import datetime
from typing import List, Optional

from pydantic import BaseModel, Field, ValidationError, parse_obj_as, validator
from pydantic.networks import HttpUrl


class Member(BaseModel):
    id: int = Field(alias="uid")
    rank: int = Field(alias="rank")
    join_date: datetime = Field(alias="joinDate")


class Organization(BaseModel):
    id: int = Field(alias="id")
    name: str = Field(alias="name")
    tag: str = Field(alias="tag")
    logo: Optional[HttpUrl] = Field(alias="logo")
    website: Optional[HttpUrl] = Field(alias="website")
    ranks: List[str] = Field(alias="ranks")
    leader: int = Field(alias="leader")
    registered: datetime = Field(alias="registerDate")
    money: int = Field(alias="money")
    members: Optional[List[Member]] = Field(alias="members")

    @validator("logo", "website", pre=True)
    def validate_urls(cls, value):
        try:
            return parse_obj_as(HttpUrl, value)
        except ValidationError:
            return None
