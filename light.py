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
CONF_WALLPAD_PORT = "wallpad_port"
CONF_SERVER_IP = "server_ip"
CONF_SERVER_PORT = "server_port"


PLATFORM_SCHEMA = PLATFORM_SCHEMA.extend({
    vol.Required(CONF_WALLPAD_IP): cv.string,
    vol.Required(CONF_SERVER_IP): cv.string,
    vol.Required(CONF_SERVER_PORT): cv.positive_int,
    vol.Required(CONF_WALLPAD_PORT): cv.positive_int,
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
    wallpadPort = config.get(CONF_WALLPAD_PORT)

    lights = []
    for room in config['rooms'].split():
        light = BestinLight(serverIp, serverPort, wallpadIp, wallpadPort, room, "")
        lightReq = light._btcp.XMLRequest("remote_access_light", "status", room, "", "")
        lightRes = light._btcp.requestToWallpad(lightReq)
        lightResult = light._btcp.ParseXMLResponse(lightRes)
        if lightResult != False :
            
            if (isinstance(lightResult,list)) :
                for lt in lightResult:
                    light = BestinLight(serverIp, serverPort, wallpadIp, wallpadPort, room, lt['@unit_num'])
                    lights.append(light)
            else :
                light = BestinLight(serverIp, serverPort, wallpadIp, wallpadPort, room, lightResult['@unit_num'])
                lights.append(light)

    add_entities(lights)

class BestinLight(LightEntity):
    def __init__(self,serverIp, serverPort, wallpadIp, wallpadPort, room, switch) -> None:
        self._room = room
        self._btcp = bestin.Bestin(serverIp, serverPort, wallpadIp, wallpadPort)
        self._switch = switch
        self._name = f"BESTIN_LIGHT_room{self._room}_{self._switch}"

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
        req = self._btcp.XMLRequest("remote_access_light", "status", self._room, self._switch, "")
        res = self._btcp.requestToWallpad(req)
        result = self._btcp.ParseXMLResponse(res)

        if (isinstance(result,list)):
            status = next((item for item in result if item['@unit_num'] == self._switch), False)
        else :
            status = result
        return self._btcp.CheckUnitStatus(status)
    
    def turn_on(self):
        req = self._btcp.XMLRequest("remote_access_light", "control", self._room, self._switch, "on")
        res = self._btcp.requestToWallpad(req)
        result = self._btcp.ParseXMLResponse(res)
        return self._btcp.CheckUnitStatus(result)
    
    def turn_off(self):
        req = self._btcp.XMLRequest("remote_access_light", "control", self._room, self._switch, "off")
        res = self._btcp.requestToWallpad(req)
        result = self._btcp.ParseXMLResponse(res)
        return self._btcp.CheckUnitStatus(result)

    # @property
    # def should_poll(self):
    #     """No polling needed."""
    #     return False

