<h1>Welcome to Stoolbotics!</h1>
Luke Doyle and Scott Peck

#Introduction
##Welcome

Hello and welcome to the Stoolbotics documentation! Stoolbotics is a general purpose robotic arm and kinematics simulator aimed at being a teaching tool for aspiring roboticists. The motivation for this project was simple: the linear algebra and mathematical concepts behind robotics is difficult for a beginner to understand without any visual context. This is especially true for people who are primarily visual learners.

This tool will hopefully fill a gap in many higher education robotics classrooms. It was designed to be easy to use, compatible with other technologies (like MATLAB). The project itself was conceived halfway through the Fall 2011 semester at RPI by Lucas Doyle, and the implementation was carried out by Lucas Doyle and Scott Peck.

##Features

Stoolbotics has many features that make it attractive to the aspiring roboticst and robotics professor. To name a few:

- Easy to use file format for specifying a robot arm
- Ability to visualize any robot that can be specified in such a file
- Compute the forward kinematics of any robot
- Animate and draw paths for robots
- Command line interface within simulator with many useful commands
- Completley customizable simulation environment (timestepping, etc)
- Ability to record simulator activity
- Ability to playback saved recordings, or even import a recording generated in MATLAB
- Change variables in the simulator on the fly
- Built in help from simulator command line, and of this stellar documentation
- Cross platform

##Getting Stoolbotics
###For Windows
####Prebuilt (reccomended)

Stoolbotics comes in a pre-packaged, portable build for Windows. You can download it from Lucas' Dropbox here: [http://dl.dropbox.com/u/4428042/simulator.zip](http://dl.dropbox.com/u/4428042/simulator.zip).

Simply unzip and run stoolbotics.bat, and you should be up and running!

####From Source
If you're feeling more adventerous, or want to develop stoolbotics for Windows, you can still run the simulator through python. You will need to install a few dependencies though. You will need to have python (2.7 works best), numpy, PyOpenGL and (optionally) the python imaging library (PIL) installed. If you choose not to install PIL, the only functionality that will be effected is the ability to take screenshots from within the simulator.

