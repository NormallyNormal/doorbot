import re

import command.argument_types as argument_types
import command.abstract_command as abstract_command

class MyeventsCommand(abstract_command.AbstractCommand):
    name = "myevents"
    desc = "Lists events you are invited to."
    args = []

    def run(self):
        #database access
        response = "command ran"
        return response
