s = []
nl = '\n'
indent = '    '

def line(k, v):
    s.append('"' + str(k) + '" : "' + str(v) + '"')

N = 10

line('N', N)

axis = ['x', 'y', 'z']
for i in range(1, N+1):
    line('h' + str(i), axis[i%3])

for i in range(1, N+1):
    line('q' + str(i), '.5*cos(t + ' + str(i) + '*(2*PI/' + str(N) + '))')

for i in range(1, N+1):
    line('l' + str(i), '20')

indexes = []
for i in range(0, N):
    indexes.append(str(i) + str(i + 1))
indexes.append(str(N) + 'T')

for i in indexes:
    line('P' + i, '[0, 0, l1]')

j = 1
for i in indexes:
    if not j > N:
        line('R' + i, 'rot(h' + str(j) + ', q' + str(j) + ')')
    else:
        line('R' + i, 'eye(3, 3)')
    j += 1
s = '{\n  ' + ',\n  '.join(s) + '\n}'

open("snake.json", 'w').write(s)
