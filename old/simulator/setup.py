from distutils.core import setup
import py2exe

setup(windows=['simulator.py'],
    options = {
        "py2exe" : {
            "compressed" : 0,
            "optimize" : 2,
            "includes" : ["ctypes", "logging"],
            "excludes" : ["OpenGL"],
            }
        }
    )
