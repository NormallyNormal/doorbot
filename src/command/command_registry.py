from command.commands import default_command, events_command, help_command, invite_command, list_command, login_command, logout_command, myevents_command, open_command, password_command, permit_command, schedule_command, uninvite_command

cmd_registry = [default_command.DefaultCommand,
                events_command.EventsCommand,
                invite_command.InviteCommand,
                help_command.HelpCommand,
                list_command.ListCommand,
                login_command.LoginCommand,
                logout_command.LogoutCommand,
                myevents_command.MyeventsCommand,
                open_command.OpenCommand,
                password_command.PasswordCommand,
                permit_command.PermitCommand,
                schedule_command.ScheduleCommand,
                uninvite_command.UninviteCommand]

def execute(string, issuer_id):
    spit_arguments = string.split()
    for command in cmd_registry:
        if command.name == spit_arguments[0]:
            executeable_command = command(string, issuer_id)
            return executeable_command.run()
    raise SyntaxError("Command " + spit_arguments[0] + " does not exist.")

def get_help(command_name=None):
    if command_name == None:
        allhelp = ""
        for command in cmd_registry:
            unexecuteable_command = command("null", -1, executable=False)
            allhelp += unexecuteable_command.help() + '\n'
        return allhelp
    for command in cmd_registry:
        if command.name == command_name:
            unexecuteable_command = command("null", -1, executable=False)
            return unexecuteable_command.help()
    raise SyntaxError("Command " + command_name + " does not exist.")
