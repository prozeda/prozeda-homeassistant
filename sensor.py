"""
Prozeda Solar Controller Sensor Platform for Home Assistant
"""
import logging
import aiohttp
import async_timeout
import xml.etree.ElementTree as ET
from datetime import timedelta

import voluptuous as vol
from homeassistant.components.sensor import (
    PLATFORM_SCHEMA,
    SensorEntity,
    SensorDeviceClass,
    SensorStateClass,
)
from homeassistant.const import (
    CONF_HOST,
    CONF_NAME,
    CONF_SCAN_INTERVAL,
    UnitOfTemperature,
    UnitOfEnergy,
    UnitOfTime,
    PERCENTAGE,
)
from homeassistant.core import HomeAssistant
from homeassistant.helpers.aiohttp_client import async_get_clientsession
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.typing import ConfigType, DiscoveryInfoType
import homeassistant.helpers.config_validation as cv
from homeassistant.helpers.update_coordinator import (
    CoordinatorEntity,
    DataUpdateCoordinator,
    UpdateFailed,
)

_LOGGER = logging.getLogger(__name__)

DEFAULT_NAME = "Prozeda Solar Controller"
DEFAULT_SCAN_INTERVAL = timedelta(seconds=30)

PLATFORM_SCHEMA = PLATFORM_SCHEMA.extend(
    {
        vol.Required(CONF_HOST): cv.string,
        vol.Optional(CONF_NAME, default=DEFAULT_NAME): cv.string,
        vol.Optional(CONF_SCAN_INTERVAL, default=DEFAULT_SCAN_INTERVAL): cv.time_period,
        vol.Optional("device_type", default="auto"): vol.In(["auto", "primos_600sr", "primos_250sr"]),
    }
)

# Sensor definitions for different device types
SENSOR_DEFINITIONS = {
    "primos_600sr": [
        (1, "S1", UnitOfTemperature.CELSIUS, SensorDeviceClass.TEMPERATURE),
        (2, "S2", UnitOfTemperature.CELSIUS, SensorDeviceClass.TEMPERATURE),  
        (3, "S3", UnitOfTemperature.CELSIUS, SensorDeviceClass.TEMPERATURE),
        (4, "S4", UnitOfTemperature.CELSIUS, SensorDeviceClass.TEMPERATURE),
        (5, "S5", UnitOfTemperature.CELSIUS, SensorDeviceClass.TEMPERATURE),
        (6, "S6", UnitOfTemperature.CELSIUS, SensorDeviceClass.TEMPERATURE),
        (10, "R1", PERCENTAGE, None),
        (11, "R2", PERCENTAGE, None),
        (12, "R3", PERCENTAGE, None),  
        (13, "R0", PERCENTAGE, None),
        (14, "HE1", PERCENTAGE, None),
        (15, "HE2", PERCENTAGE, None),
        (17, "Energieertrag", UnitOfEnergy.KILO_WATT_HOUR, SensorDeviceClass.ENERGY),
        (18, "Energieertrag2", UnitOfEnergy.KILO_WATT_HOUR, SensorDeviceClass.ENERGY),
        (19, "Betriebsstunden", UnitOfTime.HOURS, SensorDeviceClass.DURATION),
        (20, "Betriebsstunden2", UnitOfTime.HOURS, SensorDeviceClass.DURATION),
    ],
    "primos_250sr": [
        (1, "S1", UnitOfTemperature.CELSIUS, SensorDeviceClass.TEMPERATURE),
        (2, "S2", UnitOfTemperature.CELSIUS, SensorDeviceClass.TEMPERATURE),  
        (3, "S3", UnitOfTemperature.CELSIUS, SensorDeviceClass.TEMPERATURE),
        (4, "S4", UnitOfTemperature.CELSIUS, SensorDeviceClass.TEMPERATURE),
        (7, "R1", PERCENTAGE, None),
        (10, "HE1", PERCENTAGE, None),
        (11, "R0", PERCENTAGE, None),
        (13, "Energieertrag", UnitOfEnergy.KILO_WATT_HOUR, SensorDeviceClass.ENERGY),
        (15, "Betriebsstunden", UnitOfTime.HOURS, SensorDeviceClass.DURATION),
    ],
}


