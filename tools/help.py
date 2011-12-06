d = {
  'help' : { 'reference' : 'help <cmd (optional)>', 
             'description' : 'if <cmd> is provided, display help for that command. otherwise just list all commands.'
            },
  'play' : { 'reference' : 'play <file (optional)>', 
             'description' : 'if <file> is present, the simulator plays that file. otherwise, just starts the simulator.'
            },
  'stop' : { 'reference' : 'stop', 
             'description' : 'halts the simulaton.'
            },
  'rewind' : { 'reference' : 'rewind', 
             'description' : 'if playing a file, resets to the beginning'
            },
  'skew' : { 'reference' : 'skew', 
             'description' : 'enters skew mode, where the view of the robot and simulation speed can be rapidly adjusted.'
            },
  'record' : { 'reference' : 'record <file>', 
             'description' : 'outputs current arm movements to a file which can be played back later.'
            },
  'load' : { 'reference' : 'load <robot file>', 
             'description' : 'loads a robot file into the simulator.'
            },
  'list' : { 'reference' : 'list', 
             'description' : 'lists robots that can be loaded into the simulator.'
            },
  'axis' : { 'reference' : 'axis <on/off>', 
             'description' : 'turn robot axis on/off.'
            },
  'trace' : { 'reference' : 'trace <on/off>', 
             'description' : 'turn robot traces on/off.'
            },
  'ghost' : { 'reference' : 'ghost <on/off>', 
             'description' : 'turn robot ghost on/off.'
            },
  'screendump' : { 'reference' : 'screendump', 
             'description' : 'take a picture of the current screen.'
            },
  'hide' : { 'reference' : 'hide', 
             'description' : 'hides this terminal.'
            },
  'dump' : { 'reference' : 'dump <param (optional)>', 
             'description' : 'dumps the robot\'s numerical data. if param is provided, will dump only that.'
            },
  'exit' : { 'reference' : 'exit or quit', 
             'description' : 'closes the simulator.'
            }
}
