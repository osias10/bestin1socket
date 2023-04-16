import time

delayTime=5

class StatusInfo():
    def __init__(self):
        self.statusList={}

    def checkStatus(self, name):
        
        if name in self.statusList:
            nowTime = time.time()
            statusTime = self.statusList[name]["time"]
            if nowTime - statusTime < delayTime:
                return True
            else:
                return False
        else:
                return False
    def getStatus(self, name):
        return (self.statusList[name]["status"])
    def addStatus(self, name, status):
        unitStatus = {"status" : status, "time" : time.time()}
        self.statusList[name] = unitStatus
    def getAllStatus(self):
        return self.statusList
    def removeStatus(self, name):
        del self.statusList[name]