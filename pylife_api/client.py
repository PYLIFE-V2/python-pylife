from platform import python_version
from typing import Any, List, Optional

import aiohttp
from pydantic import parse_obj_as

try:
    import rapidjson as json
except ImportError:
    import json

from .models import House, Organization, Player


class PylifeAPIClient:
    auth_token: Optional[str]
    session: aiohttp.ClientSession

    def __init__(self, auth_token: Optional[str] = None):
        self.auth_token = auth_token
        self.session = aiohttp.ClientSession(
            base_url="https://panel.pylife-rpg.pl/",
            json_serialize=json.dumps,
            headers={
                "Content-Type": "application/json",
                "User-Agent": f"pylife-api/2.0 (Python {python_version()}; aiohttp {aiohttp.__version__})",
            },
        )

    async def fetch(self, method: str, url: str, **kwargs) -> Any:
        async with self.session.request(method=method, url=url, **kwargs) as resp:
            resp.raise_for_status()
            return await resp.json(loads=json.loads)

    async def get_house(self, house_id: int) -> House:
        json_data = await self.fetch("GET", f"/api/domy/{house_id}")
        return House.parse_obj(json_data)

    async def get_houses(self) -> List[House]:
        json_data = await self.fetch("GET", "/api/domy")
        return parse_obj_as(List[House], json_data)

    async def get_organization(self, organization_id: int) -> Organization:
        json_data = await self.fetch("GET", f"/api/organizacje/{organization_id}")
        return Organization.parse_obj(json_data)

    async def get_organizations(self) -> List[Organization]:
        json_data = await self.fetch("GET", "/api/organizacje")
        return parse_obj_as(List[Organization], json_data)

    async def get_player(self, player_id: int) -> Player:
        json_data = await self.fetch("GET", f"/api/gracz/{player_id}")
        return Player.parse_obj(json_data)

    async def get_players(self) -> List[Player]:
        if not self.auth_token:
            raise ValueError("No auth_token provided for authorization")

        json_data = await self.fetch("POST", "/api/gracze", json={"auth": self.auth_token})
        return parse_obj_as(List[Player], json_data)

    async def search(self, query: str) -> List[Player]:
        json_data = await self.fetch("GET", f"/api/search/{query}")
        return parse_obj_as(List[Player], json_data)

    async def close(self):
        await self.session.close()
