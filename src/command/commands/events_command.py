import re

import command.abstract_command as abstract_command
import command.argument_types as argument_types
from db.db_manager import DbManager


class EventsCommand(abstract_command.AbstractCommand):
    name = "events"
    desc = "Lists events for the specified door. Residents and admins of the door will see all events. Others will only see events they are invited to."
    args = [("door", argument_types.StringArgumentType, "The name of the door to view events for.")]

    def run(self):
        db_manger_instance = DbManager()
        if not db_manger_instance.checkLoggedIn(db_manger_instance.getUserByUUID(self.issuer_id)):
            db_manger_instance.closeConnection()
            raise SyntaxError("You are not logged in.")
        events_for_door = db_manger_instance.getEvents(str(self.parsed_args["door"]))
        response = "Events for "
        response += str(self.parsed_args["door"]) + ":\n\n"
        if (events_for_door):
            for event_for_door in events_for_door:
                response += f"- {event_for_door[2]} from {str(event_for_door[0])} to {str(event_for_door[1])}\n"
        else:
            response += "This door has no events"
        db_manger_instance.closeConnection()
        return response
