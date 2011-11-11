from objects import robot
import json, sys


def as_robot(dict):
    return robot(dict)

r = json.loads(open('robots/sample.json').read(), object_hook=as_robot)

#r.forwardkin()

#sys.exit()

for i in range(5):
    r.timestep()
    r.forwardkin()
    #print r.R0T
    print r.P0T
