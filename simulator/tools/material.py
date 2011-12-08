from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *

def green():
    chMat(0.0215, 0.1745, 0.0215, 0.07568, 0.61424, 0.07568, 0.633, 0.727811, 0.633, 0.6)

def gold():
    chMat( 0.24725, 0.1995, 0.0745, 0.75164, 0.60648, 0.22648, 0.628281, 0.555802, 0.366065, 0.4)

def magenta():
    chMat( 0.74725, 0.02995, 0.7745, 0.75164, 0.60648, 0.22648, 0.628281, 0.555802, 0.366065, 0.4)

def red():
    chMat( 0.1745, 0.01175, 0.01175, 0.61424, 0.04136, 0.04136, 0.727811, 0.626959, 0.626959, 0.6)

def blue():
    chMat( 0.0, 0.1, 0.36, 0.0, 0.50980392, 0.50980392, 0.50196078, 0.50196078, 0.50196078, .25)

def black():
    chMat( 0.0, 0.0, 0.0, 0.01, 0.01, 0.01, 0.50, 0.50, 0.50, .25)

def grey():
    chMat( 0.19225, 0.19225, 0.19225, 0.50754, 0.50754, 0.50754, 0.508273, 0.508273, 0.508273, 0.4)

def darkgrey():
    chMat( 0.05375, 0.05, 0.06625, 0.18275, 0.17, 0.22525, 0.332741, 0.328634, 0.346435, 0.3)

def chMat(ambr, ambg, ambb, difr, difg, difb, specr, specg, specb, shine):
    mat = [0, 0, 0, 0]
    mat[0] = ambr
    mat[1] = ambg
    mat[2] = ambb
    mat[3] = 1.0
    glMaterialfv(GL_FRONT, GL_AMBIENT, mat)
    mat[0] = difr
    mat[1] = difg
    mat[2] = difb
    glMaterialfv(GL_FRONT, GL_DIFFUSE, mat)
    mat[0] = specr
    mat[1] = specg
    mat[2] = specb
    glMaterialfv(GL_FRONT, GL_SPECULAR, mat)
    glMaterialf(GL_FRONT, GL_SHININESS, shine * 128.0)
