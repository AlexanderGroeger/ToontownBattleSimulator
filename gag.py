class Gag:
    def __init__(self, name = "", track = None,
        value = 0, accuracy = 0, hitsAll = False,
        targets = None, organic = False, toon = None):
        self.name = name
        self.track = track
        self.value = value
        self.accuracy = accuracy
        self.hitsAll = hitsAll
        self.target = targets
        self.organic = organic
        self.toon = toon

    def __str__(self):
        return str(self.__dict__)
        # return ", ".join([str(obj) for obj in [self.getName(),self.getTrack(),self.getValue(),self.getAccuracy(),self.isGroupAttack()]])

    def getName(self):
        return self.name

    def getTrack(self):
        return self.track

    def getValue(self):
        return self.value + max(1,int(.1*self.value)) * int(self.isOrganic())

    def getAccuracy(self):
        return self.accuracy

    def getTarget(self):
        return self.target

    def isOrganic(self):
        return self.organic

    def getToon(self):
        return self.toon

    def isGroupAttack(self):
        return self.hitsAll

    def setName(self, name):
        self.name = name

    def setTarget(self, target = None):
        self.target = target

    def setOrganic(self, organic = True):
        self.organic = organic

    def setToon(self, toon = None):
        self.toon = toon
