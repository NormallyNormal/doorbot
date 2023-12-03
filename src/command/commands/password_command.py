import re

import command.argument_types as argument_types
import command.abstract_command as abstract_command

class PasswordCommand(abstract_command.AbstractCommand):
    name = "password"
    desc = "Sets a password for your door account if you do not already have one, or changes it if you are logged in."
    args = [("password", argument_types.StringArgumentType, "The new password for your door account.")]

    def run(self):
        #database access
        response = "command ran"
        return response
