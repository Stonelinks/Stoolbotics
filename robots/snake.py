"""
An example of how to programmatically create arms.
"""

s = [] # every line starts out by getting kept in this list

# this function just adds key, value pairs to the list
def line(k, v):
    s.append('"' + str(k) + '" : "' + str(v) + '"')

# number of joints
N = 10
line('N', N)

# all the joint axis
axis = ['x', 'y', 'z']
for i in range(1, N+1):
    line('h' + str(i), axis[i%3])

# all the joint params
for i in range(1, N+1):
    line('q' + str(i), '.5*cos(t + ' + str(i) + '*(2*PI/' + str(N) + '))')

# all the links
for i in range(1, N+1):
    line('l' + str(i), '20')

# generate indexes, a list of '01', '12', '23', ... , 'NT'
indexes = []
for i in range(0, N):
    indexes.append(str(i) + str(i + 1))
indexes.append(str(N) + 'T')

# position vectors
for i in indexes:
    line('P' + i, '[0, 0, l1]')

# all the rotation matricies. note the last one is the identity matrix
j = 1
for i in indexes:
    if not j > N:
        line('R' + i, 'rot(h' + str(j) + ', q' + str(j) + ')')
    else:
        line('R' + i, 'eye(3, 3)')
    j += 1

# format the list into a string that can be written to a json file
s = '{\n  ' + ',\n  '.join(s) + '\n}'

# write the json file
f = open("snake.json", 'w')
f.write(s)
f.close()
