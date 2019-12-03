#!/usr/bin/env python
from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *

import sys, numpy, math

import tools.material as material
import config

globals()['PI'] = 3.14159265
globals()['pi'] = PI

class point():
    def __init__(self, x, y, z, label=""):
        self.x = x
        self.y = y
        self.z = z
        self.label = label

    def draw(self):
        glPointSize(5)
        glBegin(GL_POINTS)
        glVertex3f(self.x, self.y, self.z)
        glEnd()
        name = self.label
        name += " (" + str(round(self.x, 3)) + ", " + str(round(self.y, 3)) + ", " + str(round(self.z, 3)) + ")"
        text_at_pos(self.x + 1, self.y + 1, self.z + 1, name, GLUT_BITMAP_TIMES_ROMAN_10)

def draw_rotational_joint(startP, endP, r, link_rotation): #draws cylinder from sP to eP
    glPushMatrix()

    # This is the default direction for the cylinders to face in OpenGL - z axis
    z = numpy.array([0.0, 0.0, 1.0])
    
    # Get diff between two points you want cylinder along
    startP = numpy.array(startP, float).transpose()[0]
    endP = numpy.array(endP, float).transpose()[0]
    p = startP - endP
    
    # Get CROSS product (the axis of rotation)
    t = numpy.cross(z, p)

    #Get angle. LENGTH is magnitude of the vector
    length = math.sqrt(numpy.dot(p, p))
    angle = 180 / PI * math.acos(numpy.dot(z, p) / length)
    glRotate(angle, t[0], t[1], t[2])
    glRotate(link_rotation + 90.0, 0.0, 0.0, 1.0)
    if config.enable_lighting:
        material.blue()
    else:
        glColor3f(0, 1.0, 1.0)
    
    sides = r*5
    glTranslate(0, 0, -length/2)
    quad = gluNewQuadric()
    gluQuadricOrientation(quad, GLU_OUTSIDE);
    gluCylinder(quad, r, r, length, sides, 1);
    gluDeleteQuadric(quad)
    
    draw_rotational_joint_endCap(r, sides)
    glTranslate(0, 0, length)
    draw_rotational_joint_endCap(r, sides)
    glPopMatrix()

def draw_rotational_joint_endCap(r, sides):
    if config.enable_lighting:
        material.blue()
    else:
        glColor3f(0, 1.0, 1.0)
    glBegin(GL_TRIANGLE_FAN)
    glVertex3f(0, r/2, 0)
    for angle in numpy.arange(0, 2*PI, 2*PI/sides):
        glVertex3f(math.cos(angle)*r, math.sin(angle)*r,0)
    glVertex3f(r, 0, 0)
    glEnd()

    if config.enable_lighting:
        material.black()
    else:
        glColor3f(0, 0, 0)
    glLineWidth(1.5)
    glBegin(GL_LINE_LOOP)
    for angle in numpy.arange(0, 2*PI, 2*PI/sides):
        glVertex3f(math.cos(angle)*r, math.sin(angle)*r, 0)
    glEnd()

    def arrow(z):
        glVertex3f(0, 0, z)
        glVertex3f(r, 0, z)
        glVertex3f(r, 0, z)
        glVertex3f(r-r*.5, r*.5, z)
        glVertex3f(r, 0, z)
        glVertex3f(r-r*.5, -r*.5, z)

    glBegin(GL_LINES)
    arrow(0.1)
    arrow(-0.1)
    glEnd()
    glLineWidth(1.0)

def draw_prismatic_joint(startP, endP, size):
    glPushMatrix()

    # This is the default direction for the rectangular-prism to face in OpenGL - z axis
    z = [0.0, 0.0, -1.0]
    
    # Get diff between two points you want rectangular-prism along
    p = numpy.array(startP - endP, float).transpose()[0]
    
    # Get CROSS product (the axis of rotation)
    t = numpy.cross(z, p)

    # Get angle. LENGTH is magnitude of the vector
    length = math.sqrt(numpy.dot(p, p))
    angle = 180 / PI * math.acos(numpy.dot(z, p) / length)
    # glTranslate(endP[0],endP[1],endP[2])
    glRotate(angle, t[0], t[1], t[2])
    
    if (length < 5):
        length = 5
    length =- length


    if config.enable_lighting:
        material.magenta()
    else:
        glColor3f(1.0, 0.0, 1.0)

    def quickv(v):
        glVertex3f(v[0], v[1], v[2])
    
    v1 = (-size/2, -size/2, 0)
    v2 = (size/2, -size/2, 0)
    v3 = (-size/2, -size/2, length)
    v4 = (size/2, -size/2, length)
    v5 = (-size/2, size/2, length)
    v6 = (size/2, size/2, length)
    v7 = (-size/2, size/2, 0)
    v8 = (size/2, size/2, 0)

    q1234 = [v2, v1, v4, v3, v6, v5, v8, v7, v2, v1]
    q56 = [v8, v6, v4, v2, v7, v5, v3, v1]
    
    outline = [(v1, v2), (v2, v8), (v8, v7), (v7, v1)]
    outline += [(v1, v3), (v2, v4), (v7, v5), (v8, v6)]
    outline += [(v5, v6), (v6, v4), (v4, v3), (v3, v5)]
    
    #Quads 1 2 3 4
    glBegin(GL_QUAD_STRIP)
    for v in q1234:
        quickv(v)
    glEnd()
    
    #Quad 5 & 6
    glBegin(GL_QUADS)
    for v in q56:
        quickv(v)
    glEnd()
    
    # outline
    glLineWidth(1.5)

    if config.enable_lighting:
        material.black()
    else:
        glColor3f(0, 0, 0)

    glBegin(GL_LINES)
    for line in outline:
        quickv(line[0])
        quickv(line[1])
    
    glEnd()
    glLineWidth(1.0)
    
    glPopMatrix()

def text_at_pos(x, y, z, text, font=GLUT_BITMAP_TIMES_ROMAN_24):
    if config.enable_lighting:
        material.black()
    else:
        glColor3f(0, 0, 0)
    glRasterPos3f(x, y, z)
    draw_text(text, font)

def draw_text(text, font=GLUT_BITMAP_TIMES_ROMAN_24):
    for c in text:
        glutBitmapCharacter(font, ord(c))

def draw_axes(axes_l = 10, number=''):
    glLineWidth(5.0)
    glBegin(GL_LINES)

    # x axis, red

    if config.enable_lighting:
        material.red()
    else:
        glColor3f(1.0, 0, 0)
    glVertex3f(0, 0, 0)
    glVertex3f(axes_l, 0, 0)
    
    # y axis, green

    if config.enable_lighting:
        material.green()
    else:
        glColor3f(0, 1.0, 0)
    glVertex3f(0, 0, 0)
    glVertex3f(0, axes_l, 0)
    
    # z axis

    if config.enable_lighting:
        material.blue()
    else:
        glColor3f(0, 0, 1.0)
    glVertex3f(0, 0, 0)
    glVertex3f(0, 0, axes_l)

    glEnd()
    
    glLineWidth(1.0)
    
    offset = axes_l/7
    
    text_at_pos(offset + axes_l, 0, 0, 'X' + number)
    text_at_pos(0, offset + axes_l, 0, 'Y' + number)
    text_at_pos(0, 0, offset + axes_l, 'Z' + number)
