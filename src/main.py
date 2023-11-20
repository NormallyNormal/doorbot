import os
import sys

script_dir = os.path.dirname( __file__ )
sys.path.append( script_dir )

import command.command_registry as command_registry

string = input("Enter command: ")
print(command_registry.execute(string))
