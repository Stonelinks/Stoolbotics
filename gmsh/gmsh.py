import os, subprocess, sys
from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *

class mesh_obj():
  def __init__(self, _nodes, _elements):
    self.nodes = _nodes
    self.elements = _elements
      
  def draw(self):
    glPolygonMode(GL_FRONT_AND_BACK, GL_FILL);
    glColor3f(0.1,0.3,0.6)
    glPushMatrix()
    glScalef(0.05, 0.05, 0.05);
    for k, v in self.elements.iteritems():
      if v['type'] == 'triangle':
        glBegin(GL_LINES)
        n1 = self.nodes[v['n1']]
        n2 = self.nodes[v['n2']]
        n3 = self.nodes[v['n3']]
        glVertex3f(float(n1['x']), float(n1['y']), float(n1['z']))
        glVertex3f(float(n2['x']), float(n2['y']), float(n2['z']))
        glVertex3f(float(n3['x']), float(n3['y']), float(n3['z']))
        glEnd()
      if v['type'] == 'line':
        glBegin(GL_LINES)
        n1 = self.nodes[v['n1']]
        n2 = self.nodes[v['n2']]
        glVertex3f(float(n1['x']), float(n1['y']), float(n1['z']))
        glVertex3f(float(n2['x']), float(n2['y']), float(n2['z']))
        glEnd()
      elif v['type'] == 'point':
        glBegin(GL_POINTS)
        n1 = self.nodes[v['n1']]
        glVertex3f(float(n1['x']), float(n1['y']), float(n1['z']))
        glEnd()
    glPopMatrix()
    
  def _draw(self):
    glPolygonMode(GL_FRONT_AND_BACK, GL_FILL);
    glShadeModel(GL_SMOOTH)
    glColor3f(0.1,0.3,0.6)
    glPushMatrix()
    glScalef(0.05, 0.05, 0.05);
    glBegin(GL_POLYGON)
    for _, n1 in self.nodes.iteritems():
      glVertex3f(float(n1['x']), float(n1['y']), float(n1['z']))
    glEnd()
    glPopMatrix()
    
def convert(filename):
  currpath = os.path.dirname(__file__)
  print "processing file " + filename
  binpath = os.path.join(currpath, 'gmsh')
  filepath = os.path.abspath(filename)
  target = os.path.join(currpath, filename.split('/')[-1:][0] + '.msh')
  try:
    f = open(target, 'r')
    print "found cached mesh!"
  except IOError:
    p = subprocess.Popen([binpath, filepath, '-2', '-o', target], stdout=subprocess.PIPE)
    print "calling gmsh... please be patient"
    try:
      out = p.stdout.read().strip() + p.stderr.read().strip()
    except:
      pass
    f = open(target, 'r')
  lines = f.read()
  nodes = lines[lines.find('$Nodes'):lines.find('$EndNodes')]
  elements = lines[lines.find('$Elements'):lines.find('$EndElements')]
  
  node_dict = {}
  for node in nodes.split('\n'):
    if len(node.split(' ')) > 1:
      n = node.split(' ')
      node_dict[n[0]] = {'x' : n[1], 'y' : n[2], 'z' : n[3]}
    else:
      print "discard: " + str(node)
  
  elem_dict = {}
  for elem in elements.split('\n'):
    if len(elem.split(' ')) > 1:
      e = elem.split(' ')
      tmp = {}
      tmp['rawtype'] = e[1]
      if tmp['rawtype'] == '15':
        tmp['type'] = 'point'
        tmp['n1'] = e[-1:][0]
      elif tmp['rawtype'] == '1':
        tmp['type'] = 'line'
        tmp['n1'] = e[-1:][0]
        tmp['n2'] = e[-2:][0]
      elif tmp['rawtype'] == '2':
        tmp['type'] = 'triangle'
        tmp['n1'] = e[-1:][0]
        tmp['n2'] = e[-2:][0]
        tmp['n3'] = e[-3:][0]
      else:
        print "discard: " + str(elem)
      elem_dict[e[0]] = tmp
      
    else:
      print "discard: " + str(elem)

  return mesh_obj(node_dict, elem_dict)
  #print str(node_dict)
  #print str(elem_dict)
