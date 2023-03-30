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
    """
    Client for Play Your Life API.
    """

    def __init__(self, auth_token: Optional[str] = None):
        """
        Initialize client.

        Args:
            auth_token (str, optional): Token for authorization. Defaults to None.
        """
        self._auth_token = auth_token
        self._session = aiohttp.ClientSession(
            base_url="https://panel.pylife-rpg.pl/",
            json_serialize=json.dumps,
            headers={
                "Content-Type": "application/json",
                "User-Agent": f"pylife-api/2.0 (Python {python_version()}; aiohttp {aiohttp.__version__})",
            },
        )

    async def fetch(self, method: str, url: str, **kwargs) -> Any:
        """
        Fetch data from API.

        Args:
            method (str): HTTP method.
            url (str): Endpoint URL.
            **kwargs: Additional arguments for request.

        Returns:
            Any: Response data.
        """
        async with self._session.request(method=method, url=url, **kwargs) as resp:
            resp.raise_for_status()
            return await resp.json(loads=json.loads)

    async def get_house(self, house_id: int) -> House:
        """
        Get house by ID.

        Args:
            house_id (int): House ID.

        Returns:
            House: House object.
        """
        json_data = await self.fetch("GET", f"/api/domy/{house_id}")
        return House.parse_obj(json_data)

    async def get_houses(self) -> List[House]:
        """
        Get all houses.

        Returns:
            List[House]: List of houses.
        """
        json_data = await self.fetch("GET", "/api/domy")
        return parse_obj_as(List[House], json_data)

    async def get_organization(self, organization_id: int) -> Organization:
        """
        Get organization by ID.

        Args:
            organization_id (int): Organization ID.

        Returns:
            Organization: Organization object.
        """
        json_data = await self.fetch("GET", f"/api/organizacje/{organization_id}")
        return Organization.parse_obj(json_data)

    async def get_organizations(self) -> List[Organization]:
        """
        Get all organizations.

        Returns:
            List[Organization]: List of organizations.
        """
        json_data = await self.fetch("GET", "/api/organizacje")
        return parse_obj_as(List[Organization], json_data)

    async def get_player(self, player_id: int) -> Player:
        """
        Get player by ID.

        Args:
            player_id (int): Player ID.

        Returns:
            Player: Player object.
        """
        json_data = await self.fetch("GET", f"/api/gracz/{player_id}")
        return Player.parse_obj(json_data)

    async def get_players(self) -> List[Player]:
        """
        Get all players.

        Returns:
            List[Player]: List of players.

        Raises:
            ValueError: If no auth_token provided.
        """
        if not self._auth_token:
            raise ValueError("No auth_token provided for authorization")

        json_data = await self.fetch("POST", "/api/gracze", json={"auth": self._auth_token})
        return parse_obj_as(List[Player], json_data)

    async def search(self, query: str) -> List[Player]:
        """
        Search for players.

        Args:
            query (str): Search query.

        Returns:
            List[Player]: List of players.
        """
        json_data = await self.fetch("GET", f"/api/search/{query}")
        return parse_obj_as(List[Player], json_data)

    async def close(self):
        """
        Close client session.
        """
        await self._session.close()

    async def __aenter__(self):
        """
        Enter the context manager and return an object.

        Returns:
            PylifeAPIClient: Client object.
        """
        return self

    async def __aexit__(self, exc_type, exc_value, traceback):
        """
        Exit the context manager.

        Args:
            exc_type (type): The type of the exception that occurred, if any.
            exc_value (Exception): The exception instance that was raised, if any.
            traceback (traceback): The traceback of the exception that was raised, if any.
        """
        await self.close()
