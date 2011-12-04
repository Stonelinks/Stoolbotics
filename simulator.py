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
import json
import config
import objects
import tools.display as display

class mouse():
    def __init__(self):
        self.x = None
        self.y = None
        
        self.up = False
        self.down = False
        self.oldMouseDraggedX = None
        self.oldMouseDraggedY = None
        self.middlePressed = False
        self.rightPressed = False
        self.leftPressed = False
        
class simulator():
    def __init__(self, robot, room):
        self.robot = robot
        self.room = room
        self.mouse = mouse()

        self.width = 800
        self.height = 600

        self.angleY = -135
        self.angleX = 245

        self.transX = 0
        self.transY = -30.0
        self.transZ = 0

        self.tscale = .2
        self.scale = 10
        self.room.scale = self.scale
        self.zoom = 1.6

        self.robot.forwardkin()
        self.robot.timestep()
        self.robot.print_vars()
        
    def timestep(self):
        self.robot.forwardkin()
        self.robot.timestep(self.tscale)
        glutPostRedisplay()
    
    def _updateMouse(self, x, y):
        self.mouse.x = x
        self.mouse.y = y

    # Mouse motion callback routine.
    def mouseMotion(self, x, y):
        self._updateMouse(x, y)

    def mouseDragged(self, x, y):
        self._updateMouse(x, y)

        changeX = x - self.mouse.oldMouseDraggedX
        changeY = y - self.mouse.oldMouseDraggedY

        self.mouse.oldMouseDraggedX = x
        self.mouse.oldMouseDraggedY = y

        # why are these mixed up? it breaks without it
        self.angleX += changeY
        self.angleY -= changeX
        
        print "Angle = (" + str(self.angleX) + ", " + str(self.angleY) + ")"
        if (self.angleX < 180):
            self.angleX = 180
        if (self.angleX > 360):
            self.angleX = 360
        glutPostRedisplay()

    #The mouse callback routine.
    def mouseControl(self, button, state, x, y):
        self._updateMouse(x, y)
        print 'X = ' + str(x) +' Y = ' + str(y)
        if (button == 3):# Zoom in
            self.camera_zoom('in')
            return
        elif (button == 4): # Zoom out
            self.camera_zoom('out')
            return
        
        # clear mouse object
        self.mouse.leftPressed = False
        self.mouse.middlePressed = False
        self.mouse.rightPressed = False
        self.up = False
        self.down = False
        
        m = self.mouse
        s  = ''
        if state == GLUT_DOWN:
            m.down = True
            s = 'down'
        else:
            m.up = True
            s = 'up'
        if button == GLUT_LEFT_BUTTON:
            m.leftPressed = True
            print "LEFT " + s
        if button == GLUT_MIDDLE_BUTTON:
            m.middlePressed = True
            print "MIDDLE " + s
        if button == GLUT_RIGHT_BUTTON:
            m.rightPressed = True
            print "RIGHT " + s

        if (m.middlePressed or m.rightPressed) and m.down:
            m.oldMouseDraggedX = x
            m.oldMouseDraggedY = y

    def camera_zoom(self, what = 'in'):
        if what == 'in':
            if (self.zoom > 0.1):
                self.zoom -= 0.1
        elif what == 'out':
            self.zoom += 0.1
        print "Zoom = " + str(self.zoom)
        self.resize(self.width, self.height)
        glutPostRedisplay()

    def keyboard_special(self, key, x, y):
        self._updateMouse(x, y)
        amount = 5
        if key == GLUT_KEY_RIGHT:
            self.transX += amount
            glutPostRedisplay()
        elif key == GLUT_KEY_LEFT:
            self.transX -= amount
            glutPostRedisplay()
        elif key == GLUT_KEY_DOWN:
            self.transY -= amount
            glutPostRedisplay()
        elif key == GLUT_KEY_UP:
            self.transY += amount
            glutPostRedisplay()

    def keyboard(self, key, x, y):
        self._updateMouse(x, y)
        print "keypress = " + key
        if key == chr(27):
            sys.exit(0)
        elif key == 'p':
            glutIdleFunc(self.timestep)
        elif key == 's':
            glutIdleFunc(None)
        elif key == '+':
            self.camera_zoom('in')
        elif key == '-':
            self.camera_zoom('out')
        elif key == 'f':
            self.tscale += .01
        elif key == 'd':
            self.tscale -= .01
        elif key == 'y':
            s = glReadPixels(0, 0, self.width, self.height, GL_RGB, GL_UNSIGNED_BYTE)
            img = Image.new('RGB', (self.width, self.height))
            img.fromstring(s)
            img2 = img.transpose(Image.FLIP_TOP_BOTTOM)
            img2.save("screendump.png")

    def draw(self):
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        
        glPushMatrix()
        #looking at x/y plane - down z axis
        glTranslatef(self.transX, self.transY, self.transZ)
        glRotatef(self.angleY, 0.0, 1.0, 0.0)
        glRotatef(self.angleX, 1.0, 0.0, 0.0)
        
        self.room.render()
        
        glColor3f(0, 0, 0)
        display.draw_axes(20, '1')
        
        self.robot.render()
        glPopMatrix()

        # reference axis
        glPushMatrix()
        glTranslatef(self.zoom*55.0, self.zoom*-50.0, 800.0)

        glRotatef(self.angleY, 0.0, 1.0, 0.0)
        glRotatef(self.angleX, 1.0, 0.0, 0.0)
        display.draw_axes(self.zoom*13, '')
        glPopMatrix()

        glutSwapBuffers()

    def resize(self, w, h):
        self.width = w
        self.height = h
        glViewport(0, 0, w, h)
        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()
        new_w = self.zoom*h/self.scale
        new_h = self.zoom*w/self.scale
        glOrtho (-new_w, new_w, -new_h, new_h, -1000.0, 1000.0)
        glMatrixMode(GL_MODELVIEW)
        glLoadIdentity()

