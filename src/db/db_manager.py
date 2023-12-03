from dotenv import dotenv_values
import mysql.connector
import sys
import os
from datetime import datetime
import hashlib

class DbManager:
  def __init__(self):
    try:
      self.config = dotenv_values("db.env")
      self.connection = mysql.connector.connect(user=self.config["DB_USERNAME"], password=self.config["DB_PASSWORD"], host=self.config["DB_HOSTNAME"], port=self.config["DB_PORT"], database=self.config["DB_NAME"], ssl_disabled=False)
      self.cursor = self.connection.cursor()
    except mysql.connector.Error as err:
      self.connection.close()
      sys.exit()

  def getConnection(self):
    return self.connection
    
  def getCursor(self):
    return self.cursor

  def getDoorByName(self, name):
    get_door_query = ("SELECT id FROM door AS d WHERE d.displayName=%s")
    self.cursor.execute(get_door_query, (name,))
    doorResult = self.cursor.fetchone()
    if (doorResult != None):
      return doorResult[0]
    raise ValueError("Door Does Not Exist")

  def getUserByName(self, name):
    get_user_query = ("SELECT id FROM user AS u WHERE u.discordUUID=%s")
    self.cursor.execute(get_user_query, (name,))
    userResult = self.cursor.fetchone()
    if (userResult != None):
      return userResult[0]
    raise ValueError("User Does Not Exist")

  def getOpenTypeByName(self, name):
    get_opentype_query = ("SELECT id FROM opentype AS ot WHERE ot.name=%s")
    self.cursor.execute(get_opentype_query, (name,))
    openTypeResult = self.cursor.fetchone()
    if (openTypeResult != None):
      return openTypeResult[0]
    raise ValueError("Open Type Does Not Exist")

  def getUserInstance(self, doorId, userId):
    get_userinstance_query = ("SELECT id FROM userinstance AS ui WHERE ui.door_id_userinstance=%s AND ui.user_id_userinstance=%s")
    self.cursor.execute(get_userinstance_query, (doorId, userId))
    userInstanceResult = self.cursor.fetchone()
    if (userInstanceResult != None):
      return userInstanceResult[0]
    raise ValueError("User Instance Does Not Exist")

  def getEvents(self, doorName):
    doorId = self.getDoorByName(doorName)
    get_events_query = ("SELECT timeStart, timeEnd, name, door_id_scheduledEvent FROM scheduledEvent AS e WHERE e.door_id_scheduledEvent=%s")
    self.cursor.execute(get_events_query, (doorId,))
    results = self.cursor.fetchall()
    return results

  def addEvent(self, timeStart, timeEnd, name, doorName):
    doorId = self.getDoorByName(doorName)
    add_event_query = ("INSERT INTO scheduledEvent (timeStart, timeEnd, name, door_id_scheduledEvent) VALUES (%s, %s, %s, %s)")
    self.cursor.execute(add_event_query, (timeStart, timeEnd, name, doorId))

  def doorOpened(self, doorName, userName, entryPhotoFileName, openType):
    doorId = self.getDoorByName(doorName)
    userId = self.getUserByName(userName)
    openTypeId = self.getOpenTypeByName(openType)

    score = -1
    msg = ""
    self.cursor.callproc('open_door', (doorId, userId, score, msg))

    success = False
    self.cursor.callproc('create_open_log', (userId, doorId, entryPhotoFileName, openTypeId, success))
    
  def getDoors(self, userName):
    userId = self.getUserByName(userName)
    get_doors_query = ("SELECT door.displayName FROM userinstance JOIN door ON userinstance.door_id_userinstance=door.id WHERE userinstance.user_id_userinstance=%s")
    self.cursor.execute(get_doors_query, (userId,))
    results = self.cursor.fetchall()
    return results

  def checkPassword(self, userId, password):
    get_hashed_query = ("SELECT hashedPassword FROM user WHERE user.id=%s")
    self.cursor.execute(get_hashed_query, (userId,))
    databaseHash = self.cursor.fetchone()[0]

    get_salt_query = ("SELECT salt FROM user WHERE user.id=%s")
    self.cursor.execute(get_salt_query, (userId,))
    databaseSalt = self.cursor.fetchone()[0]
    
    m = hashlib.sha256()
    m.update((databaseSalt + password).encode())
    clientHash = m.hexdigest()

    if (clientHash != databaseHash):
      raise ValueError("Invalid Password")

  def checkLoggedIn(self, userId):
    check_loggedin_query = ("SELECT loggedIn FROM user WHERE user.id=%s")
    self.cursor.execute(check_loggedin_query, (userId,))
    result = self.cursor.fetchone()
    result = result[0]

    if (result == 1):
      return True
    else:
      return False

  def login(self, username, password):
    userId = self.getUserByName(username)
    if (self.checkLoggedIn(userId) == True):
      raise ValueError("You are already logged in.")
    
    self.checkPassword(userId, password)

    set_loggedin_query = ("UPDATE user SET user.loggedIn = 1 WHERE user.id=%s")
    self.cursor.execute(set_loggedin_query, (userId,))
    return True
    
  def getMyEvents(self, userName):
    userId = self.getUserByName(userName)
    get_myevents_query = ("SELECT scheduledEvent.name FROM userinstance JOIN userToEvent ON userinstance.user_id_userinstance=userToEvent.userInstance_id_userToEvent JOIN scheduledEvent ON userToEvent.event_id_userToEvent=scheduledEvent.id WHERE userinstance.user_id_userinstance=%s")
    self.cursor.execute(get_myevents_query, (userId,))
    results = self.cursor.fetchall()
    return results