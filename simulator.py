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

from config import *
from objects import *

tscale = .2

def timestep():
    global tscale
    robot.forwardkin()
    robot.timestep(tscale)
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

    changeX = x - oldMouseDraggedX
    changeY = y - oldMouseDraggedY
    oldMouseDraggedX = x
    oldMouseDraggedY = y
    angleY += changeX
    angleX += changeY
    print "Angle x/y = " + str(angleX)+"/"+str(angleY)
    if (angleX < 180):
        angleX = 180
    if (angleX > 360):
        angleX = 360
    glutPostRedisplay()

#The mouse callback routine.
def mouseControl(button, state, x, y):
    global mouseMiddlePressed
    global oldMouseDraggedX
    global oldMouseDraggedY
    #y = height - y; # Correct from mouse to OpenGL co-ordinates.
    print 'X = ' + str(x) +' Y = ' + str(y)
    if (button == 3):# Zoom in
        zoom_in()
        return
    elif (button == 4): # Zoom out
        zoom_out()
        return
        
    if (x < 0 or x > width or y < 0 or y > height):
        return
    if (button == GLUT_LEFT_BUTTON and state == GLUT_DOWN):
        print "LEFT Down"
        print "LEFT Down"
    elif (button == GLUT_MIDDLE_BUTTON and state == GLUT_DOWN):
        mouseMiddlePressed = True
        oldMouseDraggedX = x
        oldMouseDraggedY = y
        print "Middle Down"
    elif (button == GLUT_MIDDLE_BUTTON and state == GLUT_UP):
        mouseMiddlePressed = False
        print "Middle Up"
    elif (button == GLUT_RIGHT_BUTTON and state == GLUT_DOWN):
        mouseMiddlePressed = True
        oldMouseDraggedX = x
        oldMouseDraggedY = y
        print "Middle Down"
    elif (button == GLUT_RIGHT_BUTTON and state == GLUT_UP):
        mouseMiddlePressed = False
        print "Middle Up"
    elif (button == GLUT_LEFT_BUTTON and state == GLUT_UP):
        print "LEFT UP"

def zoom_out():
    global zoom
    zoom=zoom + .1
    print "Zoom = " + str(zoom)
    resize()
    glutPostRedisplay()
    
def zoom_in():
    global zoom
    if (zoom > 0.1):
        zoom = zoom - .1
    print "Zoom = " + str(zoom)
    resize()
    glutPostRedisplay()

def keyboard_special(key, x, y):
    if key == GLUT_KEY_RIGHT:
        global transX
        transX= transX+5
        glutPostRedisplay()
    elif key == GLUT_KEY_LEFT:
        global transX
        transX= transX-5
        glutPostRedisplay()
    elif key == GLUT_KEY_DOWN:
        global transY
        transY= transY-5
        glutPostRedisplay()
    elif key == GLUT_KEY_UP:
        global transY
        transY= transY+5
        glutPostRedisplay()

def keyboard(key, x, y):
    print key
    if key == chr(27):
        sys.exit(0)
    elif key == 'p':
        glutIdleFunc(timestep)
    elif key == 's':
        glutIdleFunc(None)
    elif key == '+':
        zoom_in()
    elif key == '-':
        zoom_out()
    elif key == 'f':
        global tscale
        tscale += .01
    elif key == 'd':
        global tscale
        tscale -= .01
        
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
    glTranslatef(transX, transY, transZ)
    glRotatef(angleY, 0.0, 1.0, 0.0)
    glRotatef(angleX, 1.0, 0.0, 0.0)
    
    room.render()
    
    glColor3f(0, 0, 0)
    display.draw_axes(20,'1')
    
    #robot.render()
    
    glPointSize(10)
    glLineWidth(2)
    glColor3f(0.0, 0.0, 0.0)
    glBegin(GL_LINE_STRIP)
    for vert in robot.verts:
        glVertex3f(vert[0], vert[1], vert[2])
    glEnd()
    glBegin(GL_POINTS)
    for vert in robot.verts:
        glVertex3f(vert[0], vert[1], vert[2])
    glEnd()

    
    
    glPopMatrix()

    # reference axis
    glPushMatrix()
    global zoom
    print zoom
    glTranslatef(zoom*55.0, zoom*-50.0, 80.0)

    glRotatef(angleY, 0.0, 1.0, 0.0)
    glRotatef(angleX, 1.0, 0.0, 0.0)
    display.draw_axes(zoom*13,'')
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
    room = room(100,100,100, False)
    global robot
    robot = create_robot('robots/sample.json')
    robot.forwardkin()
    robot.timestep()
    robot.print_vars()

def create_robot(filename):
    r = json.loads(open(filename).read(), object_hook=lambda d: robot(d))
    return r
    
def resize(_w = width, _h = height):
    width = _w
    height = _h
    glViewport(0, 0, width, height)
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    glOrtho (-zoom*width/scale, zoom*width/scale, -zoom*height/scale, zoom*height/scale, -100.0, 100.0)
    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()

def main():
    global width, height
    
    glutInit()
    glutInitDisplayMode(GLUT_RGB | GLUT_DOUBLE | GLUT_DEPTH)
    glutInitWindowSize(width , height)
    glutInitWindowPosition(100, 100) 

    glutCreateWindow(sys.argv[0])

    setup()
    glutDisplayFunc(draw)
    glutKeyboardFunc(keyboard)
    glutSpecialFunc(keyboard_special)
    glutMouseFunc(mouseControl)
    glutPassiveMotionFunc(mouseMotion)
    glutMotionFunc(mouseDragged)
    glutReshapeFunc(resize);  

    glutMainLoop()
    return 0

if __name__ == '__main__':
    main()
