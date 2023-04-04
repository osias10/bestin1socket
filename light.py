from __future__ import annotations

import logging

import voluptuous as vol
from homeassistant import const

import homeassistant.helpers.config_validation as cv

from homeassistant.components.light import (PLATFORM_SCHEMA,
                                            LightEntity)
from . import bestin

_LOGGER = logging.getLogger(__name__)

CONF_WALLPAD_IP = "wallpad_ip"
CONF_SERVER_IP = "server_ip"
CONF_SERVER_PORT = "server_port"


PLATFORM_SCHEMA = PLATFORM_SCHEMA.extend({
    vol.Required(CONF_WALLPAD_IP): cv.string,
    vol.Required(CONF_SERVER_IP): cv.string,
    vol.Required(CONF_SERVER_PORT): cv.positive_int,
    vol.Required('rooms'): cv.string,
    vol.Optional('enable_lights', default=True): cv.boolean,
})

def setup_platform(
    hass: HomeAssistant,
    config: ConfigType,
    add_entities: AddEntitiesCallback,
    discovery_info: DiscoveryInfoType | None = None
) -> None:
    """Set up the bestin Light platform."""
    serverIp = config[CONF_SERVER_IP]
    serverPort = config[CONF_SERVER_PORT]
    wallpadIp = config.get(CONF_WALLPAD_IP)
    

    lights = []
    for room in config['rooms'].split():
        light = BestinLight(serverIp, serverPort, wallpadIp, room)
        lights.append(light)
    add_entities(lights)

class BestinLight(LightEntity):
    def __init__(self,serverIp, serverPort, wallpadIp, room) -> None:
        self._room = room
        self._btcp = bestin.Bestin(serverIp, serverPort, wallpadIp)
        self._name = f"BESTIN_LIGHT_{self._room}"
        #self.coordinator = coordinator
    @property
    def unique_id(self):
        """Return unique ID."""
        return self._name
    @property
    def name(self) -> str:
        """BESTINLIGHT"""
        return self._name
    
    @property
    def is_on(self):
        res = self._btcp.XMLRequest("remote_access_light", "status", self._room, "switch1", "")
        return True
    
    def turn_on(self):
        res = self._btcp.XMLRequest("remote_access_light", "control", self._room, "switch1", "on")
        _LOGGER.debug(res)
    
    def turn_off(self):
        res = self._btcp.XMLRequest("remote_access_light", "control", self._room, "switch1", "off")
    
    @property
    def should_poll(self):
        """No polling needed."""
        return False

