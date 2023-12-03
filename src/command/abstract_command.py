import re

import command.argument_types as argument_types

class AbstractCommand:
    name = "command"
    desc = "A basic command."
    args = [("argument1", argument_types.IntegerArgumentType, "Takes an integer."), ("argument2", argument_types.TimeArgumentType, "Takes a time.")]

    def __init__(self, string, discordID, executable=True):
        spit_arguments = split_string_except_quotes(string)
        del spit_arguments[0]
        self.parsed_args = dict()
        self.issuer_id = discordID
        if executable:
            for i in range(0, len(spit_arguments)):
                spit_arguments[i] = spit_arguments[i].replace('"', '')
            for i in range(0, len(type(self).args)):
                try:
                    self.parsed_args[type(self).args[i][0]] = type(self).args[i][1](spit_arguments[i])
                except Exception as e:
                    print(e)
                    raise SyntaxError("Argument " + type(self).args[i][0] + " is not valid.")

    def run(self):
        #database access
        response = "command ran with integer: "
        response += str(self.parsed_args["argument1"]) + " time: " + str(self.parsed_args["argument2"])
        return response

    def help(self):
        help_response = "`" + self.name
        for item in type(self).args:
            help_response += " <" + item[0] + ">"
        help_response += "` " + self.desc + "\n"
        for item in type(self).args:
            help_response += "*" + item[0] + "*: " + item[2] + "\n"
        return help_response

def split_string_except_quotes(input_string):
    # Regex pattern to match quoted sections or non-whitespace characters
    pattern = r'(?:"[^"]*"|\S)+'

    # Find all occurrences of the pattern in the input string
    tokens = re.findall(pattern, input_string)

    return tokens
