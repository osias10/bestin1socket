import time

import logging


_LOGGER = logging.getLogger(__name__)

delayTime = 0.5
maxDelayTime = 10

class ExecuteInfo():
    def __init__(self):
        self.statusList={}

    def checkTime(self, name):
        
        if name in self.statusList:
            nowTime = time.time()
            statusTime = self.statusList[name]["time"]
            if nowTime - statusTime < delayTime:
                return True
            else:
                return False
        else:
                return False
        #delayTime 대기 후 실행 ,maxDelayTime 넘길경우 fail
    def checkDiffTime(self, name):
        if name in self.statusList:
            nowTime = time.time()
            statusTime = self.statusList[name]["time"]
            if nowTime - statusTime > delayTime:
                return True
            else:
                return False
        else:
                return True
        
    def delayExecute(self, name):
        nowTime = time.time()
        startTime = nowTime
        beforeTime = nowTime
        if name in self.statusList:
            beforeTime = self.statusList[name]["time"]
            _LOGGER.critical(f"wait {nowTime} - {beforeTime} > {delayTime}, {maxDelayTime}")
            while nowTime - beforeTime < delayTime:
                if nowTime - startTime  > maxDelayTime:
                    return False
                nowTime = time.time()
                _LOGGER.critical(f"wait command: {name}")

                time.sleep(0.1)
            return True
        else:
            return True
    def addTime(self, name):
        unitStatus = {"time" : time.time()}
        self.statusList[name] = unitStatus
    def getAllTime(self):
        return self.statusList
    def getTimeName(self, name):
        return self.statusList[name]
    def removeTime(self, name):
        del self.statusList[name]
    