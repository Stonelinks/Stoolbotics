from objects import robot
import json, sys


def create_robot(filename):
    r = json.loads(open(filename).read(), object_hook=lambda d: robot(d))
    return r

#r.forwardkin()

#sys.exit()

r = create_robot('robots/sample.json')
#print 'N = ' + str(r.N)
#print 'q1 = ' + str(r.q1)
#print 'P01 = ' + str(r.P01)
#print 'P12 = ' + repr(r.P12)
#print 'R23 = ' + str(r.R23)


for i in range(20):
  r.forwardkin()
  r.timestep()
  print 'R23 = ' + str(r.R23)
