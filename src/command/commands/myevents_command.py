import re

import command.abstract_command as abstract_command
import command.argument_types as argument_types
import db.db_manager as db_manager


class MyeventsCommand(abstract_command.AbstractCommand):
    name = "myevents"
    desc = "Lists events you are invited to."
    args = []

    def run(self):
        db_manger_instance = db_manager.DbManager()
        if not db_manger_instance.checkLoggedIn(self.issuer_id):
            raise SyntaxError("You are not logged in.")
        response = "Events you are invited to: "
        response += str(db_manger_instance.getMyEvents(self.issuer_id))
        return response
