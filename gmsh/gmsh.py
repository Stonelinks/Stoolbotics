import os, subprocess, sys
from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *

from numpy import *

class mesh_obj():
  def __init__(self, _arr):
    self.arr = _arr
    
  def draw(self):
    glPolygonMode(GL_FRONT_AND_BACK, GL_FILL);
    glColor3f(0.1,0.3,0.6)
    glPushMatrix()
    glScalef(0.05, 0.05, 0.05);
    
    
    matAmbAndDif1 = [0.9, 0.0, 0.0, 1.0]
    matAmbAndDif2 = [0.0, 0.9, 0.0, 1.0]
    matSpec = [1.0, 1.0, 1.0, 1.0]
    matShine = [50.0]

    glMaterialfv(GL_FRONT_AND_BACK, GL_AMBIENT_AND_DIFFUSE, matAmbAndDif1)
    glMaterialfv(GL_FRONT_AND_BACK, GL_SPECULAR, matSpec)
    glMaterialfv(GL_FRONT_AND_BACK, GL_SHININESS, matShine)
    
    types = {'2':'triangle','1':'line','15':'point'}
    
    for row in self.arr:
      type = types[str(int(row[0]))]
      
      if type == 'triangle':
        glBegin(GL_TRIANGLES)
        glVertex3f(float(row[1]),float(row[2]),float(row[3]))
        glVertex3f(float(row[4]),float(row[5]),float(row[6]))
        glVertex3f(float(row[7]),float(row[8]),float(row[9]))
        glEnd()
      elif type == 'line':
        glBegin(GL_LINES)
        glVertex3f(float(row[1]),float(row[2]),float(row[3]))
        glVertex3f(float(row[4]),float(row[5]),float(row[6]))
        glEnd()
      elif type == 'point':
        glBegin(GL_POINTS)
        glVertex3f(float(row[1]),float(row[2]),float(row[3]))
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
    #p = subprocess.Popen([binpath, filepath, '-2', '-o', target, '-algo', 'del2d'], stdout=subprocess.PIPE)

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
  
  arr = []
  for _, e in elem_dict.iteritems():
    row = []
    row.append(float(e['rawtype']))
    def _node_append(_row, node):
      _row.append(float(node['x']))
      _row.append(float(node['y']))
      _row.append(float(node['z']))
      return _row
    
    if e['type'] == 'point':
      row = _node_append(row, node_dict[e['n1']])
    elif e['type'] == 'line':
      row = _node_append(row, node_dict[e['n1']])
      row = _node_append(row, node_dict[e['n2']])
    elif e['type'] == 'triangle':
      row = _node_append(row, node_dict[e['n1']])
      row = _node_append(row, node_dict[e['n2']])
      row = _node_append(row, node_dict[e['n3']])
    
    rem_len = (1 + 3 * 3) - len(row)
    for i in range(rem_len):
      row.append(0.0)
    
    arr.append(row)
  
  #for row in numarr:
    #raw_input("")
    #print str(len(row)) + ' : ' + str(row)

  return mesh_obj(arr)
