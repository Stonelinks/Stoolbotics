- Proposal (Luke)

- Git repository and github setup (Luke)

- Robot object
    - config file format (Luke)
    - config file to robot object parser (Luke)
    - symbolic expression solver (Luke)
        - architecture (Luke)
        - implementation (Luke)
    - basic utility functions:
        - hat (Luke)
        - rot (euler-rodriguez) (Luke)
    - rendering of robot arm
        - base implementation (Scott)
        - axis, trace and ghost features (Luke)
    - link class (Luke)
    - general forward kinematics solver (Luke)
    - manual override (for controlling from matlab, etc) (Luke)

- Simulator
    - initialization of robot object in simulator (Luke)
    - timestepping scheme (Luke)
    - rendering of room (Scott)
    - rotation of camera (Scott)
    - OpenGL callback scheme (Scott)
    - skew mode (Luke)
    - all commands (set, eval, stop, play, etc) (Luke)
    
- Command line interface
    - core functionality
        - input vs output distinction (Luke)
        - multiline output formatting (Luke)
        - arrow keys to cycle through input (Luke)
    - function registry (Luke)
    - help (Luke)
    - simulator commands
        - architecture (Luke)
        - implementation (Luke)

- Matlab control via socket server (Luke)

- Movie making
    - file format (Luke)
    - playback (Luke)
    - recording (Luke)

- Windows support
    - py2exe (Scott)
    - Makefile (Luke)

- Documentation
    - docs folder setup (Luke)
    - intro (Luke)
    - quickstart (Luke)
    - usage of simulator (Luke)
    - implementation (with the exception of "drawing the robot") (Luke)
    - closing (Luke)
    - proofreading (Scott)
