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
  'skew' : { 'reference' : 'skew', 
             'description' : 'enters skew mode, where the view of the robot and simulation speed can be rapidly adjusted.'
            },
  'floor' : { 'reference' : 'floor <on/off>', 
             'description' : 'turns the floor on and off.'
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
  'trace' : { 'reference' : 'trace <on/off/clear/limit> <number>', 
             'description' : 'turn robot traces on/off, or clear the current set of traces. if limit is present, provide a number to set the maximum number of traces.'
            },
  'ghost' : { 'reference' : 'ghost <on/off/interval> <number>', 
             'description' : 'turn robot ghosts on/off. if interval is present, provide a number to set the ghost interval.'
            },
  'eval' : { 'reference' : 'eval <expression>', 
             'description' : 'return some variable from the simulator. e.g. \'eval robot.P01\'.'
            },
  'screendump' : { 'reference' : 'screendump', 
             'description' : 'take a picture of the current screen.'
            },
  'hide' : { 'reference' : 'hide', 
             'description' : 'hides this terminal.'
            },
  'status' : { 'reference' : 'status', 
             'description' : 'tells you what the simulator is currently doing.'
            },
  'exit' : { 'reference' : 'exit or quit', 
             'description' : 'closes the simulator.'
            },
  'setsym' : { 'reference' : 'setsym <var> <expression>', 
             'description' : 'sets a symbolic variable in the robot. e.g. \'setsym q3 cos(t)\.'
            },
  'maxtrace' : { 'reference' : 'maxtrace <number>', 
             'description' : 'limits the max number of traces for the tip of the robot.'
            }
}