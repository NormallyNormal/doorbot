import re

import command.argument_types as argument_types
import command.abstract_command as abstract_command

class LogoutCommand(abstract_command.AbstractCommand):
    name = "logout"
    desc = "Logs in to your door account with a password, allowing you to use door features."
    args = []

    def run(self):
        #database access
        response = "command ran"
        return response
