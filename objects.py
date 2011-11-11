from config import *
from numpy import *
from tools.tools import *
import json, sys

class robot(object):
    def __init__(self, d, x=0, y=0, z=0):
        
        # make initial params class variables
        # also adds lists
        self.init_params(d)
        
        # origin
        self.x = x
        self.y = y
        self.z = z
        self.arms = []

    def init_params(self, d=None):
        if d is None:
            d = self.d
        
        globals()['t'] = 0
        
        # establish local vars and pick out
        # symbolic expressions
        self.syms = {}
        for k, v in d.iteritems():
            if k[0] in ['q', 'R', 'P']:
                self.syms[k] = v
            locals()[k] = v

        # convert into something useful
        _d = self._d = {}
        for k, v in d.iteritems():
            if k[0] == 'N':
                _d[k] = int(v)
                continue

            # it is a vector
            if v[0] == '[':
                tmp = eval(v)
                
                # joint axis
                if k[0] == 'h':
                    # transpose
                    v = array([[float(tmp[0])], [float(tmp[1])], [float(tmp[2])]])
                else:
                    # leave it alone
                    v = array([float(tmp[0]), float(tmp[1]), float(tmp[2])])
            _d[k] = v

        # eval syms
        self.eval_syms()
        
        self.build_lists()
        
    def build_lists(self):
        self.joint_axes = []
        self.joint_params = []
        self.joint_geoms = []
        
        for i in range(1, self.N + 1):
            self.joint_axes.append(eval('self.h' + str(i)))
            self.joint_params.append(eval('self.q' + str(i)))
            self.joint_geoms.append(eval('self.l' + str(i)))
        
        self.rotations = []
        self.positions = []
        
        indexes = []
        for i in range(1, self.N):
            indexes.append(str(i) + str(i + 1))
        indexes.append(str(self.N) + 'T')
        
        for i in indexes:
            self.rotations.append(eval('self.R' + i))
            self.positions.append(eval('self.P' + i))
        
    def eval_syms(self):
        for k, v in self.syms.iteritems():
          for key, _ in self._d.iteritems():
              v = v.replace( key, "self._d['" + key + "']")
          self._d[k] = eval(v)
        self.sync_d()
    
    def sync_d(self):
        for k, v in self._d.iteritems():
            setattr(self, k, v)

    def timestep(self):
        global t
        t+=1
        self.eval_syms()
        self.build_lists()
    
    def forwardkin(self, params=None):
        if params == None:
            params = self.joint_params
        
        R0T = eye(3,3)
        P0T = eye(3,3)
        
        # make R0T
        for R in self.rotations:
            R0T = dot(R0T, R)

        # make P0T
        accum = []
        for R, P in zip(self.rotations, self.positions):
            accum.append(R)
            tmp = eye(3,3)
            for _r in accum:
                tmp = dot(tmp, _r)
            P = eval('[%s,%s,%s]' % (P[0], P[1], P[2]))
            P0T += dot(tmp, P)
        
        #print str(R0T)
        #print str(P0T)
        
        self.R0T = R0T
        self.P0T = P0T

    def render(self):
        pass
        

class room(object):
    def __init__(self, _length=0, _width=0, _height=0):
        self.length=_length
        self.width=_width
        self.height=_height

    def render(self):
        glColor3f(0,0,0)
        glBegin(GL_LINES)
        glVertex3f(0,0,0)
        glVertex3f(scale,0,0)
        glVertex3f(0,0,0)
        glVertex3f(0,scale,0)
        glVertex3f(0,0,0)
        glVertex3f(0,0,scale)
        glEnd()
        for i in range(-self.width/scale/2, self.width/scale/2):            
            for j in range (-self.length/scale/2, self.length/scale/2):
                if ((i+j)%2 ==0):
                    glColor3f(0.0, 1.0, 0.0);
                else:
                    glColor3f(0.0, 0.0, 1.0);
                glBegin(GL_QUADS)
                glVertex3f(i*scale,0,j*scale)
                glVertex3f((i+1)*scale,0,j*scale)
                glVertex3f((i+1)*scale,0,(j+1)*scale)
                glVertex3f(i*scale,0,(j+1)*scale)
                glEnd()
