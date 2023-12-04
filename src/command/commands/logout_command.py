import re

import command.abstract_command as abstract_command
import command.argument_types as argument_types
from db.db_manager import DbManager


class LogoutCommand(abstract_command.AbstractCommand):
    name = "logout"
    desc = "Logs in to your door account with a password, allowing you to use door features."
    args = []

    def __init__(self, string, discordID, executable=True):
        self.parsed_args = ''
        self.issuer_id = discordID

    def run(self):
        db = DbManager()
        try:
          db.logout(self.issuer_id)
          db.getConnection().commit()
          return "You are now logged out"
        except ValueError as e:
            raise SyntaxError(str(e))
        finally:
            db.closeConnection()
