import threading
import time
import queue
from . import statusinfo
from . import executeinfo
import logging


_LOGGER = logging.getLogger(__name__)

class RequestQueue(threading.Thread):
    """클래스 생성시 threading.Thread를 상속받아 만들면 된다"""
    queueDelay = 0.3
    sleepTime = 0.1
    ExecuteInfo = executeinfo.ExecuteInfo()
    maxDelay = 5
    def __init__(self,statusInfo):
        """__init__ 메소드 안에서 threading.Thread를 init한다"""
        threading.Thread.__init__(self)
        self.commandQueue = queue.Queue()
        self.statusInfo = statusInfo


    def run(self):
        while True:
            if (self.commandQueue.qsize() > 0):
                req = self.commandQueue.get()
                #_LOGGER.critical(f"queue get: {req}")
                
                if self.ExecuteInfo.checkDiffTime(req["roomName"]):
                    
                    if req["request"] == "turnOn":
                        self.turnOn(req)
                    elif req["request"] == "turnOff":
                        self.turnOff(req)
                    self.ExecuteInfo.addTime(req["roomName"])
                elif time.time() - req["time"] > self.maxDelay:
                    _LOGGER.critical(f"Drop Queue: {req}")
                else :
                    self.commandQueue.put(req)
                    #_LOGGER.critical(f"queue put: {req}")
                #time.sleep(RequestQueue.queueDelay)
            else :
                #_LOGGER.critical("no Queee")
                time.sleep(RequestQueue.sleepTime)
    def addCommand(self, req):
        self.commandQueue.put(req)
    def turnOn(self, req):
        dic = req["request"]
        entity = req["lightClass"]
        arguments = req["arguments"]
        
        req = entity._btcp.XMLRequest(arguments["reqname"], arguments["action"], arguments["dev_num"], arguments["unit_num"], arguments["ctrl_action"])
        res = entity._btcp.requestToWallpad(req)
        result = entity._btcp.ParseXMLResponse(res)

        self.UpdateStatus(entity, result)
        _LOGGER.debug(f"statusInfo(turnOn): {self.statusInfo.getStatusName(entity._name)}")


    def turnOff(self, req):
        dic = req["request"]
        entity = req["lightClass"]
        arguments = req["arguments"]

        req = entity._btcp.XMLRequest(arguments["reqname"], arguments["action"], arguments["dev_num"], arguments["unit_num"], arguments["ctrl_action"])
        res = entity._btcp.requestToWallpad(req)
        result = entity._btcp.ParseXMLResponse(res)

        self.UpdateStatus(entity, result)
        _LOGGER.debug(f"statusInfo(turnOff): {self.statusInfo.getStatusName(entity._name)}")

    def UpdateStatus(self, entity, parseRes):
        if parseRes != False:
            if isinstance(parseRes,list):
                for st in parseRes :
                    switchNum = st['@unit_num']
                    self.statusInfo.addStatus(f"{entity._roomName}_{switchNum}", entity._btcp.CheckUnitStatus(st))
                    _LOGGER.debug(f"UpdateSTatus {entity._roomName}_{switchNum}:{self.statusInfo.getStatusName(entity._name)}")
                result = self.statusInfo.getStatus(entity._name)
            else:
                switchNum = parseRes['@unit_num']
                self.statusInfo.addStatus(f"{entity._name}", entity._btcp.CheckUnitStatus(parseRes))
                #_LOGGER.critical(f"{self._roomName}_{switchNum}:{StatusInfo.getStatus(statusKey)}")
                result = self.statusInfo.getStatus(entity._name)
        else :
            _LOGGER.critical(f"fail UpdateStatus")
            result = False
        


