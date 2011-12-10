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

<table><tr><td><h4>Command</h4></td><td><h4>Usage</h4></td><td><h4>Description</h4></td></tr><tr><td><b>axis</b></td><td><b>axis &lt;on/off&gt;</b></td><td>Turn robot axis on/off. Providing no arguments toggles the axis.</td></tr><tr><td><b>eval</b></td><td><b>eval &lt;expression&gt;</b></td><td>Return some variable from the simulator. e.g. 'eval robot.P01'. Output might look a little weird.</td></tr><tr><td><b>exit</b></td><td><b>exit or quit</b></td><td>Closes the simulator.</td></tr><tr><td><b>floor</b></td><td><b>floor &lt;on/off&gt;</b></td><td>Turns the floor on and off. Providing no arguments toggles the floor.</td></tr><tr><td><b>ghost</b></td><td><b>ghost &lt;on/off/interval&gt; &lt;number&gt;</b></td><td>turn robot ghosts on/off. If &lt;interval&gt; is present, provide a number to set the ghost interval. Providing no arguments toggles the ghosts.</td></tr><tr><td><b>help</b></td><td><b>help &lt;cmd (optional)&gt;</b></td><td>If &lt;cmd&gt; is provided, display help for that command. Otherwise  it just list all commands.</td></tr><tr><td><b>hide</b></td><td><b>hide</b></td><td>Hides this terminal.</td></tr><tr><td><b>list</b></td><td><b>list</b></td><td>Lists all the robots that can be loaded into the simulator. To add something to this list, just place a valid robot.json file in the 'robots' folder.</td></tr><tr><td><b>load</b></td><td><b>load &lt;robot file&gt;</b></td><td>Loads a robot file into the simulator. Use the 'list' command to see what robots are able to be loaded.</td></tr><tr><td><b>play</b></td><td><b>play &lt;file (optional)&gt;</b></td><td>If &lt;file&gt; is present, the simulator plays that file. Otherwise, it just starts the simulator.</td></tr><tr><td><b>record</b></td><td><b>record &lt;file&gt;</b></td><td>Outputs current arm movements to a file which can be exported or played back later.</td></tr><tr><td><b>screendump</b></td><td><b>screendump</b></td><td>Take a picture of the current screen and save it to disk.</td></tr><tr><td><b>set</b></td><td><b>set &lt;var&gt; &lt;expression&gt;</b></td><td>Sets a symbolic variable in the simulator. e.g. 'set q3 cos(t)', 'set t 0', 'set tscale -.1', 'set P23 [0, 0, l2 + q2]'.</td></tr><tr><td><b>skew</b></td><td><b>skew</b></td><td>Enters skew mode, where the view of the robot and simulation speed can be rapidly adjusted.</td></tr><tr><td><b>status</b></td><td><b>status</b></td><td>Tells you what the simulator is currently doing.</td></tr><tr><td><b>stop</b></td><td><b>stop</b></td><td>Halts the simulaton.</td></tr><tr><td><b>trace</b></td><td><b>trace &lt;on/off/clear/limit&gt; &lt;number&gt;</b></td><td>Turn robot traces on/off, or clear the current set of traces. If the &lt;limit&gt; argument is used, provide a number to set the maximum number of traces.</td></tr></table>

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

<table>
<tr>
<td><h4>Command &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;</h4></td>
<td><h4>Effect</h4></td>
</tr>

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

The simulator also includes functionality to play back and record robot motion.

<!--

####Play back
####Recording

#Implementation
##Overview
##Algorithms
###Symbolics
###Kinematics
###Timestepping
##Drawing the Robot
###Joints
###Links
###Tracing
###Axis
##Misc
###Terminal Implementation
###Recording and Playback
#Closing Remarks
##Future improvements
##Credits

-->
