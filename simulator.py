#!/usr/bin/env python
from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *

from math import *
import sys
import Image
import numpy
from numpy import *
import os
import ConfigParser

from config import *
from objects import *

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
    #glEnable(GL_LIGHTING)

    # Light property vectors.
    lightAmb = [ 0.0, 0.0, 0.0, 1.0 ]
    lightDifAndSpec = [ 1.0, 1.0, 1.0, 1.0 ]
    lightPos = [ 0.0, 1.5, 3.0, 1.0 ]
    globAmb = [ 0.2, 0.2, 0.2, 1.0 ]

    # Light properties.
    glLightfv(GL_LIGHT0, GL_AMBIENT, lightAmb)
    glLightfv(GL_LIGHT0, GL_DIFFUSE, lightDifAndSpec)
    glLightfv(GL_LIGHT0, GL_SPECULAR, lightDifAndSpec)
    glLightfv(GL_LIGHT0, GL_POSITION, lightPos)

    #glEnable(GL_LIGHT0) # Enable particular light source.
    glLightModelfv(GL_LIGHT_MODEL_AMBIENT, globAmb) # Global ambient light.
    glLightModeli(GL_LIGHT_MODEL_TWO_SIDE, GL_TRUE) # Enable two-sided lighting.
    glLightModeli(GL_LIGHT_MODEL_LOCAL_VIEWER, GL_TRUE) # Enable local viewpoint.

    # Enable two vertex arrays: position and normal.
    glEnableClientState(GL_VERTEX_ARRAY)
    glEnableClientState(GL_NORMAL_ARRAY)

    # Specify locations for the position and normal arrays.
    #glVertexPointer(3, GL_FLOAT, 0, vertices)
    #glNormalPointer(GL_FLOAT, 0, normals)
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

def readTextFile(_fileName):
    global robot
    robot=Robot(50,0,50)
    
    _fileFullName=os.path.join(os.path.dirname(__file__),_fileName)
    f=open(_fileFullName)
    parser = ConfigParser.ConfigParser()
    parser.read(_fileFullName.replace("/","//"))
    
    NumJoints=int(parser.get("Joints", "NumberOfJoints"))
    for n in range(1,NumJoints+1):
        type=int(parser.get("Joint%d" %n, "Type"))
        numLinks=int(parser.get("Joint%d" %n, "NumberOfLinks"))
        jointArray=str.split(str.strip(parser.get("Joint%d" %n, "Joint"),' []'),',')
        joint=numpy.transpose(matrix(jointArray, dtype=float))
        arm=Arm(type,joint)
        for l in range (1, numLinks+1):
            linkArray=str.split(str.strip(parser.get("Joint%d" %n, "Link%d" %l),' []'),',')
            link=numpy.transpose(matrix(linkArray, dtype=float))
            arm.addLink(link)
        robot.addArm(arm)
    print robot

def main():   
    global width, height
    glutInit()
    glutInitDisplayMode(GLUT_RGB | GLUT_DOUBLE | GLUT_DEPTH)
    glutInitWindowSize(width , height)
    glutInitWindowPosition(100, 100) 

    glutCreateWindow(sys.argv[0])

    setup()
    readTextFile("robot_elbow.ini")
    glutDisplayFunc(draw)
    #glutIdleFunc(timestep)
    glutKeyboardFunc(keyboard)
    glutMouseFunc(mouseControl)
    glutPassiveMotionFunc(mouseMotion)
    glutMotionFunc(mouseDragged)
    glutReshapeFunc(resize);  

    glutMainLoop()
    return 0

if __name__ == '__main__':
    main()
