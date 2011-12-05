from numpy import *
from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *

import tools.display as display
import tools.material as material
from tools.tools import *
import config
from config import *

import json, sys, re, math, time

class link():
    def __init__(self, name, parent):
        self.name = name
        self.parent = parent
        self.index = int(name[0])
        
        self.pos = eval('parent.P' + name)
        self.P = self.pos

        self.rot = eval('parent.R' + name)
        self.R = self.rot

        if 'q' in parent.syms['P' + name]:
            self.type = 'prismatic'
        else:
            self.type = 'rotary'

        if self.index >= parent.N:
            self.q = None
            self.h = None
        else:
            n = str(self.index + 1)
            self.q = eval('parent.q' + n)
            self.h = eval('parent.h' + n)
            
        self.param = self.q
        self.parameter = self.param
        
        self.axis = self.h
        
    def __str__(self):
        return "link: " + self.name + ", type: " + self.type + ", q: " + str(self.q) + ", h: " + str(self.h) + ", p: " + str(self.P)
    
    def is_prismatic(self):
        return self.type == 'prismatic'
    
    def location(self):
        return self.parent.verts[self.index]
    
class robot(object):
    def __init__(self, d):
        self.init_params(d)
        
        self.trace = []
        self.trace_enabled = config.enable_trace
        self.ghosts_enabled = config.enable_ghost
        
        self.verts = []

    def init_params(self, d=None):
        if d is None:
            d = self.d
        
        globals()['t'] = 0.0

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
                
        x = [1, 0, 0]
        y = [0, 1, 0]
        z = [0, 0, 1]
                
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
            l = eval('link(\'' + i + '\', self)')
            self.links.append(l)
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

    def timestep(self, scale = 1.0):
        globals()['t'] += scale
        self.eval_syms()
        self.build_lists()
        time.sleep(.01)
    
    # get any arbitrary rotation matrix, e.g. self.R(0,3) will give you R03
    def R(self, base_index = 0, final_index = 'T'):
        if final_index == 'T':
            n = self.N
        else:
            n = final_index
        R = eye(3, 3)
        for i in range(base_index, n):
            R = dot(R, self.links[i].R)
        return R
    
    def forwardkin(self):
        self.R0T = eye(3, 3)
        self.P0T = zeros((3, 1))
        self.verts = []
        
        # make R0T
        for link in self.links:
            self.R0T = dot(self.R0T, link.R)
        
        # make P0T
        tmp = eye(3,3)
        p = None
        for link in self.links:
            self.P0T += dot(tmp, link.P)
            tmp = dot(tmp, link.R)
            
            # TODO - put this in link class
            p = (self.P0T[0][0], self.P0T[1][0], self.P0T[2][0])
            self.verts.append(p)
        if self.trace_enabled:
            self.trace.append(self.verts)
        
    def print_vars(self):
        print "=========== begin dump of robot vars ============"
        for k, v in self._d.iteritems():
            sys.stdout.write(str(k) + ' = ')
            print(v)
            print '\n'
        print "=========== end =============="

    def render(self):
        for link in self.links:
            R = link.R
            P = link.P
            h = link.h
            
            if config.enable_lighting:
                material.black()
            else:
                glColor3f(0, 0, 0)

            glPushMatrix()
            glLineWidth(15)
            glBegin(GL_LINES)
            glVertex3f(0,0,0)
            glVertex3f(P[0],P[1],P[2])
            glEnd()

            glTranslate(P[0], P[1], P[2])
            
            if config.enable_axis and link.index != self.N:
                display.draw_axes(20, str(link.index))
            else:
                display.draw_axes(20, 'T')
            
            # draw joint
            if link.is_prismatic(): # prismatic joint
                display.draw_prismatic_joint([[0],[0],[0]], P, 10)
            elif (R == eye(3)).all(): # link - no joint
                pass
            else: # rotation joint
                    
                if config.enable_lighting:
                    material.green()
                else:
                    glColor3f(0, 0.6, 0)
                display.draw_rotational_joint(h*10, -h*10, 8, link.q * 180 / PI)

                if config.enable_lighting:
                    material.grey()
                else:
                    glColor3f(0.3, 0.3, 0.3)
                
                glRotate(link.q * 180 / PI, link.h[0], link.h[1], link.h[2])

        # pop all joints off
        for matPop in self.links:
            glPopMatrix()

        glLineWidth(5)
        glPointSize(10)
        
        # only save the last whatever points
        self.trace = self.trace[-config.max_trace:]

        if self.ghosts_enabled:
            if config.enable_lighting:
                material.grey()
            else:
                glColor3f(0.4, 0.4, 0.4)
            
            glPointSize(8)
            for verts, i in zip(self.trace, range(len(self.trace))):
                if i % config.ghost_interval == 1:
                    glBegin(GL_POINTS)
                    for vert in verts:
                            glVertex3f(vert[0], vert[1], vert[2])
                    glEnd()

            if config.enable_lighting:
                material.grey()
            else:
                glColor3f(0.7, 0.7, 0.7)
            
            for verts, i in zip(self.trace, range(len(self.trace))):
                if i % config.ghost_interval == 1:
                    glBegin(GL_LINE_STRIP)
                    for vert in verts:
                            glVertex3f(vert[0], vert[1], vert[2])
                    glEnd()
        
        if self.trace_enabled:
            # saved tool positions

            if config.enable_lighting:
                material.red()
            else:
                glColor3f(1.0, 0.0, 0)
            glBegin(GL_LINE_STRIP)
            for verts in self.trace:
                vert = verts[-1:][0]
                glVertex3f(vert[0], vert[1], vert[2])
            glEnd()

class room(object):
    def __init__(self, length=0, width=0, height=0, outLined=True):
        self.length = length
        self.width = width
        self.height = height
        self.outLined = outLined
        
        # this gets set by the simulator
        self.scale = None
        
    def render(self):
        s = self.scale
        l = self.length
        
        startL =- (l/s)/2
        endL = (l/s)/2
        startW =- (self.width/s)/2
        endW = (self.width/s)/2
        if (self.outLined):
            glBegin(GL_LINES)
            for j in range(startW, endW + 1):
                glVertex3f(startL*s, j*s, 0)
                glVertex3f(endL*s, j*s, 0)
            for i in range (startL, endL + 1):
                glVertex3f(i*s, startW*s, 0)
                glVertex3f(i*s, endW*s, 0)
        else:
            glBegin(GL_QUADS)
            for i in range(startW, endW):
                for j in range(startL, endL):
                    if ((i + j) % 2 == 0):
                        if config.enable_lighting:
                            material.grey()
                        else:
                            glColor3f(0.3, 0.3, 0.3)
                    else:
                        if config.enable_lighting:
                            material.darkgrey()
                        else:
                            glColor3f(0.6, 0.6, 0.6)
                    x0 = i*s
                    y0 = j*s
                    x1 = (i + 1)*s
                    y1 = (j + 1)*s
                    
                    glVertex3f(x0, y0, 0)
                    glVertex3f(x1, y0, 0)
                    glVertex3f(x1, y1, 0)
                    glVertex3f(x0, y1, 0)
                    
                    # todo: draw other walls to make a room
        glEnd()

