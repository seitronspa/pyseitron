""" A generic seitron thermostat"""

from .seitron_device import SeitronDevice


class SeitronThermostat(SeitronDevice):
    """A generic seitron thermostat"""

    def __init__(self, manuf, gmac, name, model, fw_ver) -> None:
        super().__init__(manuf, gmac, name, model, fw_ver)
        self._mode: str
        self._temp_curr: float
        self._temp_target: float
        self._hvac_action: str
        self._farhenheit = False

    @property
    def temp_target(self) -> float:
        """Thermostat setpoint"""
        return self._temp_target

    @property
    def mode(self) -> str:
        """Thermostat mode"""
        return self._mode

    @property
    def temp_curr(self) -> float:
        """Thermostat temp"""
        return self._temp_curr

    def set_temp_curr(self, temp: float) -> None:
        """Set new current temperature."""
        self._temp_curr = temp

    @property
    def hvac_action(self) -> str:
        """Thermostat boiler status"""
        return self._hvac_action

    def set_hvac_action(self, action: str) -> None:
        """Set new boiler status."""
        self._hvac_action = action

    @property
    def farhenheit(self) -> bool:
        """Thermostat unit in farhenheit"""
        return self._farhenheit

    def set_farhenheit(self, far: bool) -> None:
        """Set new farhenheit."""
        self._farhenheit = far

    def set_hvac_mode(self, hvac_mode: str) -> None:
        """Set new target hvac mode."""
        self._mode = hvac_mode

    def set_temperature(self, temp: float) -> None:
        """Set new target temperature."""
        self._temp_target = temp
