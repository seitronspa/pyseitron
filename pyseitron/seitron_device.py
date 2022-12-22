"""A generic Seitron device"""


class SeitronDevice:
    """A generic Seitron device"""

    def __init__(self, manuf, gmac, name, model, fw_ver) -> None:
        self._manuf = manuf
        self._gmac = gmac
        self._name = name
        self._model = model
        self._fw_ver = fw_ver

    @property
    def manufacturer(self) -> str:
        """Device manufacturer"""
        return self._manuf

    @property
    def gmac(self) -> str:
        """Device gmac"""
        return self._gmac

    @property
    def name(self) -> str:
        """Device name"""
        return self._name

    @property
    def model(self) -> str:
        """Device model"""
        return self._model

    @property
    def fw_ver(self) -> str:
        """Device fw version"""
        return self._fw_ver
