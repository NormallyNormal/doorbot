import re

import command.argument_types as argument_types
import command.abstract_command as abstract_command
import command.command_registry as command_registry

class HelpCommand(abstract_command.AbstractCommand):
    name = "help"
    desc = "Shows help text for commands."
    args = [("command", argument_types.StringArgumentType, "The command to see help text on.")]

    def __init__(self, string, discordID, executable=True):
        spit_arguments = abstract_command.split_string_except_quotes(string)
        del spit_arguments[0]
        self.parsed_args = dict()
        self.issuer_id = discordID
        if len(spit_arguments) > 0 and executable:
            for i in range(0, len(spit_arguments)):
                spit_arguments[i] = spit_arguments[i].replace('"', '')
            for i in range(0, len(type(self).args)):
                try:
                    self.parsed_args[type(self).args[i][0]] = type(self).args[i][1](spit_arguments[i])
                except Exception as e:
                    print(e)
                    raise SyntaxError("Argument " + type(self).args[i][0] + " is not valid.")
    
    def run(self):
        try:
            return command_registry.get_help(command_name=str(self.parsed_args["command"]))
        except:
            return command_registry.get_help()
