import time

delayTime = 0.3
maxDelayTime = 3

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
    def delayExecute(self, name):
        if name in self.statusList:
            while 
            nowTime = time.time()
            statusTime = self.statusList[name]["time"]
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