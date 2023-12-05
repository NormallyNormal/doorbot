import os
import sys

script_dir = os.path.dirname( __file__ )
sys.path.append( script_dir )

import command.command_registry as command_registry

id = sys.argv[1]
while (True):
  string = input("Enter command: ")
  try:
    print(command_registry.execute(string, id))
  except SyntaxError as e:
    print(f"There was a syntax error with message: {str(e)}")
