# SPDX-License-Identifier: MIT
# custom_components/iotopen/sensor.py

"""Sensor platform for IoT Open."""

from __future__ import annotations

from typing import Any

import logging

from homeassistant.components.sensor import (
    SensorEntity,
    SensorDeviceClass,
    SensorStateClass,
)
from homeassistant.config_entries import ConfigEntry
from homeassistant.const import ATTR_ATTRIBUTION
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity import DeviceInfo
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.update_coordinator import CoordinatorEntity

from .const import DOMAIN
from .coordinator import (
    IoTOpenDataUpdateCoordinator,
    IoTOpenFunctionState,
    is_binary_function,
)

_LOGGER = logging.getLogger(__name__)

ATTRIBUTION = "Data via IoT Open"


async def async_setup_entry(
    hass: HomeAssistant,
    entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Set up IoT Open sensors for a config entry."""
    coordinator: IoTOpenDataUpdateCoordinator = hass.data[DOMAIN][entry.entry_id][
        "coordinator"
    ]

    entities: list[IoTOpenFunctionSensor] = []

    for state in coordinator.data.values():
        # Binary-style functions are handled by binary_sensor.py
        if is_binary_function(state):
            continue

        entities.append(
            IoTOpenFunctionSensor(
                coordinator=coordinator,
                function_id=state.function_id,
                entry_id=entry.entry_id,
            )
        )

    async_add_entities(entities)


class IoTOpenFunctionSensor(
    CoordinatorEntity[IoTOpenDataUpdateCoordinator],
    SensorEntity,
):
    """Sensor representing one IoT Open FunctionX (non-binary)."""

    _attr_has_entity_name = True

    def __init__(
        self,
        *,
        coordinator: IoTOpenDataUpdateCoordinator,
        function_id: int,
        entry_id: str,
    ) -> None:
        super().__init__(coordinator)
        self._function_id = function_id
        self._entry_id = entry_id

        state = self._get_state()
        assert state is not None

        self._attr_unique_id = (
            f"iotopen_{state.installation_id}_func_{state.function_id}"
        )
        self._attr_name = state.name

        # Guess metadata from type/name/meta
        dev_class, unit, state_class = _guess_sensor_characteristics(state)
        self._attr_device_class = dev_class
        self._attr_native_unit_of_measurement = unit
        self._attr_state_class = state_class

    def _get_state(self) -> IoTOpenFunctionState | None:
        return self.coordinator.data.get(self._function_id)

    @property
    def native_value(self) -> Any:
        state = self._get_state()
        return None if state is None else state.last_value

    @property
    def extra_state_attributes(self) -> dict[str, Any]:
        state = self._get_state()
        if state is None:
            return {ATTR_ATTRIBUTION: ATTRIBUTION}

        return {
            ATTR_ATTRIBUTION: ATTRIBUTION,
            "installation_id": state.installation_id,
            "function_id": state.function_id,
            "type": state.type,
            "topic_read": state.topic_read,
            "last_timestamp": state.last_timestamp,
            "device_id": state.device_id,
        }

    @property
    def device_info(self) -> DeviceInfo:
        """Group functions either under DeviceX or under the installation."""
        state = self._get_state()
        if state is None:
            return DeviceInfo(
                identifiers={(DOMAIN, "installation_unknown")},
                name="IoT Open Installation",
                manufacturer="IoT Open",
                model="Lynx",
            )

        if state.device_id is not None:
            identifier = f"device_{state.device_id}"
            name = f"IoT Open Device {state.device_id}"
        else:
            identifier = f"installation_{state.installation_id}"
            name = f"IoT Open Installation {state.installation_id}"

        return DeviceInfo(
            identifiers={(DOMAIN, identifier)},
            name=name,
            manufacturer="IoT Open",
            model="Lynx",
        )

    @property
    def available(self) -> bool:
        """Entity is available if coordinator has state for this function."""
        return self._get_state() is not None


def _guess_sensor_characteristics(
    state: IoTOpenFunctionState,
) -> tuple[SensorDeviceClass | None, str | None, SensorStateClass | None]:
    """Infer device_class, unit and state_class from type/name/meta."""
    meta = state.meta or {}
    t = state.type.lower()
    name = state.name.lower()
    unit = str(meta.get("unit") or meta.get(
        "unit_of_measurement") or "").strip()

    dev_class: SensorDeviceClass | None = None
    state_class: SensorStateClass | None = None

    if "temp" in t or "temp" in name:
        dev_class = SensorDeviceClass.TEMPERATURE
        if not unit:
            unit = "°C"
        state_class = SensorStateClass.MEASUREMENT
    elif "humidity" in t or "humidity" in name:
        dev_class = SensorDeviceClass.HUMIDITY
        if not unit:
            unit = "%"
        state_class = SensorStateClass.MEASUREMENT
    elif "power" in t or "watt" in unit.lower():
        dev_class = SensorDeviceClass.POWER
        if not unit:
            unit = "W"
        state_class = SensorStateClass.MEASUREMENT
    elif "energy" in t or unit.lower() in ("kwh", "wh"):
        dev_class = SensorDeviceClass.ENERGY
        state_class = SensorStateClass.TOTAL_INCREASING

    if not unit:
        unit = None

    return dev_class, unit, state_class
