import re

import command.abstract_command as abstract_command
import command.argument_types as argument_types
from db.db_manager import DbManager


class ListCommand(abstract_command.AbstractCommand):
    name = "list"
    desc = "Lists door names you have any level of access to, along with locations. Includes doors you may use temporarily because of events."
    args = []

    def run(self):
        db = DbManager()
        try:
            if db.checkLoggedIn(db.getUserByUUID(self.issuer_id)):
                doors = db.getDoors(self.issuer_id)
                response = "Your Doors: \n\n"
                if (doors):
                    for door in doors:
                        response += f"- {door[0]} -- {door[1]}\n"
                else:
                    response += "You do not have access to any doors"
                return response
            else:
                raise SyntaxError('You are not logged in')
        except ValueError as e:
            raise SyntaxError(str(e))
        finally:
            db.closeConnection()
