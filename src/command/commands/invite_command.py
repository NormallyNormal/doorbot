import re

import command.argument_types as argument_types
import command.abstract_command as abstract_command

class InviteCommand(abstract_command.AbstractCommand):
    name = "invite"
    desc = "Invites a user to an event. The user running this command must be a resident of the door the event is associated with."
    args = [("user", argument_types.StringArgumentType, "Discord username of the user to invite to the event."),
            ("event name", argument_types.StringArgumentType, "Name of the event to invite the user to.")]

    def run(self):
        #database access
        response = "command ran with user: "
        response += str(self.parsed_args["user"])
        return response
