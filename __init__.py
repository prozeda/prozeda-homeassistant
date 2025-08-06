"""
Prozeda Solar Controller integration for Home Assistant.
"""
from __future__ import annotations

from homeassistant.core import HomeAssistant
from homeassistant.helpers.typing import ConfigType

DOMAIN = "prozeda"


async def async_setup(hass: HomeAssistant, config: ConfigType) -> bool:
    """Set up the Prozeda integration."""
    return True