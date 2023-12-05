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
        if not db_manger_instance.checkLoggedIn(db_manger_instance.getUserByUUID(self.issuer_id)):
            db_manger_instance.closeConnection()
            raise SyntaxError("You are not logged in.")
        events = db_manger_instance.getMyEvents(self.issuer_id)
        response = "Events you are invited to: \n\n"
        if (events):
            for event in events:
                response += f"- {event[0]} at door: {event[1]}\n"
        db_manger_instance.closeConnection()
        return response