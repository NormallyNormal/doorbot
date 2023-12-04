import re

import command.abstract_command as abstract_command
import command.argument_types as argument_types
from db.db_manager import DbManager


class LoginCommand(abstract_command.AbstractCommand):
    name = "login"
    desc = "Logs in to your door account with a password, allowing you to use door features."
    args = [("password", argument_types.StringArgumentType, "The password for your door account.")]

    def __init__(self, string, discordID, executable=True):
        split_arguments = abstract_command.split_string_except_quotes(string)
        del split_arguments[0]
        self.parsed_args = dict()
        self.issuer_id = discordID
        if len(split_arguments) > 0 and executable:
            for i in range(0, len(split_arguments)):
                split_arguments[i] = split_arguments[i].replace('"', '')
            for i in range(0, len(type(self).args)):
                try:
                    self.parsed_args[type(self).args[i][0]] = type(self).args[i][1](split_arguments[i])
                except Exception as e:
                    print(e)
                    raise SyntaxError("Argument " + type(self).args[i][0] + " is not valid.")

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

