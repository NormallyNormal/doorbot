import random
import re
import string
from datetime import datetime

import command.abstract_command as abstract_command
import command.argument_types as argument_types
import db.db_manager as db_manager
import doorserver.door_server as door_server


class OpenCommand(abstract_command.AbstractCommand):
    name = "open"
    desc = "Opens a specified door. If no door is specified, the users set default door will be opened. The user must have permission to open the door at the time the command is received."
    args = [("door", argument_types.StringArgumentType, "The name of the door to open.")]

    def run(self):
        db_manger_instance = db_manager.DbManager()
        if not db_manger_instance.checkLoggedIn(db_manger_instance.getUserByUUID(self.issuer_id)):
            db_manger_instance.closeConnection()
            raise SyntaxError("You are not logged in.")
        try:
            if (self.parsed_args["door"] == None):
                self.parsed_args["door"] = db_manger_instance.getDefault(self.issuer_id)
            # generate random image file name
            now = datetime.now()
            random_str = ''.join(random.choice(string.ascii_lowercase) for i in range(8))
            filename = f"tempfile-{now.strftime('%d-%m-%Y-%H:%M:%S')}-{random_str}.png"
            db_manger_instance.doorOpened(str(self.parsed_args["door"]), self.issuer_id, filename, "manual")
            db_manger_instance.getConnection().commit()
            response = "Opened a door: "
            response += str(self.parsed_args["door"])
            door_server.open_door(str(self.parsed_args["door"]))
        except (PermissionError, ValueError) as e:
            db_manger_instance.closeConnection()
            raise SyntaxError(str(e))
        finally:       
            db_manger_instance.closeConnection()
        return response
