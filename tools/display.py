#!/usr/bin/env python
from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *

from config import *
from math import *
import sys
import Image
import numpy
from tools import *

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

def draw_rotational_joint(startP, endP, r, link_rotation=0): #draws cylinder from sP to eP
    glPushMatrix()

    #This is the default direction for the cylinders to face in OpenGL - z axis
    z=[ 0, 0, 1 ]
    #Get diff between two points you want cylinder along
    p = startP - endP
    p = [ p[0][0], p[1][0], p[2][0] ] # TODO: FIX! because it's broken.... UGH!!

    #Get CROSS product (the axis of rotation)
    t = cross(z , p)

    #Get angle. LENGTH is magnitude of the vector
    length = sqrt(dot(p, p))
    angle = 180 / PI * acos(dot(z, p) / length)
    glTranslate(endP[0], endP[1], endP[2])
    glRotate(angle,t[0], t[1], t[2])
    if (link_rotation != 0):
        glRotate(link_rotation + 90, 0, 0, 1)
    
    glColor(0, 1, 1)
    sides = r*2
    
    quad = gluNewQuadric()
    gluQuadricOrientation(quad, GLU_OUTSIDE);
    gluCylinder(quad, r, r, length, sides, 1);
    gluDeleteQuadric(quad)
    
    draw_rotational_joint_endCap(r, sides)
    glTranslate(0, 0, length)
    draw_rotational_joint_endCap(r, sides)
    glPopMatrix()

def draw_rotational_joint_endCap(r, sides):
    glColor(0, 1, 1)
    glBegin(GL_TRIANGLE_FAN)
    glVertex3f(0, r/2, 0)
    for angle in arange(0, 2*PI, 2*PI/sides):
        glVertex3f(cos(angle)*r, sin(angle)*r,0)
    glVertex3f(r, 0, 0)
    glEnd()
    
    glColor(0, 0, 0)
    glLineWidth(1.5)
    glBegin(GL_LINE_LOOP)
    for angle in arange(0, 2*PI, 2*PI/sides):
        glVertex3f(cos(angle)*r, sin(angle)*r, 0)
    glEnd()
    
    glBegin(GL_LINES)
    glVertex3f(0, 0, 0)
    glVertex3f(r, 0, 0)
    glVertex3f(r, 0, 0)
    glVertex3f(r-r*.5, r*.5, 0)
    glVertex3f(r, 0, 0)
    glVertex3f(r-r*.5, -r*.5, 0)
    glEnd()
    glLineWidth(1.0)

def draw_prismatic_joint(startP, endP, size):
    glPushMatrix()

    #This is the default direction for the rectangular-prism to face in OpenGL - z axis
    z=[0, 0, 1]
    #Get diff between two points you want rectangular-prism along
    p=startP-endP
    
    p=[p[0][0], p[1][0], p[2][0]] # TODO: FIX! because it's broken.... UGH!!    
    #Get CROSS product (the axis of rotation)
    t = cross(z, p)
    #Get angle. LENGTH is magnitude of the vector
    length = sqrt(dot(p, p))
    angle = 180 / PI * acos(dot(z, p) / length)
    #glTranslate(endP[0],endP[1],endP[2])
    glRotate(angle, t[0], t[1], t[2])
    
    if (length < 5):
        length = 5
    length =- length
    glColor(1, 0, 1)
    glBegin(GL_QUAD_STRIP)

    #Quads 1 2 3 4
    glVertex3f(size/2, -size/2, 0)   #V2
    glVertex3f(-size/2, -size/2, 0)   #V1
    glVertex3f(size/2, -size/2, length)   #V4
    glVertex3f(-size/2, -size/2, length)   #V3
    glVertex3f(size/2, size/2, length)   #V6
    glVertex3f(-size/2, size/2, length)   #V5
    glVertex3f(size/2, size/2, 0)   #V8
    glVertex3f(-size/2, size/2, 0)   #V7
    glVertex3f(size/2, -size/2, 0)   #V2
    glVertex3f(-size/2, -size/2, 0)   #V1
    glEnd()
    
    #Quad 5
    glBegin(GL_QUADS)
    glVertex3f(size/2, size/2, 0)   #V8
    glVertex3f(size/2, size/2, length)   #V6
    glVertex3f(size/2, -size/2, length)   #V4
    glVertex3f(size/2, -size/2, 0)   #V2

    #Quad 6
    glVertex3f(-size/2, size/2, 0)   #V7
    glVertex3f(-size/2, size/2, length)   #V5
    glVertex3f(-size/2, -size/2, length)   #V3
    glVertex3f(-size/2, -size/2, 0)   #V1
    glEnd()
    
    glPopMatrix()
    
def text_at_pos(x, y, z, text, font=GLUT_BITMAP_TIMES_ROMAN_24):
    glRasterPos3f(x, y, z)
    draw_text(text, font)

def draw_text(text, font=GLUT_BITMAP_TIMES_ROMAN_24, color=[0.0, 0.0, 0.0]):
    glColor3f(color[0], color[1], color[2])
    for c in text:
        glutBitmapCharacter(font, ord(c))

def draw_axes(axes_l = 10, number=''):
    
    glLineWidth(8.0)
    glBegin(GL_LINES)

    # x axis, red
    glColor3f(1, 0, 0)
    glVertex3f(0, 0, 0)
    glVertex3f(axes_l, 0, 0)
    
    #glVertex3f(axes_l, 0, 0)
    #glVertex3f(axes_l-(axes_l/5), (axes_l/5), 0)
    
    #glVertex3f(axes_l, 0, 0)
    #glVertex3f(axes_l-(axes_l/5), -(axes_l/5), 0)
    
    # y axis, green
    glColor3f(0, 1, 0)
    glVertex3f(0, 0, 0)
    glVertex3f(0, axes_l, 0)
    
    #glVertex3f(0, axes_l, 0)
    #glVertex3f(0, axes_l-(axes_l/5), (axes_l/5))

    #glVertex3f(0, axes_l, 0)
    #glVertex3f(0, axes_l-(axes_l/5), -(axes_l/5))

    # z axis
    glColor3f(0, 0, 1)
    glVertex3f(0, 0, 0)
    glVertex3f(0, 0, axes_l)

    #glVertex3f(0, 0, axes_l)
    #glVertex3f(0, (axes_l/5), axes_l-(axes_l/5))

    #glVertex3f(0, 0, axes_l)
    #glVertex3f(0, -(axes_l/5), axes_l-(axes_l/5))
    
    glEnd()
    
    text_at_pos(axes_l + 1, 0, 0, 'X' + number)
    text_at_pos(0, axes_l + 1, 0, 'Y' + number)
    text_at_pos(0, 0, axes_l + 1, 'Z' + number)
    glLineWidth(1.0)

def screendump(self, filename="screendump"):
    s = glReadPixels(0, 0, self.w, self.h, GL_RGB, GL_UNSIGNED_BYTE)
    img = Image.new('RGB', (self.w, self.h))
    img.fromstring(s)
    img2 = img.transpose(Image.FLIP_TOP_BOTTOM)
    img2.save(filename + ".jpg")

