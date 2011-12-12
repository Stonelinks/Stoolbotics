#Introduction
##Welcome

Hello and welcome to the Stoolbotics documentation! Stoolbotics is a general purpose robotic arm and kinematics simulator aimed at being a teaching tool for aspiring roboticists. The motivation for this project was simple: the linear algebra and mathematical concepts behind robotics is difficult for a beginner to understand without any visual context. This is especially true for people who are primarily visual learners.

This tool will hopefully fill a gap in many higher education robotics classrooms. It was designed to be easy to use and compatible with other technologies (like MATLAB). The project itself was conceived halfway through the Fall 2011 semester at RPI by Lucas Doyle, and the implementation was carried out by Lucas Doyle and Scott Peck.

##Features

Stoolbotics has many features that make it attractive to the aspiring roboticst and the higer education robotics classrom. To name a few, Stoolbotics features:

- Easy to use file format for specifying a robot arm
- Ability to visualize any robot that can be specified in such a file
- Compute the forward kinematics of any robot
- Animate and draw paths for arms
- Command line interface within simulator with many useful commands
- Completely customizable simulation environment (time-stepping, etc)
- Ability to record simulator activity
- Ability to playback saved recordings, or even import a recording generated in MATLAB
- Able to be driven in real time from a UDP stream from other programs like MATLAB (includes an example)
- Change variables in the simulator on the fly
- Built in help from simulator command line, and of course this stellar and complete documentation
- Cross platform implementation

##Getting Stoolbotics
###For Windows
####Prebuilt (recommended)

Stoolbotics comes in a pre-packaged, portable build for Windows. You can download it from Lucas' Dropbox here: [http://dl.dropbox.com/u/4428042/simulator.zip](http://dl.dropbox.com/u/4428042/simulator.zip).

Simply unzip and run <code>stoolbotics.bat</code>, and you should be up and running!

####From Source
If you're feeling more adventurous, or want to develop Stoolbotics for Windows, you can still run the simulator through python from the command prompt. You will need to install a few dependencies though. Python (2.7 works best), Numpy, PyOpenGL and (optionally) the python imaging library (PIL) need to all be installed. If you choose not to install PIL, the only functionality that will be effected is the ability to take screenshots from within the simulator.

Once you have everything above installed, you should [download the latest zip](https://github.com/Stonelinks/Stoolbotics/zipball/master) of our code repository from github. Once you have it downloaded, just unzip and run <code>python simulator.py</code> in the simulator directory.

###For Linux

Make sure you have Python, Git, Numpy, PyOpenGL and (optionally) the python imaging library (PIL) installed. Using pip, python's distutils, or your Linux distributions package manager is appropriate here. If you choose not to install PIL, the only functionality that will be affected is the ability to take screenshots from within the simulator.

Next, make a clone of our repository by running <code>git clone https://github.com/Stonelinks/Stoolbotics.git</code>, then just run <code>sh Stoolbotics.sh</code> to fire up the simulator. Any time you wish to update, just run <code>git pull</code> from inside the repository.

###For Mac OSX

OSX isn't officially supported as we don't have a machine we can test on, but if you have a python installation with PyOpenGL, Numpy, and PIL then there is no reason why following the Linux instructions above wouldn't work.

If you just want to grab a copy of the code, you can [download the latest zip](https://github.com/Stonelinks/Stoolbotics/zipball/master) of our code repository from github.

##Quickstart

When you fire up the simulator for the first time, you should see something like what is shown below.

<img src="https://github.com/Stonelinks/Stoolbotics/raw/master/docs/static/1.png" width="780px" height="540px">

You'll notice a robot is loaded into the simulator to start with. This simple three joint arm is called the Phantom Omni, and is defined by the <code>omni.json</code> file in the <code>robots</code> directory. All robot files that the simulator uses are described in such <code>robot.json</code> files in the <code>robots</code> directory. They are simple and easy to understand. Below we have reproduced <code>omni.json</code> as it is first loaded into the simulator:

<pre>
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
</pre>


Let’s look at this file line by line to see how it makes a complete robot object:

- <code>N</code> is first declared to tell the simulator the number of joints to expect in this robot.
- All the joint axes are specified with an <code>h</code> and an index. In this case, shorthand is used (e.g. use of <code>z</code> instead of <code>[0, 0, 1]</code>), but if we wanted a non-standard axis vector we could have used something like <code>[-.1, .2, .4]</code>.
- Angle parameters are specified with a <code>q</code> and an index. These can be completely arbitrary functions of time, static numbers, or whatever you like. These parameters represent how much an axis has rotated or displaced along its axis.
- Link lengths are specified with an <code>l</code> and an index.
- Position vectors tell the simulator how to get from one frame to the next. Additionally, prismatic joints are specified here by including a joint axis parameter (a <code>q</code>) in the vector.
- Finally, the rotation matrices are specified by using the <code>rot()</code> command, which calculates the rotation matrix using the Euler-Rodriguez formula. If no rotation is desired, just specify the identity matrix with the <code>eye()</code> command. Sometimes, for static links it is necessary to specify extra frames that don't have any rotation matrix. If this is the case, you would also just use the <code>eye()</code> command here.

All these variables can be changed once the simulator has started using the <code>set</code> command. There are many more commands available to you in the simulator that can be accessed through the command line. To see a list of them, just type <code>help</code> into the console and you should see a list like what’s below. To view help about a specific command, just type <code>help &lt;command&gt;</code>. A table showing what all the commands are, their syntax, and what they do is also included later on in this documentation.

<img src="https://github.com/Stonelinks/Stoolbotics/raw/master/docs/static/3.png" width="780px" height="540px">

In the above case, we looked at the help for the <code>axis</code> command. Let’s see what it actually does:

<img src="https://github.com/Stonelinks/Stoolbotics/raw/master/docs/static/4.png" width="780px" height="540px">

It is clear then that the axis command can be used to turn on and off the the axis for each intermediary joint coordinate frame. There are many other commands that can be used to manipulate the cosmetics of the simulation environment. These are all covered later in an example section on manipulating the environment. For now though, let’s check out another command, the <code>play</code> command. A simulator is pretty useless unless it can actually simulate things. The <code>play</code> command starts the simulation:

<img src="https://github.com/Stonelinks/Stoolbotics/raw/master/docs/static/5.png" width="780px" height="540px">

To stop the simulator, just type <code>stop</code>. All the variables we set earlier are still modifiable during the runtime. To set these, we use the <code>set</code> command. For example, let’s set q3 to cos(t) by typing <code>set q3 cos(t)</code> into the command prompt:

<img src="https://github.com/Stonelinks/Stoolbotics/raw/master/docs/static/6.png" width="780px" height="540px">

Though you can't see it in a static picture, that joint is now moving pretty fast. Let’s use the <code>set</code> command again to slow it down. Type <code>set tscale .05</code> command and notice that it now goes slower. The value of an appropriate timescale may vary depending on how fast your computer is. <code>skew</code> mode can be enabled to rapidly adjust timescale as well as other parameters. For now though, just use <code>set</code>: 

<img src="https://github.com/Stonelinks/Stoolbotics/raw/master/docs/static/7.png" width="780px" height="540px">

This concludes the quickstart. To do more advanced things like play, record, manipulate the environment, drive the simulator from matlab, etc., check out the examples section!
