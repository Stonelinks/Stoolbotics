TODO (not necessarily in order):

- specification of a robot arm VIA matricies, somehow
  - robots matricies in json?

- drawing of that arm in world
  - joints:
    - rotary = cylinder
    - prismatic = rectangular prisim
  - links between joints = lines for now
  - frames:
    - coordinate axis
    - somehow need to anchor a frame to a link or joint
  - world:
    - floor
    - lighting?

- port wen's matlab stuff to python
  - basic things:
    - hat
    - rot (euler-rodriguez)
    - trans
  - subproblems for inverse kinematics
  - jacobian (?)

- forward kinematics solver
  - give it any robot and joint angles, find end position in world

- write proposal

- research feasability of making a movie from pyopengl
  - initial research shows this will be difficult:
    - direct rendering: save screenshots to disk, use something like ffmpeg
    - deferred: keep screenshots in RAM, dump to disk, use ffmpeg or something
  - if not possible, come up with a good way of saving & replaying things within software
  
