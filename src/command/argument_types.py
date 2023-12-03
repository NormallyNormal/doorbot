from datetime import datetime
import time

class AbstractArgumentType:
    def __init__(self, string):
        self.value = None

    def __str__(self):
        return "empty"

class IntegerArgumentType(AbstractArgumentType):
    def __init__(self, string):
        self.value = int(string)

    def __str__(self):
        return str(self.value)

class FloatArgumentType(AbstractArgumentType):
    def __init__(self, string):
        self.value = float(string)

    def __str__(self):
        return str(self.value)

class StringArgumentType(AbstractArgumentType):
    def __init__(self, string):
        self.value = str(string)

    def __str__(self):
        return self.value

class TimeArgumentType(AbstractArgumentType):
    def __init__(self, string):
        try:
            self.value = time.strptime(string, "%I:%M %p %Z%z")
        except:
            self.value = time.strptime(string + " UTC-0400", "%I:%M%p %Z%z")

    def __str__(self):
        return  time.strftime("%I:%M%p %Z", self.value)

class DateArgumentType(AbstractArgumentType):
    def __init__(self, string):
        self.value = datetime.strptime(string, "%d/%m/%y")

    def __str__(self):
        return datetime.strftime("%d/%m/%y", self.value)
    
class DateTimeArgumentType(AbstractArgumentType):
    def __init__(self, string):
        try:
            print(string)
            self.value = datetime.strptime(string, "%d/%m/%y %I:%M %p %Z%z")
        except:
            print(string)
            self.value = datetime.strptime(string + " UTC-0400", "%d/%m/%y %I:%M %p %Z%z")

    def __str__(self):
        return datetime.strftime("%d/%m/%y %I:%M%p %Z", self.value)

