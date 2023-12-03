import re

import command.argument_types as argument_types
import command.abstract_command as abstract_command

class EventsCommand(abstract_command.AbstractCommand):
    name = "events"
    desc = "Lists events for the specified door. Residents and admins of the door will see all events. Others will only see events they are invited to."
    args = [("door", argument_types.StringArgumentType, "The name of the door to view events for.")]

    def run(self):
        #database access
        response = "command ran with door: "
        response += str(self.parsed_args["door"])
        return response
