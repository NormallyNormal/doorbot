import re

import command.argument_types as argument_types
import command.abstract_command as abstract_command

class LoginCommand(abstract_command.AbstractCommand):
    name = "login"
    desc = "Logs in to your door account with a password, allowing you to use door features."
    args = [("password", argument_types.StringArgumentType, "The password for your door account.")]

    def run(self):
        #database access
        response = "command ran with password: "
        response += str(self.parsed_args["password"])
        return response
