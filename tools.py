#!/usr/bin/env python
# lucas doyle
from numpy import *

# pads a matrix with zeros -- e g the matrix:
#  | 1 2 3 |
#  | 4 5 6 |
#  | 7 8 9 |
#
# would be this after calling zeros_resize(matrix, 4):
#  | 1 2 3 0 |
#  | 4 5 6 0 |
#  | 7 8 9 0 |
#  | 0 0 0 0 |

def zeros_resize(matrix, dim):
  rows = matrix.shape[0]
  cols = matrix.shape[1]
  if rows == dim or cols == dim:
    return matrix
  else:
    m = zeros((dim, dim), float)
    result = r_[matrix, m[rows:, :cols]]
    result = c_[result, m[:, cols:]]
    return result
    
# hat operator for 3x1 vector
def hat(k):
  return array([[0, -k[2][0], k[1][0]], [k[2][0], 0, -k[0][0]], [-k[1][0], k[0][0], 0]])

# generates the (dim by dim) rotation matrix for 3x1 vector for theta degrees
def rot(vector, theta, dim=3):
  vector = vector/linalg.norm(vector);
  rot = identity(dim, float)
  rot += zeros_resize(sin(theta) * hat(vector), dim)
  rot += zeros_resize(dot(dot(1-cos(theta), hat(vector)), hat(vector)), dim)
  return rot
