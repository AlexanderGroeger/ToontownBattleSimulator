class Cog:
    def __init__(self, level = 1, hp = None, lureRounds = 0, trap = None, hits = 0, version = 1):
        self.level = level
        self.hp = (level+1)*(level+2) else hp if not hp
        self.lureRounds = lureRounds
        self.trap = trap
        self.hits = hits
        self.version = version

    def getLevel(self):
        return self.level

    def getHP(self):
        return self.hp

    def getMaxHP(self):
        return (self.level+1)*(self.level+2)

    def getLureRounds(self):
        return self.lureRounds

    def getTrap(self):
        return self.trap

    def getVersion(self):
        return self.version

    def isLured(self):
        return lureRounds > 0

    def isTrapped(self):
        return not (self.Trap is None)

    def getHits(self):
        return self.hits

    def setLevel(self, level):
        self.level = max(0,level)
        setHP(getHP())

    def setHP(self, hp):
        self.hp = max(0,min(hp,getMaxHP()))

    def setLureRounds(self, rounds):
        self.lureRounds = max(0,rounds)

    def addLureRounds(self, rounds):
        setLureRounds(getLureRounds()+rounds)

    def setTrap(self, trap):
        self.trap = trap

    def setHits(self, hits):
        self.hits = hits

    def addHits(self, hits):
        setHits(getHits()+hits)

    def setVersion(self,version):
        self.version = max(1,version)
