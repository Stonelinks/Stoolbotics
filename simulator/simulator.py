#!/usr/bin/env python
import sys
sys.path += ['.']
from ctypes import util
try:
    from OpenGL.platform import win32
except AttributeError:
    pass

try:
    import Image
except:
    print "looks like you don't have the python imaging library,"
    print "so the screendump command will not work"

from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *

import sys, os, json, numpy, math, time, csv, traceback, socket
import config

import objects
import display
import tools.help as help

globals()['PI'] = 3.14159265
globals()['pi'] = PI

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
        
        # simulator /view dimensions
        self.width = 1000
        self.height = 600
        self.angleY = -135
        self.angleX = 245
        self.transX = 30.0
        self.transY = -30.0
        self.transZ = 25.0
        self.scale = 10
        self.zoom = 1.6
        self.room.scale = self.scale
        
        # time
        self.tscale = .2
        self.t = 0.0
        
        # modes
        self.skew_mode = False
        
        # command line variables
        self.text = []
        self.prompt = ">> "
        self.max_line_chr = 38
        self.cmd = ''
        self.cmd_selection = -1
        self.hide_cli = False
        
        # aux message
        self.aux_msg_enabled = False
        self.aux_msg = ''

        # final setup
        self.robot.t = self.t
        self.robot.timestep()
        self.welcome()
        
        self.file_pointer = None
        self.file = None
        self.state = 'halted'
        self.playback_index = 0
        
    def welcome(self):
        self.response_print('Welcome to stoolbotics!')
        self.response_print('')
        self.response_print('')
        self.response_print('Interact by typing commands or by using the mouse.')
        self.response_print('')
        self.response_print('')
        self.response_print('For a list of commands, type \'help\'')
        self.response_print('')
        self.response_print('')
        self.response_print('For help with a specific command you can type \'help <command name>\'')
        self.response_print('')
        self.response_print('')
        self.response_print('')
        self.response_print('')
        self.command_print('')
        
    def timestep(self):
        if self.state == 'record':
            l = [str(self.t)]
            for link in self.robot.links:
                if not (str(link.index) == str(self.robot.N)): # last link has no param
                    l.append(str(link.q))
            self.file_pointer.write( ', '.join(l) + '\n')
            self.robot.forwardkin()
            self.t += self.tscale
            self.robot.timestep(self.tscale)
        elif self.state == 'playback':
            self.playback_index += 1 #int(self.playback_index + self.tscale)
            try:
                self.t = float(self.file[self.playback_index][0])
                self.robot.to_pos(self.file[self.playback_index][1:])
                self.robot.forwardkin()
            except:
                # end of file
                self.state = 'halted'
                pass
        elif self.state == 'play':
            self.robot.forwardkin()
            self.t += self.tscale
            self.robot.timestep(self.tscale)
        elif self.state == 'server':
            data, addr = self.sock.recvfrom( 1024 ) # buffer size is 1024 bytes
            print "received message:", data
            self.robot.to_pos(data.split(','))
            self.robot.forwardkin()
        elif self.state == 'halted':
            pass
        self.robot.t = self.t
        glutPostRedisplay()
    
    def _updateMouse(self, x, y):
        self.mouse.oldMouseDraggedX = self.mouse.x
        self.mouse.oldMouseDraggedY = self.mouse.y
        self.mouse.x = x
        self.mouse.y = y


    # Mouse motion callback routine.
    def mouseMotion(self, x, y):
        self._updateMouse(x, y)

    def mouseDragged(self, x, y):
        self._updateMouse(x, y)
        
        v1 = math.sin(self.angleX * pi / 180 )
        v2 = math.cos(self.angleY * pi / 180 )
        
        changeX = v1*(x - self.mouse.oldMouseDraggedX)
        changeY = v2*(y - self.mouse.oldMouseDraggedY)

        # why are these mixed up? it breaks without it
        self.angleX += changeY
        self.angleY -= changeX
        
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
        if self.skew_mode:
            amount = 5
            if key == GLUT_KEY_RIGHT:
                self.transX += amount
            elif key == GLUT_KEY_LEFT:
                self.transX -= amount
            elif key == GLUT_KEY_DOWN:
                self.transY -= amount
            elif key == GLUT_KEY_UP:
                self.transY += amount
        else:
            if key == GLUT_KEY_DOWN:
                if not self.cmd_selection == -1:
                    self.cmd_selection += 1
                    try:
                        while self.text[self.cmd_selection][0] != 'c':
                            self.cmd_selection += 1
                    except:
                        pass
                if self.cmd_selection == -1:
                    self.cmd = self.text[-1][1] = ""
            elif key == GLUT_KEY_UP:
                if not -self.cmd_selection == len(self.text):
                    self.cmd_selection -= 1
                    try:
                        while self.text[self.cmd_selection][0] != 'c':
                            self.cmd_selection -= 1
                    except:
                        pass
            try:
                self.cmd = self.text[-1][1] = self.text[self.cmd_selection][1]
            except:
                pass
        glutPostRedisplay()

    def handle_cmd(self, cmd):
        cmd_arr = cmd.strip().split(' ')
        cmd = cmd_arr[0]
        if cmd == '':
            return
        else:
            self.response_print('')
            if cmd == 'play':
                if len(cmd_arr) == 1:
                    if self.state == 'prerecord':
                        self.state = 'record'
                    else:
                        self.state = 'play'
                elif len(cmd_arr) == 2:
                    try:
                        self.file = []
                        for row in csv.reader(open(config.save_path + cmd_arr[1], 'r')):
                            self.file.append(row)
                        self.t = float(self.file[0][0])
                        self.playback_index = 0
                        self.robot.to_pos(self.file[0][1:])
                        self.response_print('openened ' + cmd_arr[1] + ' for playback')
                        self.state = 'playback'
                    except:
                        self.response_print('there was an error opening ' + cmd_arr[1] + ' for playback')
                self.robot.trace = []
            elif cmd == 'stop':
                if self.state == 'record':
                    self.response_print('stopping the recording')
                    try:
                        self.file_pointer.close()
                    except:
                        pass
                self.state = 'halted'
            elif cmd == 'server':
                c2 = cmd_arr[1]
                if c2 == 'start':
                    self.state = 'server'
                    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
                    s.connect(("gmail.com", 80))
                    port = cmd_arr[2]
                    self.response_print('starting server at ' + s.getsockname()[0] + ':' + port)
                    s.close()

                    self.sock = socket.socket( socket.AF_INET, socket.SOCK_DGRAM )
                    self.sock.settimeout(.1)
                    self.sock.bind(("",int(port)))
                elif c2 == 'stop':
                    try:
                        self.sock.close()
                    except:
                        pass
                    self.sock = None
                    self.state = 'halted'
                    self.response_print('stopped server')
                else:
                    self.response_print('unknown server command')
            elif cmd == 'status':
                if self.state == '':
                    self.response_print('the simulator is currently doing nothing')
                else:
                    self.response_print('the simulator is currently in this state: ' + self.state)
            elif cmd == 'record':
                  file  = cmd_arr[1] + '.csv'
                  try:
                      self.file_pointer = open(config.save_path + file, 'a')
                      self.state = 'prerecord'
                      self.response_print('file ' + file + ' opened for recording')
                  except:
                      self.response_print('problem opening that file for recording')
                  self.response_print('')
            elif cmd == 'load':
                try:
                    robot_file = '../robots/' + cmd_arr[1] + '.json'
                    self.robot = create_robot(robot_file)
                    self.robot.timestep()
                except:
                    self.response_print('Error with this robot file: ' + traceback.format_exc())
                print traceback.format_exc()
            elif cmd == 'list':
                for r in os.listdir('../robots'):
                    self.response_print(" " + r.split('.')[0])
            elif cmd == 'axis':
                if len(cmd_arr) == 1:
                    config.enable_axis = not config.enable_axis
                elif cmd_arr[1] == 'on':
                    config.enable_axis = True
                elif cmd_arr[1] == 'off':
                    config.enable_axis = False
                self.draw()
            elif cmd == 'trace':
                if len(cmd_arr) == 1:
                    config.enable_trace = not config.enable_trace
                elif cmd_arr[1] == 'on':
                    config.enable_trace = True
                elif cmd_arr[1] == 'off':
                    config.enable_trace = False
                elif cmd_arr[1] == 'clear':
                    self.robot.trace = []
                elif cmd_arr[1] == 'limit':
                    config.max_trace = int(cmd_arr[2])
            elif cmd == 'ghost':
                if len(cmd_arr) == 1:
                    config.enable_ghost = not config.enable_ghost
                elif cmd_arr[1] == 'on':
                    config.enable_ghost = True
                elif cmd_arr[1] == 'off':
                    config.enable_ghost = False
                elif cmd_arr[1] == 'interval':
                    config.ghost_interval = int(cmd_arr[2])
            elif cmd == 'axis':
                if len(cmd_arr) == 1:
                    config.enable_axis = not config.enable_axis
                elif cmd_arr[1] == 'on':
                    config.enable_axis = True
                elif cmd_arr[1] == 'off':
                    config.enable_axis = False
            elif cmd == 'floor':
                if len(cmd_arr) == 1:
                    config.floor_on = not config.floor_on
                elif cmd_arr[1] == 'on':
                    config.floor_on = True
                elif cmd_arr[1] == 'off':
                    config.floor_on = False
            elif cmd == 'eval':
                try:
                    self.response_print(str(eval('self.' + cmd_arr[1])))
                except:
                    self.response_print("error evaluating command")
            elif cmd == 'set':
                var = cmd_arr[1]
                val = ' '.join(cmd_arr[2:])
                try:
                    if var in self.robot.syms:
                        exec 'self.robot.syms[\'' + var + '\'] = \'' + val + '\''
                        self.response_print(str(eval('self.robot.syms[\'' + var + '\']')))
                        self.robot.trace = []
                    else:
                        exec 'self.' + var + ' = ' + val
                        self.response_print(str(eval('self.' + var)))
                        self.robot.trace = []
                except:
                    self.response_print('error setting expression')
            elif cmd == 'quit' or cmd == 'exit':
                sys.exit(0)
            elif cmd == 'hide':
                self.response_print('hiding this command window')
                self.response_print('press \'t\' to get it back')
                self.hide_cli = True
                self.aux_msg = 'terminal is hidden. press \'t\' to get it back.'
                self.aux_msg_enabled = True
            elif cmd == 'skew':
                self.response_print('entering skew mode:')
                self.response_print(' arrow keys to to translate')
                self.response_print(' \'j\' and \'k\' to zoom in and out')
                self.response_print(' \'f\' and \'d\' speed and slow simulation')
                self.response_print(' \'t\' to quit skew mode')
                self.skew_mode = True
            elif cmd == 'help':
                if len(cmd_arr) == 1:
                    self.response_print("available commands:")
                    for k, _ in help.d.iteritems():
                        self.response_print("  " + k)
                    self.response_print("")
                    self.response_print("type \'help <command>\' to get help on an individual command")
                else:
                    try:
                        helpcmd = help.d[cmd_arr[1]]
                        ref = helpcmd['reference']
                        desc = helpcmd['description']
                        self.response_print("syntax:")
                        self.response_print("  " + ref)
                        self.response_print("")
                        self.response_print("description:")
                        self.response_print("  " + desc)
                    except:
                        self.response_print("couldn't find command")
            elif cmd == 'screendump':
                cs1, cs2 = self.aux_msg_enabled, self.hide_cli
                self.aux_msg_enabled, self.hide_cli = False, True
                self.draw()
                glutPostRedisplay()
                
                try:
                    s = glReadPixels(0, 0, self.width, self.height, GL_RGB, GL_UNSIGNED_BYTE)
                    img = Image.new('RGB', (self.width, self.height))
                    img.fromstring(s)
                    img2 = img.transpose(Image.FLIP_TOP_BOTTOM)

                    strtime = str(time.time()).split('.')[0]
                    filename = config.save_path + "screendump" + strtime + ".png"

                    self.response_print('check out ' + filename + ' in the working directory')
         
                    img2.save(filename)
                    self.aux_msg_enabled, self.hide_cli = cs1, cs2
                except:
                    self.aux_msg_enabled, self.hide_cli = cs1, cs2
                    self.response_print('error taking screenshot, do you have the python imaging library installed?')
            else:
                self.response_print('are you sure that\'s a command?')
            glutPostRedisplay()
            self.response_print('')

    def keyboard(self, key, x, y):
        self._updateMouse(x, y)
        
        if self.skew_mode:
          self.skew_mode = True
          if key == 't':
              self.skew_mode = False
              self.command_print('')
          elif key == 'j':
              self.camera_zoom('in')
          elif key == 'k':
              self.camera_zoom('out')
          elif key == 'f':
              self.tscale += .02
          elif key == 'd':
              self.tscale -= .02
          else:
              self.response_print('in skew mode, type \'t\' to exit')
        else:
            esc = chr(27)
            backspace = chr(8)
            carriagereturn = chr(13)
            newline = chr(10)

            if key in [carriagereturn, newline]:
                if self.cmd[:3] == self.prompt:
                    self.cmd = self.cmd[3:]
                self.handle_cmd(self.cmd)
                self.cmd = ''
                self.command_print(" ")
                self.cmd_selection = -1
                print "enter pressed"
            elif key == backspace:
                self.cmd = self.cmd[:-1]
                self.text[-1][1] = self.cmd
            elif key == esc:
                sys.exit(0)
            else:
                self.cmd += key
                self.text[-1][1] = self.cmd
        if self.hide_cli:
            if key == 't':
                self.command_print("")
                self.hide_cli = False
                self.aux_msg_enabled = False
        glutPostRedisplay()
    
    def multiline_format(self, text):
        line = ''
        s = ''
        for word in text.split(' '):
            if len(line) + len(word) + 1 < self.max_line_chr:
                line += word + ' '
            else:
                s += line
                for _ in range(self.max_line_chr - len(line)):
                    s += ' '
                line = word + ' '
        return s + line
    
    def command_print(self, text):
        if len(text) < self.max_line_chr:
            b = text
        else:
            b = self.multiline_format(text)
        self.text.append(['c', b])
        
    def response_print(self, text):
        if len(text) < self.max_line_chr:
            b = text
        else:
            b = self.multiline_format(text)
        self.text.append(['r', b])
            
    def draw(self):
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        
        glPushMatrix()
        
        #looking at x/y plane - down z axis
        glTranslatef(self.transX, self.transY, self.transZ)
        
        glRotatef(self.angleY, 0.0, 1.0, 0.0)
        glRotatef(self.angleX, 1.0, 0.0, 0.0)
        
        if config.floor_on:
            self.room.render()
        
        glColor3f(0, 0, 0)
        #display.draw_axes(20, '1')
        
        self.robot.render()
        
        glPopMatrix()

        # reference axis
        glPushMatrix()

        glTranslatef(self.zoom*.07*self.width, self.zoom*.07*self.height, 400.0)

        glRotatef(self.angleY, 0.0, 1.0, 0.0)
        glRotatef(self.angleX, 1.0, 0.0, 0.0)
        display.draw_axes(self.zoom*13, '')
        
        glPopMatrix()
        
        if self.aux_msg_enabled:
            glPushMatrix()
            glTranslatef(-self.zoom*.094*self.width, -self.zoom*.094*self.height, 400.0)
            glColor4f(0.0, 0.0, 0.0, 1.0)
            glPushMatrix()
            display.text_at_pos(0, self.zoom*1*3, 0, self.aux_msg, font=GLUT_BITMAP_9_BY_15)
            glPopMatrix()
            glPopMatrix()
    
        if not self.hide_cli:
            self.render_cli()
        
        glutSwapBuffers()

    def render_cli(self):
        glPushMatrix()
        glTranslatef(-self.zoom*.094*self.width, -self.zoom*.094*self.height, 400.0)
        
        glColor4f(0.5, 0.5, 1.0, 0.4)
        x0 = -self.zoom*.0023*self.width
        y0 = -self.zoom*.0023*self.height # bottom left corner
        x1 = self.zoom*.065*self.width # width
        y1 = self.zoom*.19*self.height # height
        
        glBegin(GL_QUADS)
        glVertex3f(x0, y0, -1)
        glVertex3f(x1, y0, -1)
        glVertex3f(x1, y1, -1)
        glVertex3f(x0, y1, -1)
        glEnd()
        
        glColor4f(0.0, 0.0, 0.0, 1.0)
        screen_text = self.text[-100:]
        for text in screen_text:
            if text[0] == 'c':
                if text[1][:len(self.prompt)] != self.prompt:
                    text[1] = self.prompt + text[1]
        i = 0
        for text in reversed(screen_text):
            text = text[1]
            if len(text) <= self.max_line_chr:
                glPushMatrix()
                display.text_at_pos(0, self.zoom*i*3, 0, text, font=GLUT_BITMAP_9_BY_15)
                glPopMatrix()
                i += 1
            else:
                tmp = []
                for j in range(0, len(text), self.max_line_chr):
                    segment = text[j:j + self.max_line_chr]
                    n = self.max_line_chr - len(segment)
                    for _ in range(n):
                        segment += ' '
                    tmp.append(segment)
                tmp.reverse()
                for c in tmp:
                    glPushMatrix()
                    display.text_at_pos(0, self.zoom*i*3, 0, c, font=GLUT_BITMAP_9_BY_15)
                    glPopMatrix()
                    i += 1
        glPopMatrix()

    def resize(self, w, h):
        self.width = w
        self.height = h
        glViewport(0, 0, w, h)
        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()
        new_w = self.zoom*w/self.scale
        new_h = self.zoom*h/self.scale

        glOrtho (-new_w, new_w, -new_h, new_h, -500.0, 500.0)
        glMatrixMode(GL_MODELVIEW)
        glLoadIdentity()

