"""Seitron api package for IoT device"""

import asyncio
from .auth import AbstractAuth
from .seitron_thermostat import SeitronThermostat

class SeitronGateway:
    """Central data API entity."""

    def __init__(self, http_client):
        """Initialize Seitron gateway communicator."""
        self._devices = []  # type SeitronThermostat[]
        self._lock = asyncio.Lock()
        self._http_client = http_client or AbstractAuth

    async def update(self):
        """Get latest data from API."""

        if len(self._devices) > 0:
            await self.update_status()
        else:
            await self.listing()
            await self.update_status()

    @property
    def devices(self) -> list:
        """Detected devices"""
        return self._devices

    async def update_status(self):
        """Update status of all devices"""
        async with self._lock:
            headers_dict = {}
            headers_dict["Content-Type"] = "application/json"
            json_request_body = {"gmacs": []}
            for device in self._devices:
                json_request_body["gmacs"].append(device.gmac)

            res = await self._http_client.request(
                "POST",
                "thermo_statuses",
                headers=headers_dict,
                json=json_request_body,
            )
            if not res.ok:
                return

            data = await res.json()
            for thermo in data:
                for device in self._devices:
                    if device.gmac == thermo["gMac"]:
                        device.set_hvac_mode(thermo["mode"])
                        device.set_temp_curr(thermo["temp_curr"])
                        if thermo["temp_target"] == 3058.3:
                            device.set_temperature(None)
                        else:
                            device.set_temperature(thermo["temp_target"])
                        device.set_hvac_action(thermo["hvac_action"])
                        device.set_farhenheit(thermo["farhenheit"] == "true")

    async def listing(self):
        """List discovery of devices"""
        async with self._lock:
            res = await self._http_client.request("GET", "list_thermo")
            if not res.ok:
                return

            data = await res.json()
            for thermo in data:
                self._devices.append(
                    SeitronThermostat(
                        thermo["manuf"],
                        thermo["gMac"],
                        thermo["name"],
                        thermo["model"],
                        thermo["fw_Ver"],
                    )
                )
            return

    async def set_hvac_mode(self, gmac, mode):
        """Change mode of a thermostat"""
        async with self._lock:
            headers_dict = {}
            headers_dict["Content-Type"] = "application/json"
            json_request_body = {
                "gmac": gmac,
                "command": "SetThermostatMode",
                "mode": mode,
            }

            res = await self._http_client.request(
                "POST",
                "set_args",
                headers=headers_dict,
                json=json_request_body,
            )

    async def set_temperature(self, gmac, temp: float):
        """Change set point of a thermostat"""
        async with self._lock:
            headers_dict = {}
            headers_dict["Content-Type"] = "application/json"
            json_request_body = {
                "gmac": gmac,
                "command": "SetTargetTemperature",
                "temp_target": temp,
            }

            res = await self._http_client.request(
                "POST",
                "set_args",
                headers=headers_dict,
                json=json_request_body,
            )
