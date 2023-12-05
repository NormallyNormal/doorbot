import re

import command.abstract_command as abstract_command
import command.argument_types as argument_types
from db.db_manager import DbManager


class PasswordCommand(abstract_command.AbstractCommand):
    name = "password"
    desc = "Sets a password for your door account if you do not already have one, or changes it if you are logged in."
    args = [("password", argument_types.StringArgumentType, "The new password for your door account.")]

    def run(self):
        db = DbManager()
        try:
            # throws error if account does not exist
            if not db.checkLoggedIn(db.getUserByUUID(self.issuer_id)):
                raise SyntaxError("Must be logged in to change password")
            # logged in - so changing password
            db.editUser(self.issuer_id, str(self.parsed_args["password"]))
            db.getConnection().commit()
            return "Password changed"
        except ValueError as e:
            # user does not exist - so making user
            try:
                db.addUser(self.issuer_id, str(self.parsed_args["password"]))
                db.getConnection().commit()
                return "Account created"
            except (ValueError, LookupError) as e:
                raise SyntaxError(str(e))
        finally:
            db.closeConnection()