# Team Chupacabra - Databases Final Project
### Team Members: Caleb Rollins, Finn Bacheldor, Alex Hill, Matthew Welker, Jakari Robinson
Code for CSC 440 (Database Management Systems) Fall 2023 Final Project
<br>
<br>
# Running the Program

### main.py
Rather than inviting and using the discord bot in a server, you can use `src/main.py` to run commands and interact with the database. To run it, run `python src/main.py <discord_id>`, where `<discord_id>` is some positive integer that simulates a discord user (it does not need to be a real discord ID). On mac the command will use `python3`. 
<br>
<br>
The program will continually prompt for commands and each command will be run as if it was a discord message input from the discord ID specified on the command line. To quit, press Control + C. You can either continually quit and rerun the program with different users or have multiple terminals / terminal instances open with different users.
<br>
<br>
Any arguments given that require spaces (such as dates or names with spaces) need to be surrounded in quotation marks

### Creating an Account

To create an account, use the command `password <password>`, and then login using `login <password>`. The account is tied to the discord user (or "discord ID" if using main.py)

### Permission Levels
Permission levels for a door are resident, admin, guest, and none. For the time being resdient and admin have the same permissions, and guest has limited permissions such as not being able to create events (but they can open the door)

### Command List and Help Command
The commands available are listed below with a brief description of what they do. For a more in depth description of the commands, including their arguments, use `help <command>` while running the bot or main.py. For all commands other than help, password, and login the user must be logged in

- default: Set a default door so the open command can be used without a door argument
- events: list events for a door
- invite: invite a user to an event
- list: list doors available for the user to open
- login: log in to the system
- logout: log out of the system
- myevents: list events you are invited to
- open: open a door
- password: change password or create account
- permit: give user permissions on a door
- schedule: create an event
- uninvite: uninvite a user from an event
<br>
<br>
<br>
<br>
[![doorbot continuous integration](https://github.ncsu.edu/ccrollin/csc440-teamproj/actions/workflows/doorbot-ci.yml/badge.svg)](https://github.ncsu.edu/ccrollin/csc440-teamproj/actions/workflows/doorbot-ci.yml)
