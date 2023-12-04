import re

import command.argument_types as argument_types
import command.abstract_command as abstract_command
import doorserver.door_server as door_server
import db.db_manager as db_manager

class OpenCommand(abstract_command.AbstractCommand):
    name = "open"
    desc = "Opens a specified door. If no door is specified, the users set default door will be opened. The user must have permission to open the door at the time the command is received."
    args = [("door", argument_types.StringArgumentType, "The name of the door to open.")]

    def __init__(self, string, discordID, executable=True):
        spit_arguments = abstract_command.split_string_except_quotes(string)
        del spit_arguments[0]
        self.parsed_args = dict()
        self.issuer_id = discordID
        if len(spit_arguments) > 0 and executable:
            for i in range(0, len(spit_arguments)):
                spit_arguments[i] = spit_arguments[i].replace('"', '')
            for i in range(0, len(type(self).args)):
                try:
                    self.parsed_args[type(self).args[i][0]] = type(self).args[i][1](spit_arguments[i])
                except Exception as e:
                    print(e)
                    raise SyntaxError("Argument " + type(self).args[i][0] + " is not valid.")

    def run(self):
        db_manger_instance = db_manager.DbManager()
        try:
            db_manger_instance.doorOpened(str(self.parsed_args["door"]), self.issuer_id, "none", "manual")
        except PermissionError:
            db_manager.closeConnection()
            raise SyntaxError("That door does not exist, or you do not have permission to use it.")
        response = "Opened a door: "
        response += str(self.parsed_args["door"])
        door_server.open(str(self.parsed_args["door"]))
        db_manager.closeConnection()
        return response
