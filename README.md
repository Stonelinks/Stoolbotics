TODO:

- (x) Specification of a robot arm VIA config file
    - (x) easy way to symbolically express arm parameters
    - (x) parameters should be first class variables for robot objects

- (x) Drawing of that arm in world
    - (x) joints (params = axis, type, angle/displacement):
        - (x) rotary = cylinder
        - (x) prismatic = rectangular prisim
    - (x) links between joints = lines for now
    - (x) frames:
        - (x) coordinate axis
        - (x) need to anchor a frame to a link or joint
    - (x) world:
        - (x) floor
        - (x) lighting
    - (x) skew mode - move robot around
    
- (x) Port some of Prof. Wen's matlab to python:
    - (x) basic things:
        - (x) hat
        - (x) rot (euler-rodriguez)
        - Note: cross and dot product covered by numpy
    - (x) homogeneous matrices
    - subproblems for inverse kinematics
    - jacobian (?)

- (x) General forward kinematics solver - given any robot and joint angles, find end position in world

- scripting environment
    - load and run user facing script
    - write examples (inverse kinematics, etc)

- (x) write proposal

- (x) terminal
    - (x) core functionality
    - (x) function registry
    - (x) write command help / document some
    - (x) simulator commands
        - (x) load robot
        - (x) axis on/off
        - (x) trace on/off
        - (x) ghost on/off
        - (x) screendump
    - (x) hide / show

- (x) matlab control via socket

- (x) movie making
    - (x) implement record - write to a file 
    - (x) implement play / pause / rewind

- (x) windows support / installer
