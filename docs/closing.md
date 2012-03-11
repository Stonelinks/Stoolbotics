#Closing Remarks

##Future Improvements

There are many future improvements that could be made to Stoolbotics. Two major ones come to mind:

A support for a user scripting environment would have been nice. This could allow students to write scripts that do things like inverse kinematics, workspace calculations, finding DH parameters, etc. The simulator would have to be modified to include hooks to look for scripts. In the case of inverse kinematics, a hook would need to look for a function and pass it forward kinematics information and expect to get a list of joint angles in return.

In conjunction with the above, integration with a physics engine would be nice for writing users to measure torques, writing their own PID loops, simulating forces applied, etc.

##Thank You

Thank you for reading this documentation! Please feel free to send any comments or questions to lucas.p.doyle@gmail.com.
