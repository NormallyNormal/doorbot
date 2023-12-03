import re

import command.argument_types as argument_types
import command.abstract_command as abstract_command

class ListCommand(abstract_command.AbstractCommand):
    name = "list"
    desc = "Lists door names you have any level of access to, along with locations. Includes doors you may use temporarily because of events."
    args = []

    def run(self):
        #database access
        response = "command ran"
        return response
