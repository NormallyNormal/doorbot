import hashlib
import os
import sys
from datetime import datetime

import mysql.connector
from dotenv import dotenv_values


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

  def closeConnection(self):
    self.connection.close()

  def getDoorByName(self, name):
    get_door_query = ("SELECT id FROM door AS d WHERE d.displayName=%s")
    self.cursor.execute(get_door_query, (name,))
    doorResult = self.cursor.fetchone()
    if (doorResult != None):
      return doorResult[0]
    raise ValueError("Door Does Not Exist")

  def getUserByUUID(self, uuid):
    get_user_query = ("SELECT id FROM user AS u WHERE u.discordUUID=%s")
    self.cursor.execute(get_user_query, (uuid,))
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

  def doorOpened(self, doorName, userUUID, entryPhotoFileName, openType):
    doorId = self.getDoorByName(doorName)
    userId = self.getUserByUUID(userUUID)
    openTypeId = self.getOpenTypeByName(openType)

    msg = ""
    result_args = self.cursor.callproc('open_door', (doorId, userId, msg))
    msg = result_args[2]
    if ("success" in msg):
      if ("event" not in msg):
        success = False
        self.cursor.callproc('create_open_log', (userId, doorId, entryPhotoFileName, openTypeId, success))
      # success will be True if log was created
    else:
      raise PermissionError(msg) # cannot access door
    
  def getDoors(self, uuid):
    userId = self.getUserByUUID(uuid)
    # all doors (not events)
    get_doors_query = ("SELECT d.displayName, ut.category FROM userinstance AS ui JOIN door AS d ON ui.door_id_userinstance = d.id JOIN usertype AS ut ON ui.userType_id_userinstance = ut.id WHERE ui.user_id_userinstance=%s")
    self.cursor.execute(get_doors_query, (userId,))
    results = self.cursor.fetchall()
    # add doors to doorlist (do not want duplicate entries for events and normal permissions)
    doorlist = []
    for r in results:
      doorlist.append(r[0])
    # event invites
    get_doors_events_query = ("SELECT d.displayName FROM door AS d JOIN scheduledEvent AS se ON se.door_id_scheduledEvent = d.id JOIN userToEvent AS ute ON ute.event_id_userToEvent = se.id WHERE ute.user_id_userToEvent=%s")
    self.cursor.execute(get_doors_events_query, (userId,))
    results_e = self.cursor.fetchall()
    # add new doors to results
    for r in results_e:
      if (r[0] not in doorlist):
        results.append((r[0], 'event')) 
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

  def login(self, userUUID, password):
    userId = self.getUserByUUID(userUUID)
    if (self.checkLoggedIn(userId) == True):
      raise ValueError("You are already logged in.")
    
    self.checkPassword(userId, password)

    set_loggedin_query = ("UPDATE user SET user.loggedIn = 1 WHERE user.id=%s")
    self.cursor.execute(set_loggedin_query, (userId,))
    return True
  
  def logout(self, userUUID):
    userId = self.getUserByUUID(userUUID)
    if (self.checkLoggedIn(userId) == False):
      raise ValueError("You are not logged in.")
    
    set_loggedout_query = ("UPDATE user SET user.loggedIn = 0 WHERE user.id=%s")
    self.cursor.execute(set_loggedout_query, (userId,))
    return True

  def userPermissionUpdate(self, userUUID, doorName, permissionLevel):
    user_id = self.getUserByUUID(userUUID)
    door_id = self.getDoorByName(doorName)

    if not permissionLevel in ["none", "guest", "resident", "admin"]:
      raise ValueError("Bad permission level.")
    
    get_user_instance_query = ("SELECT id FROM userinstance WHERE user_id_userinstance=%s AND door_id_userinstance=%s")
    self.cursor.execute(get_user_instance_query, (user_id, door_id))
    user_instance_id = self.cursor.fetchone()

    permission_id = ""
    get_permission_id_query = ("SELECT id FROM usertype WHERE category=%s")
    self.cursor.execute(get_permission_id_query, (permissionLevel,))
    permission_id = self.cursor.fetchone()[0]

    if (user_instance_id != None):
      set_loggedout_query = ("UPDATE userinstance SET userType_id_userinstance = %s WHERE id=%s")
      self.cursor.execute(set_loggedout_query, (permission_id, user_instance_id[0]))
    else:
      if not permissionLevel == "none":
        add_event_query = ("INSERT INTO userinstance (score, door_id_userinstance, user_id_userinstance, userType_id_userinstance) VALUES (50, %s, %s, %s)")
        self.cursor.execute(add_event_query, (door_id, user_id, permission_id))
      else:
        raise ValueError("User already has no permission.")

  def permissionLevelForDoor(self, userUUID, doorName):
    try:
      userId = self.getUserByUUID(userUUID)
      doorId = self.getDoorByName(doorName)

      get_door_in_userinstance_query = ("SELECT userinstance.id FROM userinstance WHERE userinstance.user_id_userinstance=%s AND userinstance.door_id_userinstance=%s")
      self.cursor.execute(get_door_in_userinstance_query, (userId, doorId))
      result = self.cursor.fetchone()[0]

      get_usertype_query = ("SELECT usertype.category FROM userinstance JOIN usertype ON userinstance.userType_id_userinstance=usertype.id WHERE userinstance.id=%s")
      self.cursor.execute(get_usertype_query, (result, ))
      result = self.cursor.fetchone()[0]
      return result
    except:
      raise ValueError("User has no permissions to complete actions on this door.")

  def setDefault(self, userUUID, doorName):    
    userId = self.getUserByUUID(userUUID)
    doorId = self.getDoorByName(doorName)

    set_default_query = ("UPDATE user SET user.door_id_user = %s WHERE user.id=%s")
    self.cursor.execute(set_default_query, (doorId, userId))

  def getDefault(self, uuid):
    userId = self.getUserByUUID(uuid)
    select_door_name = ("SELECT door.displayName FROM user JOIN door ON user.door_id_user=door.id WHERE user.id=%s")
    self.cursor.execute(select_door_name, (userId,))
    result = self.cursor.fetchone()
    if (result != None):
      return result[0]
    raise ValueError("No default door has been set")

  def getMyEvents(self, uuid):
    userId = self.getUserByUUID(uuid)
    get_myevents_query = ("SELECT se.name, d.displayName FROM user JOIN userToEvent AS ute ON user.id=ute.user_id_userToEvent JOIN scheduledEvent AS se ON ute.event_id_userToEvent=se.id JOIN door AS d ON d.id = se.door_id_scheduledEvent WHERE user.id=%s")
    self.cursor.execute(get_myevents_query, (userId,))
    results = self.cursor.fetchall()
    return results
  
  def getEventByName(self, name):
    get_event_query = ("SELECT id FROM scheduledEvent WHERE name=%s")
    self.cursor.execute(get_event_query, (name,))
    eventResult = self.cursor.fetchone()
    if (eventResult != None):
      return eventResult[0]
    raise ValueError("Event Does Not Exist")
  
  def addUserToEvent(self, invitedUserUUID, eventName): 
    userId = self.getUserByUUID(invitedUserUUID)
    eventId = self.getEventByName(eventName)
    add_to_event_q = ("INSERT INTO userToEvent(user_id_userToEvent, event_id_userToEvent) VALUES (%s, %s)")
    self.cursor.execute(add_to_event_q, (userId, eventId))

  def removeUserFromEvent(self, invitedUserUUID, eventName):
    userId = self.getUserByUUID(invitedUserUUID)
    eventId = self.getEventByName(eventName)
    get_users_in_event_query = ("SELECT ute.user_id_userToEvent FROM userToEvent AS ute WHERE ute.event_id_userToEvent=%s")
    self.cursor.execute(get_users_in_event_query, (eventId, ))
    users_in_event = self.cursor.fetchall()

    if ((userId, ) not in users_in_event):
      raise ValueError("User is not invited, so they cannot be uninvited from the event.")
    
    remove_to_event_q = ("DELETE FROM userToEvent WHERE user_id_userToEvent=%s AND event_id_userToEvent=%s")
    self.cursor.execute(remove_to_event_q, (userId, eventId))

  def permissionLevelForEvent(self, userUUID, eventName):
    try:
      userId = self.getUserByUUID(userUUID)
      get_event_door_query = ("SELECT door_id_scheduledEvent FROM scheduledEvent WHERE name=%s")
      self.cursor.execute(get_event_door_query, (eventName,))
      eventDoorResult = self.cursor.fetchone()[0]
      get_userinstance_permission_query = ("SELECT userType_id_userinstance FROM userinstance AS ui WHERE ui.door_id_userinstance=%s AND ui.user_id_userinstance=%s")
      self.cursor.execute(get_userinstance_permission_query, (eventDoorResult, userId))
      userInstancePermissionResult = self.cursor.fetchone()[0]
      get_permission_name_query = ("SELECT category FROM usertype WHERE id=%s")
      self.cursor.execute(get_permission_name_query, (userInstancePermissionResult,))
      return self.cursor.fetchone()[0]
    except:
      raise ValueError("User has no permissions set")
    
  def addUser(self, discordUUID, password): 
    try:
      self.getUserByUUID(discordUUID)
      raise LookupError("User already exists in the system.")
    except ValueError:
      salt = os.urandom(16).hex()
      m = hashlib.sha256()
      m.update((salt + password).encode())
      hashedPassword = m.hexdigest()

      addUserQuery = ("INSERT INTO user (discordUUID, hashedPassword, salt, developer, loggedIn, door_id_user) VALUES (%s, %s, %s, 0, 0, NULL)")
      self.cursor.execute(addUserQuery, (discordUUID, hashedPassword, salt))

  def editUser(self, discordUUID, password):
    id = self.getUserByUUID(discordUUID)
    salt = os.urandom(16).hex()
    m = hashlib.sha256()
    m.update((salt + password).encode())
    hashedPassword = m.hexdigest()
    addUserQuery = ("UPDATE user SET hashedPassword = %s, salt = %s WHERE id = %s")
    self.cursor.execute(addUserQuery, (hashedPassword, salt, id))