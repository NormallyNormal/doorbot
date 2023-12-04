import re

import command.abstract_command as abstract_command
import command.argument_types as argument_types
from db.db_manager import DbManager


class LoginCommand(abstract_command.AbstractCommand):
    name = "login"
    desc = "Logs in to your door account with a password, allowing you to use door features."
    args = [("password", argument_types.StringArgumentType, "The password for your door account.")]

    def run(self):
        db = DbManager()
        try:
            db.login(self.issuer_id, str(self.parsed_args["password"]))
            db.getConnection().commit()
            return "You are now logged in"
        except ValueError as e:
            raise SyntaxError(str(e))
        finally:
            db.closeConnection()

