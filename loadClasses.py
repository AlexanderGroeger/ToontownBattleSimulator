from gag import Gag
from toon import Toon
from cog import Cog
from data.gags import gagData

def LoadGagObjects():
    return {gag["name"]:Gag(name=gag["name"],track=gag["track"],value=gag["value"],accuracy=gag["accuracy"],hitsAll=gag["hitsAll"]) for gag in gagData}

def GagObjectFromDict(gag):
    return Gag(name=gag["name"],track=gag["track"],value=gag["value"],accuracy=gag["accuracy"],hitsAll=gag["hitsAll"])
