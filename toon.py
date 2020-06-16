class Toon:
    def __init__(self, laff = 15, maxLaff = 15, gagPouch = None, gagPouchLimit = 80):
        self.laff = laff
        self.maxLaff = maxlaff
        self.gagPouch = gagPouch
        self.gagPouchLimit = gagPouchLimit

    def getLaff(self):
        return self.laff

    def getMaxLaff(self):
        return self.maxLaff

    def getGags(self):
        return self.gagPouch

    def getNumberOfGags(self):
        return len(self.gagPouch)

    def getGagPouchLimit(self):
        return self.gagPouchLimit

    def setGagPouchLimit(self, limit):
        self.gagPouchLimit = max(limit, getNumberOfGags)

    def addGag(self,gag):
        if getNumberOfGags() < getGagPouchLimit():
            self.gagPouch.append(gag)

    def setLaff(self, laff):
        self.laff = max(0,min(laff,getMaxLaff()))

    def setMaxLaff(self, laff):
        self.maxLaff = max(1,laff)
        setLaff(laff)

    def Heal(self, laff):
        setLaff(getLaff()+laff)

    def Hurt(self, laff):
        setLaff(getLaff()-laff)
