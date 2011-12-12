#Closing Remarks

##Future Improvements

There are a number of future improvements that can be made the simulator.

First, we really want to implement closed loop control from external applications such as MATLAB (IE not having to generate a file to be played back). In an effort to make this as cross platform as possible, the current plan is to do this using UDP sockets. Essentially, a program like MATLAB would send a list of joint angles to a UDP socket that the sumilator is listening on. Once the simulator receives the message, it would move the arm to that position.

Second, a user scripting environment would have been nice. This could allow people to write scripts that do things like inverse kinematics, workspace calculations, finding DH parameters, etc. The simulator would have to be modified to include hooks to look for scripts. In the case of inverse kinematics, a hook would need to look for a function and pass it forward kinematics information and expect to get a list of joint angles in return.
