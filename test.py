from objects import robot
import json, sys
import time

def create_robot(filename):
    r = json.loads(open(filename).read(), object_hook=lambda d: robot(d))
    return r

#r.forwardkin()

#sys.exit()

r = create_robot('robots/sample.json')

for i in range(20):
  r.forwardkin()
  r.timestep()
  time.sleep(1)
  print "==========  Timestep " + str(i) + " ==========="
  for link in r.links:
    print link
