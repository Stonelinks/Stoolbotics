from config import *
from numpy import *
from tools.tools import *
import json, sys

class arm(object):
    def __init__(self, _type=1, _joint=[]):
        self.type = _type
        self.joint = _joint
        self.links = []
    
    def addLink(self, link):
        self.links.append(link)
        
    def setJoint(_joint):
        self.joint=_joint
        
    def setType(_type):
        self.type=_type
    
    def repr(self):
        return self.str()
        
    def str( self ):
        s="Rotation =\n"
        s=s+str(joint)+"\n"
        for i in range(len(links)):
            s=s+"Joint "+str(i)+"\n"
            s=s+str(links[i])
        s+="\n"
        return s

class robot(object):
    def __init__(self, d, x=0, y=0, z=0):
        
        # establish literals
        for k, v in d.iteritems():
            locals()[k] = v
        
        # convert settings into something useful
        _d = {}
        for k, v in d.iteritems():
            # joint parameter
            if k[0] == 'q':
                _d[k] = float(v)
                continue
            elif k[0] == 'N':
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
            
        # set everything as class variables
        for k, v in _d.iteritems():
            if not (isinstance(v, float) or isinstance(v, int)):
                if v[0] == 'r' or v[0] == 'e':
                    cmd = v
                    for key, val in _d.iteritems():
                        cmd = cmd.replace( key, "_d['" + key + "']")
                    setattr(self, k, eval(cmd))
            else:
                setattr(self, k, v)
            
        # origin
        self.x = x
        self.y = y
        self.z = z
        self.arms = []

    def addArm(self, arm):
        self.arms.append(arm)
            
    def render(self):
        pass
                
    def repr(self):
        print "test"
        return self.str()
        
    def str(self):
        print "test2"
        return "robot"
        s="Position ="+str(x)+","+str(y)+","+str(z)+"\n"
        for i in range(len(arms)):
            s=s+"Arm"+str(i)+"\n"
            s=s+str(arms[i])
        s+="\n"
        return s
        
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
