from config import *
from numpy import *
from tools.tools import *
from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *

import json, sys

from tools.display import *

class robot(object):
    def __init__(self, d, x=0, y=0, z=0):
        
        # make initial params class variables
        # also adds lists
        self.init_params(d)
        
        # origin
        self.x = x
        self.y = y
        self.z = z

    def init_params(self, d=None):
        if d is None:
            d = self.d
        
        globals()['t'] = 0
        
        # establish local vars
        for k, v in d.iteritems():
            locals()[k] = v

        # convert into something useful
        self._d = {}
        for k, v in d.iteritems():
            if k[0] == 'N':
                self._d[k] = int(v)
                continue

            # it is a vector
            if v[0] == '[':
                tmp = eval(v)
                
                # joint axis or position vector
                if k[0] == 'h' or k[0] == 'P':
                    # transpose
                    v = [[tmp[0]], [tmp[1]], [tmp[2]]]
            self._d[k] = v

        # pick out symbolic expressions
        self.syms = {}
        for k, v in self._d.iteritems():
            if k[0] in ['q', 'R', 'P']:
                self.syms[k] = v

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
                v = str(v).replace( key, "self._d['" + key + "']")
            if v[0] == '[':
                v = str(v).replace('\n', ',').replace("u'", '').replace("'", '')
                v = 'array(' + str(v) + ', float)'
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
        
        self.R0T = eye(3,3)
        self.P0T = zeros((3,1))
        
        # make R0T
        for R in self.rotations:
            self.R0T = dot(self.R0T, R)

        # make P0T
        tmp = eye(3,3)
        for R, P in zip(self.rotations, self.positions):
            self.P0T += dot(tmp, P)
            tmp = dot(tmp, R)
        
        #print str(R0T)
        #print str(P0T)

    def render(self):
        i=0
        glPushMatrix()
        for R, P in zip(self.rotations, self.positions):
            #if i ==0:
            #    print str(R)+' '+str(P)
            i=i+1
            glColor3f(1,1.0/len(self.rotations)*i,1.0/len(self.rotations)*i)
            
            glPushMatrix()
            glTranslate(P[0],P[1],P[2])
            #draw joint
            if array_equal(R,matrix(eye(3))): #prismatic
                draw_prismatic_joint(0, 0, 0, P[0], P[1], P[2])
                print "eye matrix"
            else: #rotational
                draw_rotational_joint(0, 0, 0, 10, 30)
                print "rot matrix"
            
            
            #load matrix
            tm=matrix([[1,0,0,0],[0,1,0,0],[0,0,1,0],[P[0],P[1],P[2],1]])
            rm=zeros_resize(R,4)
            currentMatrix=glGetFloatv(GL_PROJECTION_MATRIX)
            print currentMatrix
            #print rm
            
            double_matrix=[rm[0,0],rm[0,1],rm[0,2],rm[0,3],rm[1,0],rm[1,1],rm[1,2],rm[1,3],rm[2,0],rm[2,1],rm[2,2],rm[2,3],rm[3,0],rm[3,1],rm[3,2],rm[3,3]]
            glLoadMatrixf(double_matrix)
            
        #pop all joints off
        for i in range(len(self.rotations)):
            glPopMatrix()
        glPopMatrix()

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