def setup():
    glClearColor(1.0, 1.0, 1.0, 0.0)
    glEnable(GL_DEPTH_TEST)
    #glEnable(GL_LIGHTING)

    # Light property vectors.
    lightAmb = [0.0, 0.0, 0.0, 1.0]
    lightDifAndSpec = [1.0, 1.0, 1.0, 1.0]
    lightPos = [0.0, 1.5, 3.0, 1.0]
    globAmb = [0.2, 0.2, 0.2, 1.0]

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

def create_robot(filename):
    r = json.loads(open(filename).read(), object_hook=lambda d: objects.robot(d))
    return r

def main():
    room = objects.room(200, 200, 200, False)
    robot = create_robot('robots/sample.json')
    s = simulator(robot, room)

    glutInit()
    glutInitDisplayMode(GLUT_RGB | GLUT_DOUBLE | GLUT_DEPTH)
    glutInitWindowSize(s.width, s.height)
    glutInitWindowPosition(100, 100) 

    glutCreateWindow(sys.argv[0])

    setup()

    # mock callback functions that transfer to the simulator
    def _draw():
        s.draw()
    def _mouseMotion(x, y):
        s.mouseMotion(x, y)
    def _mouseDragged(x, y):
        s.mouseDragged(x, y)
    def _mouseControl(button, state, x, y):
        s.mouseControl(button, state, x, y)
    def _keyboard_special(key, x, y):
        s.keyboard_special(key, x, y)
    def _keyboard(key, x, y):
        s.keyboard(key, x, y)
    def _resize(w, h):
        s.resize(w, h)

    glutDisplayFunc(_draw)
    glutKeyboardFunc(_keyboard)
    glutSpecialFunc(_keyboard_special)
    glutMouseFunc(_mouseControl)
    glutPassiveMotionFunc(_mouseMotion)
    glutMotionFunc(_mouseDragged)
    glutReshapeFunc(_resize);  
    glutMainLoop()
    return 0

if __name__ == '__main__':
    main()
