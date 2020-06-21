from loadClasses import LoadGagObjects, Gag, Toon, Cog
from toonAttack import Attack

gagsByName = LoadGagObjects()
wheatley = Toon(name = "Wheatley")
missblack = Toon(name = "Miss Black")
cog1 = Cog(level = 5)
cog2 = Cog(level = 6)

gag_wheatley = gagsByName["Elephant Trunk"]
gag_wheatley.setTarget(cog1)
gag_missblack = gagsByName["Elephant Trunk"]
gag_missblack.setTarget(cog1)
gag_wheatley.setOrganic(True)
gag_missblack.setOrganic(True)
plan = [gag_wheatley,gag_missblack]
toons = [wheatley,missblack]
cogs = [cog1,cog2]

# print(cog1.getHP(),cog2.getHP())
# Attack(plan = gags ,toons = toons, cogs = cogs)
