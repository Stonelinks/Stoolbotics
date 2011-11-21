from config import *
from numpy import *
from tools.tools import *
from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *

import json, sys, re, math
import copy as realcopy

from tools.display import *

class link():
    def __init__(self, name, pos, rot, type, param, axis):
        self.name = name
        self.pos = pos
        self.P = pos
        self.rot = rot
        self.R = rot
        self.type = type

        self.param = param
        self.parameter = param
        self.q = param
        
        self.axis = axis
        self.h = axis
        
    def __str__(self):
        return "link: " + self.name + ", type: " + self.type + ", q: " + str(self.q) + ", h: " + str(self.h) 
    
    def is_prismatic(self):
        return self.type == 'prismatic'

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

        # establish local vars, pick out syms
        self.syms = {}
        for k, v in d.iteritems():
            if k[0] in ['q', 'R', 'P']:
                if k[0] == 'q':
                    self.syms[k] = 'float(' + v + ')'
                else:
                    self.syms[k] = v
            locals()[k] = v

        # attempt to naievely evaluate
        for k, v in d.iteritems():
            try:
                locals()[k] = eval(v)
            except:
                pass
                
        x = [ 1, 0, 0 ]
        y = [ 0, 1, 0 ]
        z = [ 0, 0, 1 ]

                
        self._d = {}
        for k, v in d.iteritems():
            if k[0] == 'N':
                self._d[k] = int(v)
                continue
            elif k[0] == 'q':
                self._d[k] = eval('float(' + v + ')')
                continue
            elif k[0] == 'l':
                self._d[k] = float(v)
                continue
            elif k[0] == 'h' and v[0] != '[': #used axis shorthand
                v = eval('str(' + v + ')')

            # it is a vector
            if v[0] == '[':
                
                tmp = eval(v)
                
                # joint axis or position vector
                if k[0] == 'h' or k[0] == 'P':
                    # transpose
                    v = array([[tmp[0], tmp[1], tmp[2]]], float).T
            self._d[k] = v
        
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
        
        self.links = []
        indexes = []
        for i in range(0, self.N):
            indexes.append(str(i) + str(i + 1))
        indexes.append(str(self.N) + 'T')
        
        c = 1
        for i in indexes:
            cmd = 'link(\'' + i + '\', '
            cmd += 'self.P' + i + ', '
            cmd += 'self.R' + i + ', '
            
            if 'q' in self.syms['P' + i]:
                cmd += '\'prismatic\''
            else:
                cmd += '\'rotary\''
            cmd += ', '
            q = 'self.q' + str(c)

            cmd2 = ', '
            cmd2 += 'self.h' + str(c)
            if c > self.N:
                m = eval(cmd + 'None, None )')
            else:
                m = eval(cmd + q + cmd2 + ')')
            self.links.append(m)
            c += 1
        
    def eval_syms(self):
        # TODO: use regex for all of this

        x = array([[1], [0], [0] ], float)
        y = array([[0], [1], [0] ], float)
        z = array([[0], [0], [1] ], float)

        # eval syms
        for k, v in self.syms.iteritems():
            tmp = v
            for key, _ in self._d.iteritems():
                tmp = str(tmp).replace( key, 'self._d[\'' + key + '\']')
                if 'u\'' + key + '\'' in tmp:
                    tmp = tmp.replace('u\'' + key + '\'', key)
                    #something like this would be awesome: tmp = re.sub(r'u\'(.*)\'', tmp, tmp)
            
            if k[0] == 'P' and tmp[0] == '[':
                tmp = 'array([' + tmp + '], float).T'
            elif k[0] == 'h' and v[0] != '[': #axis shorthand
                tmp = v
            self._d[k] = eval(tmp)
        self.sync_d()
    
    def sync_d(self):
        for k, v in self._d.iteritems():
            setattr(self, k, v)

    def timestep(self):
        global t
        t+=1
        self.eval_syms()
        self.build_lists()
    
    def forwardkin(self):
        
        self.R0T = eye(3,3)
        self.P0T = zeros((3,1))
        
        # make R0T
        for link in self.links:
            self.R0T = dot(self.R0T, link.R)

        # make P0T
        tmp = eye(3,3)
        for link in self.links:
            self.P0T += dot(tmp, link.P)
            tmp = dot(tmp, link.R)
        

    def render(self):
        glPushMatrix()
        glTranslate(0,0,1)
        H=asmatrix(eye(4))
        currentMatrix=reshape(asmatrix(glGetFloatv(GL_PROJECTION_MATRIX)),(4,4))
        for numLink in range(len(self.links)):
            link=self.links[numLink]
            R = link.R
            P = link.P
            h = link.h
            
            
            glColor3f( 0,0,0)
            glPushMatrix()
            glBegin(GL_LINES)
            glVertex3f(0,0,0)
            glVertex3f(P[0],P[1],P[2])
            glEnd()
            glTranslate(P[0],P[1],P[2])
            
            glColor3f( 1, 1.0/len(self.links)*numLink ,1.0/len(self.links)*numLink)
            #draw joint
            print link
            if link.is_prismatic(): #prismatic joint
                draw_prismatic_joint(0, 0, 0, P[0], P[1], P[2])
            elif (R == eye(3)).all(): #link - no joint
                pass
            else: #rotation joint
                glPushMatrix()
                draw_rotational_joint(h*10, h*-10, 10)
                glPopMatrix()
                
                glRotate(link.q, link.h[0], link.h[1], link.h[2])
                
                
            
            #load matrix
            #rot_m=zeros_resize(R, 4)
            #rot_m[0,3]=P[0]
            #rot_m[1,3]=P[1]
            #rot_m[2,3]=P[2]
            #rot_m[3,3]=1
            #H=H*rot_m
            #tm=H*currentMatrix
            #print tm
            #double_matrix=[ tm[0,0],tm[0,1],tm[0,2],tm[0,3],
            #                tm[1,0],tm[1,1],tm[1,2],tm[1,3],
            #                tm[2,0],tm[2,1],tm[2,2],tm[2,3],
            #                tm[3,0],tm[3,1],tm[3,2],tm[3,3] ]
            
            #glLoadMatrixf(double_matrix)
            
        #pop all joints off
        draw_axes(10,'T')
        for matPop in range(len(self.links)):
            glPopMatrix()
        glPopMatrix()

class room(object):
    def __init__(self, _length=0, _width=0, _height=0, outLined=True):
        self.length=_length
        self.width=_width
        self.height=_height
        self.outLined=outLined
        
    def render(self):
        startL=-self.length/scale/2
        endL=self.length/scale/2
        startW=-self.width/scale/2
        endW=self.width/scale/2
        if (self.outLined):
            glBegin(GL_LINES)
            for j in range(startW, endW+1):
                glVertex3f(startL*scale,j*scale, 0)
                glVertex3f(endL*scale,j*scale, 0)
            for i in range (startL, endL+1):
                glVertex3f(i*scale,startW*scale, 0)
                glVertex3f(i*scale,endW*scale, 0)
        else:
            glBegin(GL_QUADS)
            for i in range(startW, endW):
                for j in range (startL, endL):
                    if ((i+j)%2 ==0):
                        glColor3f(0.0, 1.0, 0.0);
                    else:
                        glColor3f(0.0, 0.0, 1.0);
                    
                    glVertex3f(i*scale,j*scale, 0)
                    glVertex3f((i+1)*scale,j*scale, 0)
                    glVertex3f((i+1)*scale,(j+1)*scale, 0)
                    glVertex3f(i*scale,(j+1)*scale, 0)
        glEnd()
