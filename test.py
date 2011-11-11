from objects import robot
import json


def as_robot(dict):
    return robot(dict)

r = json.loads(open('robots/sample.json').read(), object_hook=as_robot)

for i in range(5):
    r.timestep()
    r.forwardkin()