class ProzedaDataUpdateCoordinator(DataUpdateCoordinator):
    """Class to manage fetching data from the Prozeda controller."""

    def __init__(self, hass: HomeAssistant, host: str, scan_interval: timedelta, device_type: str = "auto"):
        """Initialize."""
        self.host = host
        self.device_type = device_type
        self.detected_device_type = None
        self.session = async_get_clientsession(hass)
        super().__init__(hass, _LOGGER, name="prozeda", update_interval=scan_interval)

    async def _async_update_data(self):
        """Update data via library."""
        try:
            async with async_timeout.timeout(10):
                async with self.session.get(f"http://{self.host}/primos_val.xml") as response:
                    if response.status != 200:
                        raise UpdateFailed(f"Error communicating with API: {response.status}")
                    
                    xml_data = await response.text()
                    root = ET.fromstring(xml_data)
                    data_element = root.find("data")
                    
                    if data_element is None or data_element.text is None:
                        raise UpdateFailed("No data element found in XML")
                    
                    sensor_data = data_element.text
                    
                    # Auto-detect device type if not specified
                    if self.device_type == "auto":
                        self.detected_device_type = self._detect_device_type(sensor_data)
                        _LOGGER.info(f"Auto-detected device type: {self.detected_device_type}")
                    else:
                        self.detected_device_type = self.device_type
                    
                    return self._parse_sensor_data(sensor_data, self.detected_device_type)
                    
        except Exception as err:
            raise UpdateFailed(f"Error communicating with API: {err}")

    def _detect_device_type(self, sensor_data: str) -> str:
        """Auto-detect device type based on data signature."""
        if len(sensor_data) >= 42:
            signature = sensor_data[40:42]  # Position 41-42 (0-based indexing)
            if signature == "3B":
                return "primos_600sr"
            elif signature == "33":
                return "primos_250sr"
        
        _LOGGER.warning(f"Could not detect device type from signature. Using primos_600sr as default.")
        return "primos_600sr"

    def _get_offset_map(self, device_type: str) -> dict:
        """Get offset map for specific device type."""
        if device_type == "primos_600sr":
            return {
                1: 50,   # S1
                2: 54,   # S2  
                3: 58,   # S3
                4: 62,   # S4
                5: 66,   # S5
                6: 70,   # S6
                10: 86,  # R1
                11: 90,  # R2
                12: 94,  # R3
                13: 98,  # R0
                14: 102, # HE1
                15: 106, # HE2
                17: 114, # Energieertrag
                18: 118, # Energieertrag2
                19: 122, # Betriebsstunden
                20: 126, # Betriebsstunden2
            }
        elif device_type == "primos_250sr":
            return {
                1: 50,   # S1
                2: 54,   # S2  
                3: 58,   # S3
                4: 62,   # S4
                7: 74,   # R1
                10: 86,  # HE1
                11: 90,  # R0
                13: 98,  # Energieertrag
                15: 106, # Betriebsstunden
            }
        else:
            _LOGGER.error(f"Unknown device type: {device_type}")
            return {}

    def _parse_sensor_data(self, sensor_data: str, device_type: str) -> dict:
        """Parse the hex sensor data for specific device type."""
        sensor_values = {}
        offset_map = self._get_offset_map(device_type)
        sensor_definitions = SENSOR_DEFINITIONS.get(device_type, [])
        
        for pos, name, unit, device_class in sensor_definitions:
            offset = offset_map.get(pos)
            if offset is None:
                _LOGGER.warning(f"No offset defined for position {pos}")
                sensor_values[name] = None
                continue
                
            if offset + 4 <= len(sensor_data):
                value = sensor_data[offset:offset + 4]
                try:
                    value = int(value, 16)
                    # Apply scaling based on sensor type and device
                    if pos in [1, 2, 3, 4, 5, 6]:  # Temperature sensors
                        value = value / 10.0  # Divide by 10 for °C
                    elif pos in [7, 10, 11, 12, 13] and device_type == "primos_600sr":  # R1–R0 for 600SR
                        value = min(value / 2.0, 100.0)  # Divide by 2 for %, cap at 100%
                    elif pos in [7, 11] and device_type == "primos_250sr":  # R1, R0 for 250SR
                        value = min(value / 2.0, 100.0)  # Divide by 2 for %, cap at 100%
                    elif pos in [14, 15] and device_type == "primos_600sr":  # HE1–HE2 for 600SR
                        value = min(value / 100.0, 100.0)  # Divide by 100 for %, cap at 100%
                    elif pos in [10] and device_type == "primos_250sr":  # HE1 for 250SR
                        value = min(value / 100.0, 100.0)  # Divide by 100 for %, cap at 100%
                    elif pos in [17, 18, 13]:  # Energieertrag
                        pass  # Already in kWh
                    elif pos in [19, 20, 15]:  # Betriebsstunden
                        pass  # Already in hours
                    sensor_values[name] = value
                except ValueError:
                    _LOGGER.warning(f"Could not parse value for {name}: {value}")
                    sensor_values[name] = None
            else:
                _LOGGER.warning(f"Offset {offset} out of range for sensor {name}")
                sensor_values[name] = None
                
        return sensor_values


