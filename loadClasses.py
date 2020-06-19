from gag import Gag
from data.gags import gagData

def LoadGagObjects():
    return [Gag(name=gag["name"],track=gag["track"],value=gag["value"],accuracy=gag["accuracy"],hitsAll=gag["hitsAll"]) for gag in gagData]
