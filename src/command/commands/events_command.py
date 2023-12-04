import re

import command.argument_types as argument_types
import command.abstract_command as abstract_command

class EventsCommand(abstract_command.AbstractCommand):
    name = "events"
    desc = "Lists events for the specified door. Residents and admins of the door will see all events. Others will only see events they are invited to."
    args = [("door", argument_types.StringArgumentType, "The name of the door to view events for.")]

    def run(self):
        db_manger_instance = db_manager.DbManager()
        if not db_manger_instance.checkLoggedIn(self.issuer_id):
            raise SyntaxError("You are not logged in.")
        events_for_door = db_manger_instance.getEvents(str(self.parsed_args["door"])
        response = "Events for "
        response += str(self.parsed_args["door"]) + ":\n"
        for event_for_door in events_for_door:
            response += event_for_door[2] + " from " + str(event_for_door[0]) + str(event_for_door[1])
        return response