def setup():
    if config.enable_lighting:
        ambient = [1.0, 1.0, 1.0, 1.0]
        #diffuse = [1.0, 1.0, 1.0, 1.0]
        #specular = [1.0, 1.0, 1.0, 1.0]
        #position = [0.0, 0.0, -200.0, 0.0]

        lmodel_ambient = [0.2, 0.2, 0.2, 1.0]
        local_view = [0.0]

        glLightfv(GL_LIGHT0, GL_AMBIENT, ambient)
        #glLightfv(GL_LIGHT0, GL_DIFFUSE, diffuse)
        #glLightfv(GL_LIGHT0, GL_POSITION, position)
        glLightModelfv(GL_LIGHT_MODEL_AMBIENT, lmodel_ambient)
        glLightModelfv(GL_LIGHT_MODEL_LOCAL_VIEWER, local_view)

        #glFrontFace(GL_CW)
        glEnable(GL_LIGHTING)
        glEnable(GL_LIGHT0)
        #glEnable(GL_AUTO_NORMAL)
        #glEnable(GL_NORMALIZE)

    glEnable(GL_BLEND)
    glEnable(GL_POLYGON_SMOOTH)
    glBlendFunc(GL_SRC_ALPHA_SATURATE, GL_ONE)
    glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)
    glEnable(GL_DEPTH_TEST)
    glClearColor(1.0, 1.0, 1.0, 0.0)

    # Enable two vertex arrays: position and normal.
    glEnableClientState(GL_VERTEX_ARRAY)
    glEnableClientState(GL_NORMAL_ARRAY)

def create_robot(filename):
    r = json.loads(open(filename).read(), object_hook=lambda d: objects.robot(d))
    return r

def main(robotfile='default'):
    if robotfile == 'default':
        robotfile = '../robots/' + config.robot_file
    room = objects.room(200, 200, 200, False)
    robot = create_robot(robotfile)
    s = simulator(robot, room)

    glutInit()
    glutInitDisplayMode(GLUT_RGB | GLUT_DOUBLE | GLUT_DEPTH)
    glutInitWindowSize(s.width, s.height)
    glutInitWindowPosition(100, 100) 

    glutCreateWindow('stoolbotics simulator')

    setup()

    # mock callback functions that transfer to the simulator object
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
    glutReshapeFunc(_resize)
    glutIdleFunc(s.timestep)
    glutMainLoop()
    return 0

if __name__ == '__main__':
    main()
