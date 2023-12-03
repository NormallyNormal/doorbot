import re

import command.argument_types as argument_types
import command.abstract_command as abstract_command

class DefaultCommand(abstract_command.AbstractCommand):
    name = "default"
    desc = "Sets the default door for a user. Allows the `open`  command to be used without an argument. Also allows the quick access button to be used."
    args = [("door", argument_types.StringArgumentType, "The name of the door to set as default.")]

    def run(self):
        #database access
        response = "command ran with door: "
        response += str(self.parsed_args["door"])
        return response
