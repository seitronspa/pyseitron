"""Seitron api package for IoT device"""

from abc import ABC, abstractmethod
from aiohttp import ClientResponse, ClientSession

class AbstractAuth(ABC):
    """Abstract class to make authenticated requests."""

    def __init__(self, websession: ClientSession, host: str) -> None:
        """Initialize the auth."""
        self.websession = websession
        self.host = host

    @abstractmethod
    async def async_get_access_token(self) -> str:
        """Return a valid access token."""

    async def request(self, method, url, **kwargs) -> ClientResponse:
        """API request injected with access_token."""

        headers = kwargs.get("headers")
        if headers is None:
            headers = {}
        else:
            headers = dict(headers)

        access_token = await self.async_get_access_token()
        headers["authorization"] = f"Bearer {access_token}"
        kwargs["headers"] = headers

        complete_url = f"{self.host}/{url}"
        return await self.websession.request(method, complete_url, **kwargs)
