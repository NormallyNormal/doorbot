from dotenv import dotenv_values
import mysql.connector
import sys

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
    get_door_query = ("SELECT * FROM door AS d WHERE d.displayName=%s")
    self.cursor.execute(get_door_query, (name,))
    doorResult = self.cursor.fetchone()
    if (doorResult != None):
      return doorResult[0]
    return None

  def addEvent(self, timeStart, timeEnd, name, doorName):
    add_event_query = ("INSERT INTO scheduledEvent (timeStart, timeEnd, name, door_id_scheduledEvent) VALUES (%s, %s, %s, %s)")
    doorId = self.getDoorByName(doorName)
    if doorId == None:
      return "That is not a valid door"
    self.cursor.execute(add_event_query, (timeStart, timeEnd, name, doorId))
