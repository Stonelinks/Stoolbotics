d = {
  'help' : { 'reference' : 'help <cmd (optional)>', 
             'description' : 'If <cmd> is provided, display help for that command. Otherwise  it just list all commands.'
            },
  'play' : { 'reference' : 'play <file (optional)>', 
             'description' : 'If <file> is present, the simulator plays that file. Otherwise, it just starts the simulator.'
            },
  'stop' : { 'reference' : 'stop', 
             'description' : 'Halts the simulaton.'
            },
  'skew' : { 'reference' : 'skew', 
             'description' : 'Enters skew mode, where the view of the robot and simulation speed can be rapidly adjusted.'
            },
  'floor' : { 'reference' : 'floor <on/off>', 
             'description' : 'Turns the floor on and off. Providing no arguments toggles the floor.'
            },
  'record' : { 'reference' : 'record <file>', 
             'description' : 'Outputs current arm movements to a file which can be exported or played back later.'
            },
  'load' : { 'reference' : 'load <robot file>', 
             'description' : 'Loads a robot file into the simulator. Use the \'list\' command to see what robots are able to be loaded.'
            },
  'list' : { 'reference' : 'list', 
             'description' : 'Lists all the robots that can be loaded into the simulator. To add something to this list, just place a valid robot.json file in the \'robots\' folder.'
            },
  'axis' : { 'reference' : 'axis <on/off>', 
             'description' : 'Turn robot axis on/off. Providing no arguments toggles the axis.'
            },
  'trace' : { 'reference' : 'trace <on/off/clear/limit> <number>', 
             'description' : 'Turn robot traces on/off, or clear the current set of traces. If the <limit> argument is used, provide a number to set the maximum number of traces.'
            },
  'ghost' : { 'reference' : 'ghost <on/off/interval> <number>', 
             'description' : 'turn robot ghosts on/off. If <interval> is present, provide a number to set the ghost interval. Providing no arguments toggles the ghosts.'
            },
  'eval' : { 'reference' : 'eval <expression>', 
             'description' : 'Return some variable from the simulator. e.g. \'eval robot.P01\'. Output might look a little weird.'
            },
  'screendump' : { 'reference' : 'screendump', 
             'description' : 'Take a picture of the current screen and save it to disk.'
            },
  'hide' : { 'reference' : 'hide', 
             'description' : 'Hides this terminal.'
            },
  'status' : { 'reference' : 'status', 
             'description' : 'Tells you what the simulator is currently doing.'
            },
  'exit' : { 'reference' : 'exit or quit', 
             'description' : 'Closes the simulator.'
            },
  'set' : { 'reference' : 'set <var> <expression>', 
             'description' : 'Sets a symbolic variable in the simulator. e.g. \'set q3 cos(t)\', \'set t 0\', \'set tscale -.1\', \'set P23 [0, 0, l2 + q2]\'.'
            },
  'server' : { 'reference' : 'server <start/stop> <port>', 
             'description' : 'Starts or stops the simulator listening on the specified port for incoming commands from other programs.'
            },
}
