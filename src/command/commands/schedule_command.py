import re
import db.db_manager as dbManager
import command.argument_types as argument_types
import command.abstract_command as abstract_command

class ScheduleCommand(abstract_command.AbstractCommand):
    name = "schedule"
    desc = "Creates a new scheduled event for a door. Events allow any user invited to that event to open the associated door, even if they would otherwise not have permission to."
    args = [("event name", argument_types.StringArgumentType, "Unique name of the new event."),
            ("time start", argument_types.DateTimeArgumentType, "Start time of the event, users invited will be able to enter after this time. Formatted as DD/MM/YY HH:MM AM/PM"),
            ("time end", argument_types.DateTimeArgumentType, "End time of the event, users invited will be no longer be able to enter after this time. Formatted as DD/MM/YY HH:MM AM/PM"),
            ("door", argument_types.StringArgumentType, "Door that the event is scheduled for. The user running the command must have the resident or admin role for this door.")]
    

    def run(self):
        #database access
        manager = dbManager.DbManager()
        timeStart = self.parsed_args["time start"]
        timeEnd = self.parsed_args["time end"]
        name = self.parsed_args["event name"]
        doorName = self.parsed_args["door"]

        manager.addEvent(timeStart, timeEnd, name, doorName)
        response = "command ran with name : "
        response += str(self.parsed_args["event name"])
        return response
