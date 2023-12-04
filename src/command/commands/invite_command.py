import re

import command.argument_types as argument_types
import command.abstract_command as abstract_command

class InviteCommand(abstract_command.AbstractCommand):
    name = "invite"
    desc = "Invites a user to an event. The user running this command must be a resident of the door the event is associated with."
    args = [("user", argument_types.StringArgumentType, "Discord username of the user to invite to the event."),
            ("event name", argument_types.StringArgumentType, "Name of the event to invite the user to.")]

    def run(self):
        db_manger_instance = db_manager.DbManager()
        if not db_manger_instance.checkLoggedIn(self.issuer_id):
            raise SyntaxError("You are not logged in.")
        try:
            permission_level = db_manger_instance.permissionLevelForEvent(self.issuer_id, self.parsed_args["event name"])
            if permission_level == 'admin' or permission_level == 'resident':
                try:
                    db_manger_instance.addUserToEvent(str(self.parsed_args["user"]), str(self.parsed_args["event name"])) 
                    response = "Added @<"
                    response += str(self.parsed_args["user"]) + "> to event "
                    response += str(self.parsed_args["event name"]) + "."
                except:
                    response = "Failed to add @<"
                    response += str(self.parsed_args["user"]) + "> to event "
                    response += str(self.parsed_args["event name"]) + "."
            else:
                raise SyntaxError("That event does not exist, or you do not have permission")
        except:
            db_manager.closeConnection()
            raise SyntaxError("That event does not exist, or you do not have permission")
        return response

