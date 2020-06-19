from itertools import groupby
import random
import numpy as np

def Attack(plan, toons, cogs):

    def getAccuracy(gag):
        track = gag.getTrack()
        target = gag.getTarget()
        # Special Cases
        if track == "trap" or (all([cog.isLured() for cog in targets]) and track in ["sound","throw","squirt"]):
            return 1
        if all([cog.isLured() for cog in targets]) and track == "drop":
            return 0

        if gag.isGroupAttack():
            targetLevel = max([cog.getLevel() for cog in cogs])
            targetHits = max([cog.getHits() for cog in cogs])
        elif gag.getTarget() is not None:
            targetLevel = target.getLevel()
            targetHits = target.getHits()
        else:
            targetLevel = 1
            targetHits = 0

        baseAccuracy = gag.getAccuracy()
        targetDefense = max(.02,.05*(targetLevel-1)) * int(track != "toon-up")
        lureRatio = sum([cog.isLured() for cog in cogs])/len(cogs) * int(track not in ["toon-up","lure","drop"])
        stunBonus = .2*targetHits

        return min(.95, baseAccuracy - targetDefense + lureRatio + stunBonus)

    def UseGags(gags):

        def ToonUp(gags):
            for gag in gags:
                if random.random() < getAccuracy(gag):
                    # Toon-up provides stun for ALL cogs
                    for cog in cogs:
                        cog.addHits(1)
                    if gag.isGroupAttack():
                        for toon in toons:
                            toon.Heal(np.ceil(gag.getValue()/len(toons)))
                    else:
                        gag.getTarget().Heal(gag.getValue())

        def Trap(gags):
            if len(gags)>1:
                groupTrap = any([gag.isGroupAttack() for gag in gags])
                if groupTrap:
                    print("All trap gags evaporated!")
                else:
                    # All traps are single attacks. Look for ones that conflict.
                    for cog in cogs:
                        gagsTargetingCog = [gag for gag in gags if cog is gag.getTarget()]
                        if len(gagsTargetingCog) == 1:
                            cog.addHits(1)
                            cog.setTrap(gagsTargetingCog[0])
                        else:
                            print("{} evaporated!".format(", ".join([gag.getName() for gag in gagsTargetingCog])))

        def Lure(gags):
            groupLure = any([gag.isGroupAttack() for gag in gags])
            for cog in cogs:
                gagsTargetingCog = [gag for gag in gags if cog is gag.getTarget()]
                if groupLure:
                    accuracy = max([getAccuracy(gag) for gag in gags])
                else:
                    accuracy = max([getAccuracy(gag) for gag in gagsTargetingCog])
                if random.random() < accuracy:
                    trap = cog.getTrap()
                    if trap:
                        cog.takeDamage(trap.getValue())
                        cog.setTrap(None)
                        cog.setLureRounds(0)
                    else:
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
                gagsTargetingCog = [gag for gag in gags if cog is gag.getTarget()]
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
                gagsTargetingCog = [gag for gag in gags if cog is gag.getTarget()]
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
