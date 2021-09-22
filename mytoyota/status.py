"""Vehicle status representation for mytoyota"""
import logging
from typing import Optional, Union

from mytoyota.const import DOORS, HOOD, KEY, LIGHTS, WINDOWS
from mytoyota.sensors import Doors, Hood, Key, Lights, Windows

_LOGGER: logging.Logger = logging.getLogger(__package__)


class Odometer:
    """Odometer representation"""

    mileage: int = None
    unit: str = None

    def __init__(self, data: dict) -> None:
        self.mileage = data.get("mileage", None)
        self.unit = data.get("mileage_unit", None)

    def __str__(self) -> str:
        return str(self.as_dict())

    def as_dict(self) -> dict:
        """Return odometer as dict."""
        return vars(self)


class Sensors:
    """Vehicle sensors representation"""

    lights: Optional[Lights] = None
    hood: Optional[Hood] = None
    doors: Optional[Doors] = None
    windows: Optional[Windows] = None
    key: Optional[Key] = None

    overallstatus: str = None
    last_updated: str = None

    def __init__(self, status: dict):

        _LOGGER.debug("Raw sensor data: %s", str(status))

        self.overallstatus = status.get("overallStatus", None)
        self.last_updated = status.get("timestamp", None)

        self.lights = Lights(status[LIGHTS]) if LIGHTS in status else None
        self.hood = Hood(status[HOOD]) if HOOD in status else None
        self.doors = Doors(status[DOORS]) if DOORS in status else None
        self.windows = Windows(status[WINDOWS]) if WINDOWS in status else None
        self.key = Key(status[KEY]) if KEY in status else None

    def __str__(self) -> str:
        return str(self.as_dict())

    def as_dict(self) -> dict:
        """Return as dict."""
        return {
            "overallstatus": self.overallstatus,
            "lights": self.lights.as_dict() if self.lights is not None else None,
            "hood": self.hood.as_dict() if self.hood is not None else None,
            "doors": self.doors.as_dict() if self.doors is not None else None,
            "windows": self.windows.as_dict() if self.windows is not None else None,
            "key": self.key.as_dict() if self.key is not None else None,
            "last_updated": self.last_updated,
        }


class Energy:
    """Represents fuel level, battery capacity and range"""

    level: Optional[int] = None
    range: Optional[int] = None
    type: str = None
    last_updated: Optional[str] = None

    def __init__(self, data: Union[list, dict] = None, legacy: bool = False):

        # Support for old endpoint for fuel level. Some cars still uses this.
        if legacy:
            self.level = data.get("Fuel", None)
            self.range = None
            self.last_updated = None

        else:
            self.level = data[0].get("level", None)
            self.range = data[0].get("remainingRange", None)
            self.type = data[0].get("type", "Unknown").capitalize()
            self.last_updated = data[0].get("timestamp", None)

    def __str__(self) -> str:
        return str(self.as_dict())

    def as_dict(self) -> dict:
        """Return odometer as dict."""
        return vars(self)
