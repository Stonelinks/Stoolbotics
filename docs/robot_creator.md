#How to specify a robot

##Background

We describe robots in terms of their underlying matrices. For base frame 0 and task frame T, the end goal is to have a single homogenous matrix H0T for the robot, representing both the position and rotational information.

Where H0T = [ R0T P0T ]
            [  0   1  ]

For this to happen, we need to find R0T and P0T in terms of some friendly parameters specified by the user. To do this, we use a widely used and easy to understand format called JSON. Take a look at robots/sample.json to see a sample of how to do this.
