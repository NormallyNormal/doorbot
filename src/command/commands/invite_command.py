import re

import command.abstract_command as abstract_command
import command.argument_types as argument_types
from db.db_manager import DbManager


class InviteCommand(abstract_command.AbstractCommand):
    name = "invite"
    desc = "Invites a user to an event. The user running this command must be a resident of the door the event is associated with."
    args = [("user", argument_types.StringArgumentType, "Discord username of the user to invite to the event."),
            ("event name", argument_types.StringArgumentType, "Name of the event to invite the user to.")]

    def run(self):
        db_manger_instance = DbManager()
        if not db_manger_instance.checkLoggedIn(db_manger_instance.getUserByUUID(self.issuer_id)):
            db_manger_instance.closeConnection()
            raise SyntaxError("You are not logged in.")
        try:
            permission_level = db_manger_instance.permissionLevelForEvent(self.issuer_id, str(self.parsed_args["event name"]))
            if permission_level == 'admin' or permission_level == 'resident':
                try:
                    db_manger_instance.addUserToEvent(str(self.parsed_args["user"]), str(self.parsed_args["event name"])) 
                    db_manger_instance.getConnection().commit()
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
            raise SyntaxError("That event does not exist, or you do not have permission")
        finally:
            db_manger_instance.closeConnection()
        return response