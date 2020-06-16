import json
from collections import namedtuple
from json import JSONEncoder
from system.gag import Gag

def customStudentDecoder(studentDict):
    return namedtuple('X', studentDict.keys())(*studentDict.values())

#Assume you received this JSON response
studentJsonData = '{"name": "Cupcake", "track": "throw", "value": 6, "accuracy": 80}'

# Parse JSON into an object with attributes corresponding to dict keys.
student = json.loads(studentJsonData, object_hook=customStudentDecoder)

print("After Converting JSON Data into Custom Python Object")
print(student.name, student.track, student.value, student.accuracy)
