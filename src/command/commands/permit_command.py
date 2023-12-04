import re

import command.argument_types as argument_types
import command.abstract_command as abstract_command

class PermitCommand(abstract_command.AbstractCommand):
    name = "permit"
    desc = "Gives a user some level of permission for a door. A user must be resident for the given door to run this command. Residents cannot create residents or admins, but admins can."
    args = [("user", argument_types.StringArgumentType, "Discord name of the user to update the permissions of."), ("role", argument_types.StringArgumentType, "None, Guest, Resident, Admin."), ("door", argument_types.StringArgumentType, "The name of the door to add the user to.")]

    def run(self):
        db_manger_instance = db_manager.DbManager()
        if not db_manger_instance.checkLoggedIn(self.issuer_id):
            raise SyntaxError("You are not logged in.")
        try:
            db_manger_instance.userPermissionUpdate(str(self.parsed_args["user"]), str(self.parsed_args["door"]), str(self.parsed_args["role"])
        except:
            raise SyntaxError("Could not grant permission.")
        response = "Permission  "
        response += str(self.parsed_args["role"]) + " given to @<"
        response += str(self.parsed_args["user"]) + "> for "
        response += str(self.parsed_args["door"])
        return response
