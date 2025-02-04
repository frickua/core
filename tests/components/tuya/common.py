"""Test code shared between test files."""

from tuya_sharing import CustomerDevice, DeviceFunction, DeviceStatusRange
from tuyaha.devices import climate, light, switch

from homeassistant.components.tuya import DOMAIN

from tests.common import load_json_object_fixture

CLIMATE_ID = "1"
CLIMATE_DATA = {
    "data": {"state": "true", "temp_unit": climate.UNIT_CELSIUS},
    "id": CLIMATE_ID,
    "ha_type": "climate",
    "name": "TestClimate",
    "dev_type": "climate",
}

LIGHT_ID = "2"
LIGHT_DATA = {
    "data": {"state": "true"},
    "id": LIGHT_ID,
    "ha_type": "light",
    "name": "TestLight",
    "dev_type": "light",
}

SWITCH_ID = "3"
SWITCH_DATA = {
    "data": {"state": True},
    "id": SWITCH_ID,
    "ha_type": "switch",
    "name": "TestSwitch",
    "dev_type": "switch",
}

LIGHT_ID_FAKE1 = "9998"
LIGHT_DATA_FAKE1 = {
    "data": {"state": "true"},
    "id": LIGHT_ID_FAKE1,
    "ha_type": "light",
    "name": "TestLightFake1",
    "dev_type": "light",
}

LIGHT_ID_FAKE2 = "9999"
LIGHT_DATA_FAKE2 = {
    "data": {"state": "true"},
    "id": LIGHT_ID_FAKE2,
    "ha_type": "light",
    "name": "TestLightFake2",
    "dev_type": "light",
}

TUYA_DEVICES = [
    climate.TuyaClimate(CLIMATE_DATA, None),
    light.TuyaLight(LIGHT_DATA, None),
    switch.TuyaSwitch(SWITCH_DATA, None),
    light.TuyaLight(LIGHT_DATA_FAKE1, None),
    light.TuyaLight(LIGHT_DATA_FAKE2, None),
]


async def load_device_from_json(filename: str) -> CustomerDevice:
    """Load json from file and cast it to CustomerDevice with correct functions and status_range."""
    device = CustomerDevice(**load_json_object_fixture(filename, DOMAIN))
    device.function = {k: DeviceFunction(**v) for k, v in device.function.items()}
    device.status_range = {
        k: DeviceStatusRange(**v) for k, v in device.status_range.items()
    }
    return device


class MockTuya:
    """Mock for Tuya devices."""

    def get_all_devices(self):
        """Return all configured devices."""
        return TUYA_DEVICES

    def get_device_by_id(self, dev_id):
        """Return configured device with dev id."""
        if dev_id == LIGHT_ID_FAKE1:
            return None
        if dev_id == LIGHT_ID_FAKE2:
            return switch.TuyaSwitch(SWITCH_DATA, None)
        for device in TUYA_DEVICES:
            if device.object_id() == dev_id:
                return device
        return None
