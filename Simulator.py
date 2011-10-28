#!/usr/bin/env python
from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *

from math import *
import sys
import Image
import numpy

width = 700
height = 400
oldMouseDraggedX=0
oldMouseDraggedY=0
angleY = 0
angleX = 60
scale=10
PI = 3.14159265
R = 20.0    
mouseMiddlePressed=False

class arm():
    rotation=[1,0,0]
    links=[]
    def __init__(self, axis):
        rotation=axis
    def __init__(self, axis, linkX, linkY, linkZ):
        rotation=axis
        addLink(linkX, linkY, linkZ)
        
    def addLink(self, linkX, linkY, linkZ):
        links.append(array(linkX, linkY, linkZ))
    def setRotation(axis):
        rotation=axis
        
class Robot():
    x=0
    y=0
    z=0
    arms=[]
    def __init__(self, _x, _y, _z):
        self.x=_x
        self.y=_y
        self.z=_z

    def addArm(self, arm):
        arms.append(arm)
            
    def render(self):
        #for i in arms
            
         #   for j in i.links
                
        return
    
class Room():
    length=0
    width=0
    height=0
    def __init__(self, _length, _width, _height):
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

                
def timestep():
    global angleY
    angleY += 1
    glutPostRedisplay()

# Mouse motion callback routine.
def mouseMotion(x,y):
    return
    #y=height-y
    #glutPostRedisplay()

def mouseDragged(x,y):
    global angleX
    global angleY
    global oldMouseDraggedX
    global oldMouseDraggedY

    if(mouseMiddlePressed == False):
        return
    if ( x < 0 or x > width or y < 0 or y > height ):
        return

    
    changeX=x-oldMouseDraggedX
    changeY=y-oldMouseDraggedY
    oldMouseDraggedX=x
    oldMouseDraggedY=y
    angleY+=changeX
    angleX+=changeY
    if (angleX<0):
        angleX=0
    if (angleX>180):
        angleX=180
    glutPostRedisplay()

#The mouse callback routine.
def mouseControl(button, state, x, y):
    global mouseMiddlePressed
    global oldMouseDraggedX
    global oldMouseDraggedY
    #y = height - y; # Correct from mouse to OpenGL co-ordinates.
    print 'X='+ str(x) +' Y='+str(y)
    if ( x < 0 or x > width or y < 0 or y > height ):
        return
    if (button == GLUT_LEFT_BUTTON and state == GLUT_DOWN):
        print "LEFT Down"
    elif (button==GLUT_MIDDLE_BUTTON and state == GLUT_DOWN):
        mouseMiddlePressed=True
        oldMouseDraggedX=x
        oldMouseDraggedY=y
        print "Middle Down"
    elif (button==GLUT_MIDDLE_BUTTON and state == GLUT_UP):
        mouseMiddlePressed=False
        print "Middle Up"
    elif (button==GLUT_RIGHT_BUTTON and state == GLUT_DOWN):
        mouseMiddlePressed=True
        oldMouseDraggedX=x
        oldMouseDraggedY=y
        print "Middle Down"
    elif (button==GLUT_RIGHT_BUTTON and state == GLUT_UP):
        mouseMiddlePressed=False
        print "Middle Up"
    elif (button == GLUT_LEFT_BUTTON and state == GLUT_UP):
        print "LEFT UP"

def keyboard(key, x, y):
    if key == chr(27):
        sys.exit(0)
    elif key == 's':
        s = glReadPixels(0, 0, w, h, GL_RGB, GL_UNSIGNED_BYTE)
        img = Image.new('RGB', (width, height))
        img.fromstring(s)
        img2 = img.transpose(Image.FLIP_TOP_BOTTOM)
        img2.save("screendump.jpg")

def draw():
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glPushMatrix()
    #looking at x/y plane - down z axis
    glTranslatef(0.0, 0.0, -30.0)
    glRotatef(angleY, 0.0, 1.0, 0.0)
    glRotatef(angleX, 1.0, 0.0, 0.0)
  #  glTranslatef(0.0, 0.0, 60.0)
    room.render()
    
    glColor3f(0.0, 0.0, 0.0)
    glBegin(GL_LINE_STRIP)
    for t in numpy.arange(0, 20 * PI, float(PI / 20.0)): 
        glVertex3f(R * cos(t), t, R * sin(t))
    glEnd()
    
    glPopMatrix()

    glutSwapBuffers()

def setup():
    glClearColor(1.0, 1.0, 1.0, 0.0)
    glEnable(GL_DEPTH_TEST)
    global room
    room = Room(100,100,100)
    
def resize(_w, _h):
    width = _w
    height = _h
    glViewport(0, 0, width, height)
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    glOrtho (-width/scale, width/scale, -height/scale, height/scale, -100.0, 100.0)
    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()

glutInit([])
glutInitDisplayMode(GLUT_RGB | GLUT_DOUBLE | GLUT_DEPTH)
glutInitWindowSize(width,height)
glutInitWindowPosition(100, 100) 
glutCreateWindow(sys.argv[0])
setup()

glutDisplayFunc(draw)
#glutIdleFunc(timestep)
glutKeyboardFunc(keyboard)
glutMouseFunc(mouseControl)
glutPassiveMotionFunc(mouseMotion)
glutMotionFunc(mouseDragged)
glutReshapeFunc(resize);  

glutMainLoop()
