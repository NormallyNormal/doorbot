import command.abstract_command as abstract_command

cmd_registry = [abstract_command.AbstractCommand]

def execute(string):
    spit_arguments = string.split()
    for command in cmd_registry:
        if command.name == spit_arguments[0]:
            executeable_command = command(string, 0)
            return executeable_command.run()
    raise SyntaxError("Command " + spit_arguments[0] + " does not exist.")
    
