class Gag:
    def __init__(self,name = "", track = None,value = 0,accuracy = 0,targets = [], organic = False):
        self.name = name
        self.track = track
        self.value = value
        self.accuracy = accuracy
        self.targets = targets
        self.organic = organic

    def getName(self):
        return self.name

    def getTrack(self):
        return self.track

    def getValue(self):
        return self.value + max(1,int(.1*self.value)) * int(isOrganic())

    def getAccuracy(self):
        return self.accuracy

    def getTargets(self):
        return self.targets

    def isOrganic(self):
        return self.organic

    def multiTarget(self):
        return len(getTargets())>1

    def setName(self, name):
        self.name = name

    def setTargets(self, targets = []):
        self.targets = targets

    def setOrganic(self, organic = True):
        self.organic = organic
