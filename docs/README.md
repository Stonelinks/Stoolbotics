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

<img src="static/1.png" width="640px" height="480px">


#Using the Simulator

##Specifying a Robot

##Command Overview

<table><tr><td><h4>Command</h4></td><td><h4>Usage</h4></td><td><h4>Description</h4></td></tr><tr><td><b>axis</b></td><td><b>axis &lt;on/off&gt;</b></td><td>Turn robot axis on/off. Providing no arguments toggles the axis.</td></tr><tr><td><b>eval</b></td><td><b>eval &lt;expression&gt;</b></td><td>Return some variable from the simulator. e.g. 'eval robot.P01'. Output might look a little weird.</td></tr><tr><td><b>exit</b></td><td><b>exit or quit</b></td><td>Closes the simulator.</td></tr><tr><td><b>floor</b></td><td><b>floor &lt;on/off&gt;</b></td><td>Turns the floor on and off. Providing no arguments toggles the floor.</td></tr><tr><td><b>ghost</b></td><td><b>ghost &lt;on/off/interval&gt; &lt;number&gt;</b></td><td>turn robot ghosts on/off. If &lt;interval&gt; is present, provide a number to set the ghost interval. Providing no arguments toggles the ghosts.</td></tr><tr><td><b>help</b></td><td><b>help &lt;cmd (optional)&gt;</b></td><td>If &lt;cmd&gt; is provided, display help for that command. Otherwise  it just list all commands.</td></tr><tr><td><b>hide</b></td><td><b>hide</b></td><td>Hides this terminal.</td></tr><tr><td><b>list</b></td><td><b>list</b></td><td>Lists all the robots that can be loaded into the simulator. To add something to this list, just place a valid robot.json file in the 'robots' folder.</td></tr><tr><td><b>load</b></td><td><b>load &lt;robot file&gt;</b></td><td>Loads a robot file into the simulator. Use the 'list' command to see what robots are able to be loaded.</td></tr><tr><td><b>play</b></td><td><b>play &lt;file (optional)&gt;</b></td><td>If &lt;file&gt; is present, the simulator plays that file. Otherwise, it just starts the simulator.</td></tr><tr><td><b>record</b></td><td><b>record &lt;file&gt;</b></td><td>Outputs current arm movements to a file which can be exported or played back later.</td></tr><tr><td><b>screendump</b></td><td><b>screendump</b></td><td>Take a picture of the current screen and save it to disk.</td></tr><tr><td><b>set</b></td><td><b>set &lt;var&gt; &lt;expression&gt;</b></td><td>Sets a symbolic variable in the simulator. e.g. 'set q3 cos(t)', 'set t 0', 'set tscale -.1', 'set P23 [0, 0, l2 + q2]'.</td></tr><tr><td><b>skew</b></td><td><b>skew</b></td><td>Enters skew mode, where the view of the robot and simulation speed can be rapidly adjusted.</td></tr><tr><td><b>status</b></td><td><b>status</b></td><td>Tells you what the simulator is currently doing.</td></tr><tr><td><b>stop</b></td><td><b>stop</b></td><td>Halts the simulaton.</td></tr><tr><td><b>trace</b></td><td><b>trace &lt;on/off/clear/limit&gt; &lt;number&gt;</b></td><td>Turn robot traces on/off, or clear the current set of traces. If the &lt;limit&gt; argument is used, provide a number to set the maximum number of traces.</td></tr></table>

##Examples
###Changing the Environment
###Skew mode
###Set
###Playback and Recording
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
