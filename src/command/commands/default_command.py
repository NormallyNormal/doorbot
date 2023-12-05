import re

import command.argument_types as argument_types
import command.abstract_command as abstract_command
import db.db_manager as dbManager

class DefaultCommand(abstract_command.AbstractCommand):
    name = "default"
    desc = "Sets the default door for a user. Allows the `open`  command to be used without an argument. Also allows the quick access button to be used."
    args = [("door", argument_types.StringArgumentType, "The name of the door to set as default.")]

    def run(self):
        manager = dbManager.DbManager()
        if not manager.checkLoggedIn(manager.getUserByUUID(self.issuer_id)):
            manager.closeConnection()
            raise SyntaxError("You are not logged in.")
        try:
            permission_level = manager.permissionLevelForDoor(self.issuer_id, self.parsed_args["door"])
            if permission_level == 'admin' or permission_level == 'resident':
                manager.setDefault(self.issuer_id, self.parsed_args["door"])
                manager.getConnection().commit()
            else:
                raise SyntaxError('That door does not exist, or you do not have permission')
        except ValueError as e:
            raise SyntaxError(str(e))
        finally:
            manager.closeConnection()

        response = "command ran with door: "
        response += str(self.parsed_args["door"])
        return response