Once you have everything above installed, you should [download the latest zip](https://github.com/Stonelinks/Stoolbotics/zipball/master) of our code repository. Once you have it downloaded, just unzip and run <code>python simulator.py</code> in the simulator directory.

###For Linux

Make sure you have Python, git, numpy, PyOpenGL and (optionally) the python imaging library (PIL) installed. If you choose not to install PIL, the only functionality that will be effected is the ability to take screenshots from within the simulator.

Make a clone of our repository by running <code>git clone https://github.com/Stonelinks/Stoolbotics.git</code>, then just run <code>sh stoolbotics.sh</code> to fire up the simulator.

###For Mac OSX

OSX isn't officially supported as we don't have a machine we can test on, but if you have a python installation with PyOpenGL, numpy, and PIL then there is no reason why following the Linux instructions above wouldn't work.

If you just want to grab a copy of the code, you can [download the latest zip](https://github.com/Stonelinks/Stoolbotics/zipball/master) of our code repository.

##Quickstart

When you fire up the simulator for the first time, you should see something like what is shown below.

<img src="https://github.com/Stonelinks/Stoolbotics/raw/master/docs/static/1.png" width="780px" height="540px">

You'll notice a robot is loaded into the simulator to start with. This simple three joint arm is called the phantom omni, and is defined by the 'omni.json' file in the robots directory. All robot files that the simulator uses are described in such robot.json files. They are simple and easy to understand. Below we have reproduced omni.json as it is first loaded into the simulator:

        "N" : "3",
        
        "h1" : "z",
        "h2" : "x",
        "h3" : "x",
        
        "q1" : ".1*t",
        "q2" : ".1*cos(t)",
        "q3" : ".001*t + .2*sin(t)",
        
        "l1" : "40",
        "l2" : "50",
        "l3" : "50",
        
        "P01" : "[0, 0, 0]",
        "P12" : "[0, 0, l1]",
        "P23" : "[0, l2, 0]",
        "P3T" : "[0, l3, 0]",
        
        "R01" : "rot(h1, q1)",
        "R12" : "rot(h2, q2)",
        "R23" : "rot(h3, q3)",
        "R3T" : "eye(3, 3)"

Lets look at this file line by line to see how it makes a complete robot object:

- "N" is first declaired to tell the simulator the number of joints to expect in this robot.
- All the joint axes are specified with an "h" and an index. In this case, shorthand is used (e.g. use of "z" instead of "[0, 0, 1]"), but if we wanted a non-standard axis vector we could have used something like "[-.1, .2, .4]".
- Angle parameters are specified with a "q" and an index. These can be completley arbitrary functions of time, static numbers, or whatever you like. These parameters represent how much an axis has rotated or displaced along its axis.
- Link lengths are specified with an "l" and an index.
- Position vectors tell the simulator how to get from one frame to the next. Additionally, prismatic joints are specified here by including a joint axis parameter (a "q").
- Finally, the rotation matricies are specified by using the <code>rot()</code> command, which calculates the rotation matric using the euler-rodrigues formula. If no rotation is desired, just specify the identity matrix with the <code>eye()</code> command.

All these variables can be changed once the simulator has started using the <code>set</code> command. There are many more commands available to you in the simulator that can be accessed through the command line. To see a list of them, just type <code>help</code> into the console and you should see a list like whats below. To view help about a specific command, just type <code>help &lt;command&gt;</code>.

<img src="https://github.com/Stonelinks/Stoolbotics/raw/master/docs/static/3.png" width="780px" height="540px">

In this case, we looked at the help for the <code>axis</code> command. Lets see what it does:

<img src="https://github.com/Stonelinks/Stoolbotics/raw/master/docs/static/4.png" width="780px" height="540px">

It is then clear that the axis command can be used to turn on and off the the axis for each intermediary joint coordinate frame. There are many other commands that can be used to manipulate the cosmetics of the simulation environment, which will be covered in an example later on. For now though, lets check out another command, the <code>play</code> command. A simulator is pretty useless unless it can actually simulate things. The <code>play</code> command starts the simulaton:

<img src="https://github.com/Stonelinks/Stoolbotics/raw/master/docs/static/5.png" width="780px" height="540px">

To stop the simulator, just type <code>stop</code>. All the varibles we set earlier are still modifiable during the runtime. To set these, we use the <code>set</code> command. For example, lets set q3 to cos(t) by typing <code>set q3 cos(t)</code>:

<img src="https://github.com/Stonelinks/Stoolbotics/raw/master/docs/static/6.png" width="780px" height="540px">

Though you can't see it in a static picture, that joint is now moving pretty fast. Lets use the <code>set</code> command again to slow it down. Type <code>set tscale .05</code> command and notice that it now goes slower. The value of an appropriate timescale may vary depending on how fast your computer is.

<img src="https://github.com/Stonelinks/Stoolbotics/raw/master/docs/static/7.png" width="780px" height="540px">

To do more advanced things like play, record, manipulate the environment, etc., check out the examples section!
#Using the Simulator

##Specifying a Robot

###Robot.json File
As covered in the quickstart, robots are specified in json files that contain sections in it for defining various aspects of a robot to be simulated. Here is an example file for the phantom omni and the explenation again in case you skipped over the quickstart:

        "N" : "3",
        
        "h1" : "z",
        "h2" : "x",
        "h3" : "x",
        
        "q1" : ".1*t",
        "q2" : ".1*cos(t)",
        "q3" : ".001*t + .2*sin(t)",
        
        "l1" : "40",
        "l2" : "50",
        "l3" : "50",
        
        "P01" : "[0, 0, 0]",
        "P12" : "[0, 0, l1]",
        "P23" : "[0, l2, 0]",
        "P3T" : "[0, l3, 0]",
        
        "R01" : "rot(h1, q1)",
        "R12" : "rot(h2, q2)",
        "R23" : "rot(h3, q3)",
        "R3T" : "eye(3, 3)"

- "N" is first declaired to tell the simulator the number of joints to expect in this robot.
- All the joint axes are specified with an "h" and an index. In this case, shorthand is used (e.g. use of "z" instead of "[0, 0, 1]"), but if we wanted a non-standard axis vector we could have used something like "[-.1, .2, .4]".
- Angle parameters are specified with a "q" and an index. These can be completley arbitrary functions of time, static numbers, or whatever you like. These parameters represent how much an axis has rotated or displaced along its axis.
- Link lengths are specified with an "l" and an index.
- Position vectors tell the simulator how to get from one frame to the next. Additionally, prismatic joints are specified here by including a joint axis parameter (a "q").
- Finally, the rotation matricies are specified by using the <code>rot()</code> command, which calculates the rotation matric using the euler-rodrigues formula. If no rotation is desired, just specify the identity matrix with the <code>eye()</code> command.

###Loading a robot into the simulator

First, all robots are pulled from the robots directory in root directory of the simulator. I reccomend actually copying an existing one and modifying it to suit your needs.

Once you have written a robot.json file, there are two commands that will help you out getting it into the simulator. First, use the <code>list</code> command to see what robots the simulator think's exists. You should see a list containing the omni, puma560, etc. and whatever else you have put in the robots directory. Next, use the <code>load</code> command to load your robot.

##Command Overview

<table><tr><td><h4 style="width: 100px;">Command</h4></td><td><h4 style="width: 300px;">Usage</h4></td><td><h4>Description</h4></td></tr><tr><td><b>axis</b></td><td><b>axis &lt;on/off&gt;</b></td><td>Turn robot axis on/off. Providing no arguments toggles the axis.</td></tr><tr><td><b>eval</b></td><td><b>eval &lt;expression&gt;</b></td><td>Return some variable from the simulator. e.g. 'eval robot.P01'. Output might look a little weird.</td></tr><tr><td><b>exit</b></td><td><b>exit or quit</b></td><td>Closes the simulator.</td></tr><tr><td><b>floor</b></td><td><b>floor &lt;on/off&gt;</b></td><td>Turns the floor on and off. Providing no arguments toggles the floor.</td></tr><tr><td><b>ghost</b></td><td><b>ghost &lt;on/off/interval&gt; &lt;number&gt;</b></td><td>turn robot ghosts on/off. If &lt;interval&gt; is present, provide a number to set the ghost interval. Providing no arguments toggles the ghosts.</td></tr><tr><td><b>help</b></td><td><b>help &lt;cmd (optional)&gt;</b></td><td>If &lt;cmd&gt; is provided, display help for that command. Otherwise  it just list all commands.</td></tr><tr><td><b>hide</b></td><td><b>hide</b></td><td>Hides this terminal.</td></tr><tr><td><b>list</b></td><td><b>list</b></td><td>Lists all the robots that can be loaded into the simulator. To add something to this list, just place a valid robot.json file in the 'robots' folder.</td></tr><tr><td><b>load</b></td><td><b>load &lt;robot file&gt;</b></td><td>Loads a robot file into the simulator. Use the 'list' command to see what robots are able to be loaded.</td></tr><tr><td><b>play</b></td><td><b>play &lt;file (optional)&gt;</b></td><td>If &lt;file&gt; is present, the simulator plays that file. Otherwise, it just starts the simulator.</td></tr><tr><td><b>record</b></td><td><b>record &lt;file&gt;</b></td><td>Outputs current arm movements to a file which can be exported or played back later.</td></tr><tr><td><b>screendump</b></td><td><b>screendump</b></td><td>Take a picture of the current screen and save it to disk.</td></tr><tr><td><b>set</b></td><td><b>set &lt;var&gt; &lt;expression&gt;</b></td><td>Sets a symbolic variable in the simulator. e.g. 'set q3 cos(t)', 'set t 0', 'set tscale -.1', 'set P23 [0, 0, l2 + q2]'.</td></tr><tr><td><b>skew</b></td><td><b>skew</b></td><td>Enters skew mode, where the view of the robot and simulation speed can be rapidly adjusted.</td></tr><tr><td><b>status</b></td><td><b>status</b></td><td>Tells you what the simulator is currently doing.</td></tr><tr><td><b>stop</b></td><td><b>stop</b></td><td>Halts the simulaton.</td></tr><tr><td><b>trace</b></td><td><b>trace &lt;on/off/clear/limit&gt; &lt;number&gt;</b></td><td>Turn robot traces on/off, or clear the current set of traces. If the &lt;limit&gt; argument is used, provide a number to set the maximum number of traces.</td></tr></table>

##Examples

###Changing the Environment

The cosmetics of the simulation environment are highly configurable:

- Axis
    - The joint coordinate frame axis display can be turned on and off with the use of the <code>axis</code> command.
- Floor
    - The floor in the simulator can be turned on and off with the use of the <code>floor</code> command.
- Ghosts
    - A 'ghost' is a shadow of a robot in a previous articulated position. Use the <code>ghost</code> command to control them.
    - The interval of when ghosts appear can be set with <code>ghost interval &lt;somenumber&gt;</code>.
- Traces
    - The trace that the robot leaves behind is completely configurable with the <code>trace</code> command.
    - The number of traces saved can be set by executing <code>trace limit &lt;somenumber&gt;</code>.
    - Finally, traces can get kind of ugly and annoying sometimes, so it is nice to be able to clear them by running <code>trace clear</code>.

Here is an example of some simulation environment manipulation and the result:

<img src="https://github.com/Stonelinks/Stoolbotics/raw/master/docs/static/8.png" width="780px" height="540px">

###Skew mode

Skew mode allows you to rapidly adjust where the camera is positioned in the simulation as well as adjust the timestep. To enter skew mode, just type <code>skew</code>. From there you can use the arrow keys to translate the camera up or down, use 'f' and 'd' to speed up or slow down the simulation, and finally 'j' and 'k' to zoom in and out. While in skew mode, none of the other commands work, so to exit you need to type 't'.

###Set

As you can see from the quickstart, the set command is highly versatile. You can set any variable in the simulator or the robot with this command. Here are some examples of clever ways to use the set command:

<table><tr><td><h4 style="width: 300px;">Command</h4></td><td><h4>Effect</h4></td></tr>
<tr>
<td><pre>set t 0</pre></td>
<td>Resets the time in the simulator back to time = 0.</td>
</tr>

<tr>
<td><pre>set tscale 0.05</pre></td>
<td>Manually sets the timescale in the simulator (the same effect could also be done with the skew command).</td>
</tr>

<tr>
<td>
<pre>
set q1 0
set q2 0
set q3 0
(etc ...)
</pre>
</td>
<td>Sets all joints in the robot to zero position.</td>
</tr>

<tr>
<td>
<pre>
set h1 x
set h2 [1, 1, 1]
set h3 z
(etc ...)
</pre>
</td>
<td>Sets all joints axis in the robot to arbitrary vectors. use of shortcuts like "x" is entirely optional, you can do things like [1, 0, 0] and accomplish the same effect.</td>
</tr>

<tr>
<td>
<pre>
set l1 50
</pre>
</td>
<td>Set link one to be 50.</td>
</tr>

<tr>
<td>
<pre>
set P12 [0, 0, l2 + q2]
</pre>
</td>
<td>Make a prismatic joint in the Z direction from frame one to frame two.</td>
</tr>

<tr>
<td>
<pre>
set R12 eye(3, 3)
</pre>
</td>
<td>Sets R12 to be the identity matrix, effectively creating a static link.</td>
</tr>
</table>


###Playback and Recording

The simulator also includes functionality to play back and record robot motion through the <code>play</code> and <code>record</code> commands.

####File Format

The file format that stoolbotics uses to store robot activity is very straightforward. It is a standard .csv file, where each row is a slice of time. The first entry in each row is always time, but since the timescale can be adjusted in the simulator, this column almost doesn't matter. The remaining entries in the row coorespond to to joint angles (in radians) starting from the first joint out to the end of the arm. An example snippit for a three joint arm is shown below:

<pre>

0.0, 0.1, 0.0540302305868, 0.169294196962
0.2, 0.02, 0.0980066577841, 0.039933866159
0.4, 0.04, 0.0921060994003, 0.0782836684617
0.6, 0.06, 0.082533561491, 0.113528494679
0.8, 0.08, 0.0696706709347, 0.14427121818
1.0, 0.1, 0.0540302305868, 0.169294196962
1.2, 0.12, 0.0362357754477, 0.187607817193
1.4, 0.14, 0.01699671429, 0.198489945998
1.6, 0.16, -0.00291995223013, 0.201514720608
1.8, 0.18, -0.0227202094693, 0.196569526176
2.0, 0.2, -0.0416146836547, 0.183859485365
2.2, 0.22, -0.0588501117255, 0.163899280764
2.4, 0.24, -0.0737393715541, 0.13749263611
2.6, 0.26, -0.0856888753369, 0.105700274364
2.8, 0.28, -0.0942222340669, 0.0697976300312
3.0, 0.3, -0.09899924966, 0.031224001612

</pre>

####Recording

Recording is as easy as using the <code>record</code> command. Providing an argument to the command, such as "example" will automatically start recording to a file called "example.csv" in the root of stoolbotics.

####Playback

When playing back, all you need to do is use the <code>play</code> command with the filename you want to play back. For example, after recording to "example", you could type <code>play example.csv</code> to start playing what was recorded in the file.
#Implementation
##Overview

Many technical challenges were overcome during the development of stoolbotics. To take a look at the code yourself, here is a [link](https://github.com/Stonelinks/Stoolbotics) to our github. Choice algorithms and segments of the code will be explained and highlited in this section.

##Symbolics

In order to properly make use of the configuration file, a symbolic solving engine had to me implemented in python to evaluate symbolic expressions. This means that given a symbolic string like 'rot(h1, q1)', the solver knows what the values of h1 and q1 are, and knows how to call the rot() function on them and generate a numeric answer. This solver is also used for evaluating joint parameters as a finction of time. For example, given the joint parameter .001*cos(t) + PI / 2, spit out the correct answer for a given time t, and be able to recognize special cases of variables (in this case PI) that are not first order robot class variables.

To accomplish this, the robot object contains two dictionaries, \_d and syms. As you probably could have guessed, syms contains the symbolic expressions much in the same state as they are in the configuration file. At every time step, this syms dictionary is parsed and evaluated into numeric values that are entered into the other dictionary, \_d. This has the advantage of being able to set any string into the syms dictionary, and then being to immediately see its effect on the simulation without having to restart the simulator. This is indeed how the 'syms' command in the simulator works for variables inside the robot object.

Once every timestep, a function called eval_syms() is called. This function goes through the syms dictionary and uses string manipulation, substitution and finally the pythin eval() command to turn everything into numerical answers. These numerical answers are plugs into \_d. It is from \_d that the values for the various links are assigned, which ultimately dictate how the robot is drawn. Additionally, after evaluating \_d, a function called sync_d() is called that simply uses the built in python setattr() function to make each entry in \_d a class variable within the robot object instance. This allows calling of things like robot.P01 to work instead of having to do robot._d['P01'] every time you want to get at a varable inside \_d.

Links are then constructed from all these variables as a convienent way to group related variables together. These links contain things like a joint's rotation matrix, position vector, joint parameter and joint axis. As we'll see later on, links are used mostly for accessing information about a robot arm.

##Kinematics

Once all symbolics for the robot are evaluated, it is actually pretty easy to solve for the forward kinematics of the arm. We use the product of exponentials approach to solve this. First, computing R0T is as simple as this:

<pre>
robot.R0T = eye(3, 3)
for link in robot.links:
    robot.R0T = dot(robot.R0T, link.R)
</pre>

As you can see, R0T starts out as the identity matrix. The links of the robot then are traversed in order from the base to the end, and along the way the current R0T is multiplied by the link's individual rotation matrix (which comes from \_d). When this is all done, the resulting matrix is the correct R0T.

For positions, the algorithm is a bit more involved:

<pre>
tmp = eye(3,3)
robot.P0T = zeros((3, 1))
p = None
for link in robot.links:
    robot.P0T += dot(tmp, link.P)
    tmp = dot(tmp, link.R)
    
    p = (robot.P0T[0][0], robot.P0T[1][0], robot.P0T[2][0])
    self.verts.append(p)
</pre>

First, a few variables are initialized. tmp is the temporary rotation matrix for all links up until the current iteration. It starts off as the identity matrix. Second, the overall position vector, P0T, starts out as a three by one zero vector. Next, for each link in the robot arm, the representation of the link's position vector in terms of the base frame is added to the current position vector. This is done by using the dot product of the tmp rotation matrix and the link's position vector. The temporary rotation matrix is then updated, and the current position vector is appended to the verts list, which contains all the robot's verticies for the current timestep. This list is later used to draw things like the arm ghosts and trace.

##Timestepping

##Drawing the Robot
###Joints
When drawing the robot in a certain configuration in OpenGL, it is necessary to indicate which joints are rotational or prismatic. Also have to distinguish the links from the prismatic joints. This is done by using a gluCylinder along the axis of the joint. Unfortunately, OpenGL can only use gluCylinder along the Z axis. To accommodate this as our frame is independent of our rotation axis, we calculate the rotation need from the the axis we want to draw along (some arbitrary axis - the rotation axis within our frame) to the Z vector within this same frame. Once this is rotated, drawing along the Z axis inside this new frame will draw along the rotation axis in the old frame. After the cylinder is drawn, endcaps were drawn so enclose this cylinder. Using a for loop to iterate around a circle of points for gl_triangle_fan. This is done by using glPushMatrix and glPopMatrix with all the drawing taking place within the new calculated rotated matrix. For prismatic joints, a method was developed to draw a rectangular prism along an arbitrary axis. This was done using a length and width/height (square area) as well as a start and end point. From there, a matrix is push onto the model view which is the rotation from the vector (end-start, same as shown above) to the Z axis. Then, a simple gl_quads was used to draw the 6 faces of the rectangular prism of the size provided and the matrix popped off. After the joint is drawn, the frame is rotated along the axis of rotation by the amount specified using glRotate. Then it is translated using glTranslate along the link which is representative in the rotated frame so no additional calculations are needed. Now that the frame is at the next joint, the process is repeated till all joints are displayed. This process works off of the stack pushing and popping matrices. Joint 3 is related to Joint 2 which is a rotation and translation from Joint 1. Problems encountered while drawing the robot include the drawing of the gluClinder along the axis or rotation as the rotation matrix needed to draw along the Z axis was causing issues due math errors in the passing of parameters  to the cross and dot product. Another issue was trying to draw the entire robot in one frame as python was already calculating all the necessary information. This led to complexity issues that were troublesome to debug and even harder to comment and follow. The last troublesome part was using glLoadMatrix to force OpenGL to load a matrix that python had already calculated for internal purposes. The problem became known when rounding errors in python of the rotation matrix caused the determinate not to be 1.000 in all cases which would cause OpenGL to clip triangles of the screen and paint the pixels white.

###Links
###Tracing
###Axis
##Misc
###Terminal Implementation
###Recording and Playback
#Closing Remarks
##Future improvements
##Credits

