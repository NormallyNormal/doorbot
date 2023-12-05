import re

import command.argument_types as argument_types
import command.abstract_command as abstract_command
from db.db_manager import DbManager

class UninviteCommand(abstract_command.AbstractCommand):
    name = "uninvite"
    desc = "Uninvites a user to an event. The user running this command must be a resident or admin of the door the event is associated with."
    args = [("user", argument_types.StringArgumentType, "Discord username of the user to remove from the event."),
            ("event name", argument_types.StringArgumentType, "Name of the event to remove the user from.")]

    def run(self):
        db_manger_instance = DbManager()
        if not db_manger_instance.checkLoggedIn(self.issuer_id):
            raise SyntaxError("You are not logged in.")
        try:
            permission_level = db_manger_instance.permissionLevelForEvent(self.issuer_id, self.parsed_args["event name"])
            if permission_level == 'admin' or permission_level == 'resident':
                try:
                    db_manger_instance.removeUserFromEvent(str(self.parsed_args["user"]), str(self.parsed_args["event name"])) 
                    response = "Removed @<"
                    response += str(self.parsed_args["user"]) + "> from event "
                    response += str(self.parsed_args["event name"]) + "."
                except:
                    response = "Failed to remove @<"
                    response += str(self.parsed_args["user"]) + "> from event "
                    response += str(self.parsed_args["event name"]) + "."
            else:
                raise SyntaxError("That event does not exist, or you do not have permission")
        except:
            db_manger_instance.closeConnection()
            raise SyntaxError("That event does not exist, or you do not have permission")
        return response
