from itertools import groupby
import random
import numpy as np

def Attack(plan, toons, cogs):

    def getAccuracy(gag):
        track = gag.getTrack()
        target = gag.getTarget()
        # Special Cases
        if track == "trap":
            return 1
        elif track in ["sound","throw","squirt"]:
            if all([cog.isLured() for cog in cogs]):
                return 1
            elif not gag.isGroupAttack() and target.isLured():
                return 1
        if track == "drop":
            if all([cog.isLured() for cog in cogs]):
                return 0
            elif not gag.isGroupAttack() and target.isLured():
                return 0

        if gag.isGroupAttack():
            targetLevel = max([cog.getLevel() for cog in cogs])
            targetHits = max([cog.getHits() for cog in cogs])
        elif target is not None:
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

    def UseGags(gags, track):

        def ToonUp(gags):
            for gag in gags:
                if random.random() < getAccuracy(gag):
                    print("{} hit and is healing {} laff".format(gag.getName(),str(gag.getValue())))
                    # Toon-up provides stun for ALL cogs
                    for cog in cogs:
                        cog.addHits(1)
                    if gag.isGroupAttack():
                        for toon in toons:
                            toon.Heal(np.ceil(gag.getValue()/len(toons)))
                    else:
                        gag.getTarget().Heal(gag.getValue())
                else:
                    print("{} missed and is healing {} laff".format(gag.getName(),str(np.ceil(.2*gag.getValue()))))
                    if gag.isGroupAttack():
                        for toon in toons:
                            toon.Heal(np.ceil(.2*gag.getValue()/len(toons)))
                    else:
                        gag.getTarget().Heal(.2*gag.getValue())

        def Trap(gags):
            if len(gags)>1:
                groupTrap = any([gag.isGroupAttack() for gag in gags])
                if groupTrap:
                    print("All trap gags evaporated!")
                else:
                    # All traps are single attacks. Look for ones that conflict.
                    for cog in cogs:
                        gagsTargetingCog = [gag for gag in gags if cog is gag.getTarget()]
                        if len(gagsTargetingCog) == 0:
                            continue
                        if len(gagsTargetingCog) == 1:
                            cog.addHits(1)
                            cog.setTrap(gagsTargetingCog[0])
                        else:
                            print("{} evaporated!".format(", ".join([gag.getName() for gag in gagsTargetingCog])))

        def Lure(gags):
            groupLure = any([gag.isGroupAttack() for gag in gags])
            for cog in cogs:
                gagsTargetingCog = [gag for gag in gags if cog is gag.getTarget()]
                if len(gagsTargetingCog) == 0:
                    continue
                if groupLure:
                    accuracy = max([getAccuracy(gag) for gag in gags])
                else:
                    accuracy = max([getAccuracy(gag) for gag in gagsTargetingCog])
                if random.random() < accuracy:
                    print("{} hit and is luring a level {} cog".format(gag.getName(),str(cog.getLevel())))
                    trap = cog.getTrap()
                    if trap:
                        print("{} is being activated on a level {} cog".format(trap.getName(),str(cog.getLevel())))
                        cog.takeDamage(trap.getValue())
                        cog.setTrap(None)
                        cog.setLureRounds(0)
                    else:
                        cog.addLureRounds(sum([gag.getValue() for gag in gagsTargetingCog]))
                else:
                    print("{} missed!".format(gag.getName()))

        def Sound(gags):
            accuracy = max([getAccuracy(gag) for gag in gags])
            if random.random() < accuracy:
                print("Sound hit all the cogs")
                damage = sum([gag.getValue() for gag in gags])
                combo = np.ceil(.2*damage)*int(len(gags)>1)
                print("The cogs took a total of {} sound damage".format(str(damage+combo)))
                for cog in cogs:
                    cog.takeDamage(damage + combo)
            else:
                print("Sound missed!")

        def Throw(gags):
            for cog in cogs:
                gagsTargetingCog = [gag for gag in gags if cog is gag.getTarget()]
                if len(gagsTargetingCog) == 0:
                    continue
                accuracy = max([getAccuracy(gag) for gag in gagsTargetingCog])
                if random.random() < accuracy:
                    damage = sum([gag.getValue() for gag in gagsTargetingCog])
                    knockback = np.ceil(.5*damage) * int(cog.isLured())
                    combo = np.ceil(.2*damage) * int(len(gagsTargetingCog)>1)
                    cog.takeDamage(damage + knockback + combo)
                else:
                    print("Throw/Squirt missed!")

        def Squirt(gags):
            Throw(gags)

        def Drop(gags):
            for cog in cogs:
                if cog.isLured():
                    continue
                gagsTargetingCog = [gag for gag in gags if cog is gag.getTarget()]
                if len(gagsTargetingCog) == 0:
                    continue
                accuracy = max([getAccuracy(gag) for gag in gagsTargetingCog])
                if random.random() < accuracy:
                    damage = sum([gag.getValue() for gag in gagsTargetingCog])
                    combo = int(.2*damage) * int(len(gagsTargetingCog)>1)
                    cog.takeDamage(damage + combo)
                else:
                    print("Drop missed!")

        attacks = {
            "toon-up": ToonUp,
            "trap": Trap,
            "lure": Lure,
            "sound": Sound,
            "throw": Throw,
            "squirt": Squirt,
            "drop": Drop
        }
        print(list(gags))
        attacks[track](gags)

    plan.sort(key=lambda gag: gag.getTrack())
    gagsByTrack = [list(group[1]) for group in groupby(plan, lambda gag: gag.getTrack())]
    for gags in gagsByTrack:
        UseGags(gags,gags[0].getTrack())
