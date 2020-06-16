from itertools import groupby
import random
import numpy as np

def Attack(plan, toons, cogs):

    def getAccuracy(gag):
        track = gag.getTrack()
        targets = gag.getTargets()
        # Special Cases
        if track == "trap" or (all([cog.isLured() for cog in targets]) and track in ["sound","throw","squirt"]):
            return 1
        if all([cog.isLured() for cog in targets]) and track == "drop":
            return 0
        baseAccuracy = gag.getAccuracy()
        targetDefense = max(.02,.05*(max([cog.getLevel() for cog in targets])-1)) * int(track != "toon-up")
        lureRatio = sum([cog.isLured() for cog in cogs])/len(cogs) * int(track not in ["toon-up","lure","drop"])
        stunBonus = .2*max([cog.getHits() for cog in targets])
        return min(.95, baseAccuracy - targetDefense + lureRatio + stunBonus)

    def UseGags(gags):

        def ToonUp(gags):
            for gag in gags:
                if random.random() < getAccuracy(gag):
                    for cog in cogs:
                        cog.addHits(1)
                    if gag.multiTarget():
                        for target in gag.getTargets():
                            target.Heal(np.ceil(gag.getValue()/len(toons)))
                    else:
                        gag.getTargets()[0].Heal(gag.getValue())

        def Trap(gags):
            if len(gags)>1:
                groupTrap = sum([gag.multiTarget() for gag in gags]) > 0
                if groupTrap:
                    print("All trap gags evaporated!")
                else:
                    for cog in cogs:
                        gagsTargetingCog = [gag for gag in gags if cog in gag.getTargets()]
                        if len(gagsTargetingCog) == 1:
                            cog.addHits(1)
                            gagsTargetingCog[0].setTargets(None)
                            cog.setTrap(gagsTargetingCog[0])
                        else:
                            print("{} evaporated!".format(", ".join([gag.getName() for gag in gagsTargetingCog])))

        def Lure(gags):
            groupLure = sum([gag.multiTarget() for gag in gags]) > 0
            if groupLure:
                accuracy = max([getAccuracy(gag) for gag in gags])
                if random.random() < accuracy:
                    for gag in gags:
                        for target in gag.getTargets():
                            target.addLureRounds(gag.getValue())
            else:
                for cog in cogs:
                    gagsTargetingCog = [gag for gag in gags if cog in gag.getTargets()]
                    accuracy = max([getAccuracy(gag) for gag in gagsTargetingCog])
                    if random.random() < accuracy:
                        cog.addLureRounds(sum([gag.getValue() for gag in gagsTargetingCog]))

        def Sound(gags):
            accuracy = max([getAccuracy(gag) for gag in gags])
            if random.random() < accuracy:
                damage = sum([gag.getValue() for gag in gags])
                combo = int(.2*damage)*int(len(gags)>1)
                for cog in cogs:
                    cog.takeDamage(damage + combo)

        def Throw(gags):
            for cog in cogs:
                gagsTargetingCog = [gag for gag in gags if cog in gag.getTargets()]
                accuracy = max([getAccuracy(gag) for gag in gagsTargetingCog])
                if random.random() < accuracy:
                    damage = sum([gag.getValue() for gag in gagsTargetingCog])
                    knockback = int(.5*damage)*int(cog.isLured())
                    combo = int(.2*damage)*int(len(gagsTargetingCog)>1)
                    cog.takeDamage(damage + knockback + combo)

        def Squirt(gags):
            Throw(gags)

        def Drop(gags):
            for cog in cogs:
                if cog.isLured():
                    continue
                gagsTargetingCog = [gag for gag in gags if cog in gag.getTargets()]
                accuracy = max([getAccuracy(gag) for gag in gagsTargetingCog])
                if random.random() < accuracy:
                    damage = sum([gag.getValue() for gag in gagsTargetingCog])
                    combo = int(.2*damage)*int(len(gagsTargetingCog)>1)
                    cog.takeDamage(damage + combo)

        attacks = {
            "toon-up": ToonUp,
            "trap": Trap,
            "lure": Lure,
            "sound": Sound,
            "throw": Throw,
            "squirt": Squirt,
            "drop": Drop
        }
        attacks[gags[0].getTrack()](gags)


    gagsByTrack = [list(group[0]) for group in groupby(plan, lambda gag: gag.getTrack())]
    for gags in gagsByTrack:
        UseGags(gags)