async def async_setup_platform(
    hass: HomeAssistant,
    config: ConfigType,
    async_add_entities: AddEntitiesCallback,
    discovery_info: DiscoveryInfoType | None = None,
) -> None:
    """Set up the sensor platform."""
    host = config[CONF_HOST]
    name = config[CONF_NAME]
    scan_interval = config[CONF_SCAN_INTERVAL]
    device_type = config.get("device_type", "auto")

    coordinator = ProzedaDataUpdateCoordinator(hass, host, scan_interval, device_type)
    
    # Fetch initial data so we have data when entities are added
    await coordinator.async_config_entry_first_refresh()
    
    # Get the detected device type after first refresh
    detected_type = coordinator.detected_device_type or "primos_600sr"
    sensor_definitions = SENSOR_DEFINITIONS.get(detected_type, [])

    entities = []
    for pos, sensor_name, unit, device_class in sensor_definitions:
        entities.append(
            ProzedaSensor(
                coordinator,
                name,
                sensor_name,
                unit,
                device_class,
                detected_type,
            )
        )

    async_add_entities(entities, update_before_add=True)


class ProzedaSensor(CoordinatorEntity, SensorEntity):
    """Representation of a Prozeda sensor."""

    def __init__(
        self,
        coordinator: ProzedaDataUpdateCoordinator,
        device_name: str,
        sensor_name: str,
        unit: str,
        device_class: SensorDeviceClass | None,
        device_type: str,
    ):
        """Initialize the sensor."""
        super().__init__(coordinator)
        self._device_name = device_name
        self._sensor_name = sensor_name
        self._unit = unit
        self._device_class = device_class
        self._device_type = device_type
        self._attr_unique_id = f"prozeda_{device_type}_{sensor_name.lower()}"
        self._attr_name = f"{device_name} {sensor_name}"

    @property
    def native_value(self):
        """Return the state of the sensor."""
        return self.coordinator.data.get(self._sensor_name)

    @property
    def native_unit_of_measurement(self):
        """Return the unit of measurement."""
        return self._unit

    @property
    def device_class(self):
        """Return the device class of the sensor."""
        return self._device_class

    @property
    def state_class(self):
        """Return the state class of the sensor."""
        if self._device_class in [SensorDeviceClass.ENERGY]:
            return SensorStateClass.TOTAL_INCREASING
        elif self._device_class in [SensorDeviceClass.TEMPERATURE, SensorDeviceClass.DURATION]:
            return SensorStateClass.MEASUREMENT
        return None

    @property
    def device_info(self):
        """Return device information."""
        return {
            "identifiers": {("prozeda", f"{self._device_type}_{self.coordinator.host}")},
            "name": f"{self._device_name} ({self._device_type.upper()})",
            "manufacturer": "Prozeda",
            "model": self._device_type.replace("_", " ").title(),
        }