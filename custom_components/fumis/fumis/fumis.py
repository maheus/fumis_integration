"""Asynchronous Python for the Fumis WiRCU API."""
import asyncio
import socket
from typing import Dict, Optional, Union

import aiohttp
from yarl import URL

from .__version__ import __version__
from .exceptions import FumisConnectionError, FumisError
from .models import Info


class Fumis:
    """Main class for handling connections with the Fumis WiRCU API."""

    info: Optional[Info] = None

    def __init__(
        self,
        mac: str,
        password: str,
        application_name: str = "PythonFumis",
        loop: asyncio.events.AbstractEventLoop = None,
        request_timeout: int = 60,
        session: aiohttp.client.ClientSession = None,
        user_agent: str = None,
    ) -> None:
        """Initialize connection with the Fumis WiRCU API."""
        self._loop = loop
        self._session = session
        self._close_session = False

        self.mac = mac
        self.password = password
        self.application_name = application_name
        self.request_timeout = request_timeout
        self.user_agent = user_agent

        if user_agent is None:
            self.user_agent = f"PythonFumis/{__version__}"

    async def _request(
        self,
        uri: str = "",
        method: str = "GET",
        data: Optional[Dict[str, Union[int, str]]] = None,
    ) -> Optional[Dict[str, Union[bool, int, str]]]:
        """Handle a request to the Fumis WiRCU API."""
        url = URL.build(
            scheme="https", host="api.fumis.si", port=443, path="/v1/"
            #scheme="http", host="api.fumis.si", port=80, path="/v1/"
        ).join(URL(uri))

        if self._loop is None:
            self._loop = asyncio.get_event_loop()

        if self._session is None:
            self._session = aiohttp.ClientSession(loop=self._loop)
            self._close_session = True

        try:
            async with asyncio.timeout(self.request_timeout):
                response = await self._session.request(
                    method,
                    url,
                    json=data,
                    headers={
                        "Accept": "application/json",
                        "appname": self.application_name,
                        "password": self.password,
                        "User-Agent": self.user_agent,
                        "username": self.mac,
                    },
                )
                response.raise_for_status()
        except asyncio.TimeoutError as exception:
            raise FumisConnectionError(
                "Timeout occurred while connecting to the Fumis WiRCU API"
            ) from exception
        except (
            aiohttp.ClientError,
            aiohttp.ClientResponseError,
            socket.gaierror,
        ) as exception:
            raise FumisConnectionError(
                "Error occurred while communicating with to the Fumis WiRCU API"
            ) from exception

        content_type = response.headers.get("Content-Type", "")
        if "application/json" not in content_type:
            text = await response.text()
            raise FumisError(
                "Unexpected response from the Fumis WiRCU API",
                {"Content-Type": content_type, "response": text},
            )

        response_data = await response.json()
        return response_data

    async def _send_command(self, data):
        command_data = {
            "unit": {"id": self.mac, "type": 0, "pin": self.password},
            "apiVersion": "1",
            "controller": data,
        }

        await self._request("status/", method="POST", data=command_data)

    async def update_info(self) -> Optional[Info]:
        """Get all information about the Fumis WiRCU device."""
        try:
            data = await self._request("status")
        except FumisError as exception:
            self.info = None
            raise exception

        if data is None:
            self.info = None
            raise FumisError("Did not receive data from the Fumis WiRCU API")

        self.info = Info.from_dict(data)
        return self.info

    async def turn_on(self) -> None:
        """Turn on Fumis WiRCU device."""
        await self._send_command({"command": 2, "type": 0})

    async def turn_off(self) -> None:
        """Turn off Fumis WiRCU device."""
        await self._send_command({"command": 1, "type": 0})

    async def set_target_temperature(self, temperature: float, temperature_id: int) -> None:
        """Set target temperature of Fumis WiRCU device."""
        await self._send_command(
            {"temperatures": [{"set": temperature, "id": temperature_id}], "type": 0}
        )

    async def set_mode(self, mode: int) -> None:
        """Set target mode of Fumis WiRCU device."""
        await self._send_command(
            {"ecoMode":{"ecoModeEnable": mode}}
        )

    async def set_power(self, power: int) -> None:
        """Set power of Fumis WiRCU device."""
        await self._send_command(
            {"power": {"setPower": power}}
        )

    async def close(self) -> None:
        """Close open client session."""
        if self._session and self._close_session:
            await self._session.close()

    async def __aenter__(self) -> "Fumis":
        """Async enter."""
        return self

    async def __aexit__(self, *exc_info) -> None:
        """Async exit."""
        await self.close()
