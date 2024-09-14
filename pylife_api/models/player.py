from datetime import datetime, timezone
from typing import List, Optional

from pydantic import BaseModel, Field
from pydantic.networks import HttpUrl


class Achievement(BaseModel):
    title: str = Field(alias="title")
    description: str = Field(alias="description")
    points: int = Field(alias="pg")
    date: datetime = Field(alias="date")
    origin: str = Field(alias="origin")


class Membership(BaseModel):
    player_id: int = Field(alias="uid")
    organization_id: int = Field(alias="org")
    rank: Optional[int] = Field(alias="rank")
    join_date: datetime = Field(alias="joinDate")
    reputation: int = Field(alias="reputation")
    kills: int = Field(alias="kills")
    deaths: int = Field(alias="deaths")


class Fine(BaseModel):
    id: int = Field(alias="id")
    name: str = Field(alias="name")
    price: float = Field(alias="price")
    policeman: str = Field(alias="policeman")
    photo: Optional[HttpUrl] = Field(alias="photo")
    description: Optional[str] = Field(alias="description")
    penalty: int = Field(alias="pk")


class Player(BaseModel):
    id: int = Field(alias="id")
    login: str = Field(alias="login")
    played_time: int = Field(alias="playedTime")
    last_online: datetime = Field(alias="lastOnline")
    gender: str = Field(alias="gender")
    good_reputation: int = Field(alias="goodReputation")
    bad_reputation: int = Field(alias="badReputation")
    points: int = Field(alias="pg")
    premium: Optional[datetime] = Field(alias="premium")
    registered: datetime = Field(alias="registered")
    achievements: Optional[List[Achievement]] = Field(None, alias="achievements")
    organizations: Optional[List[Membership]] = Field(None, alias="organization")
    fines: Optional[List[Fine]] = Field(None, alias="fines")

    @property
    def reputation(self) -> int:
        return self.good_reputation - self.bad_reputation

    @property
    def has_premium(self) -> bool:
        return self.premium and self.premium >= datetime.now(timezone.utc)
