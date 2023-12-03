import re

import command.argument_types as argument_types
import command.abstract_command as abstract_command

class UninviteCommand(abstract_command.AbstractCommand):
    name = "uninvite"
    desc = "Uninvites a user to an event. The user running this command must be a resident or admin of the door the event is associated with."
    args = [("user", argument_types.StringArgumentType, "Discord username of the user to remove from the event."),
            ("event name", argument_types.StringArgumentType, "Name of the event to remove the user from.")]

    def run(self):
        #database access
        response = "command ran with user: "
        response += str(self.parsed_args["user"])
        return response
