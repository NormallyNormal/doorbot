import re

import command.abstract_command as abstract_command
import command.argument_types as argument_types
import db.db_manager as dbManager


class ScheduleCommand(abstract_command.AbstractCommand):
    name = "schedule"
    desc = "Creates a new scheduled event for a door. Events allow any user invited to that event to open the associated door, even if they would otherwise not have permission to."
    args = [("event name", argument_types.StringArgumentType, "Unique name of the new event."),
            ("time start", argument_types.DateTimeArgumentType, "Start time of the event, users invited will be able to enter after this time. Formatted as DD/MM/YY HH:MM AM/PM"),
            ("time end", argument_types.DateTimeArgumentType, "End time of the event, users invited will be no longer be able to enter after this time. Formatted as DD/MM/YY HH:MM AM/PM"),
            ("door", argument_types.StringArgumentType, "Door that the event is scheduled for. The user running the command must have the resident or admin role for this door.")]
    

    def run(self):
        timeStart = self.parsed_args["time start"].sql()
        timeEnd = self.parsed_args["time end"].sql()
        name = str(self.parsed_args["event name"])
        doorName = str(self.parsed_args["door"])

        manager = dbManager.DbManager()

        if not manager.checkLoggedIn(manager.getUserByUUID(self.issuer_id)):
            manager.closeConnection()
            raise SyntaxError("You are not logged in.")
        try:
            permission_level = manager.permissionLevelForDoor(self.issuer_id, self.parsed_args["door"])
            if permission_level == 'admin' or permission_level == 'resident':
                manager.addEvent(timeStart, timeEnd, name, doorName)
                manager.getConnection().commit()
            else:
                raise SyntaxError('That event does not exist, or you do not have permission')
        except ValueError as e:
            raise SyntaxError(str(e))
        finally:
            manager.closeConnection()