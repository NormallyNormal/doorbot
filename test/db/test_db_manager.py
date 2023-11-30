from dotenv import dotenv_values
import os
import sys

from src.db.db_manager import DbManager
import mysql.connector
import pytest

import socket
import time
import sys

from datetime import datetime

config = dotenv_values("db.env")
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
while sock.connect_ex((config["DB_HOSTNAME"], int(config["DB_PORT"]))) != 0:
     time.sleep(2)
sock.close()
        
try:
     manager = DbManager()
     connection = manager.getConnection()
except:
     sys.exit()

class TestDbManager:        
    
    def setup_test_data(self):
        add_door_info_query = ("INSERT INTO doorInfo (status, ipAddress, dns, port) VALUES (%s, %s, %s, %s)")
        manager.getCursor().execute(add_door_info_query, ("online", "10.10.10.67", "door403", 22))        
        add_door_query = ("INSERT INTO door (displayName, location, doorInfo_id_door) VALUES (%s, %s, %s)")
        manager.getCursor().execute(add_door_query, ("Room 403 Door", "Lakeview", 1))
           
    def test_getDoorByName(self):
        result = manager.getDoorByName("Room 403 Door")
        assert result == 1
        result = manager.getDoorByName("Random Door")
        assert result == None
    
    def test_addEvent(self):
        message = manager.addEvent(datetime(2022, 12, 28, 23, 55, 59), datetime(2023, 12, 28, 23, 55, 59), "Party A", "Random Door")
        check_event_query = ("SELECT * FROM scheduledEvent")
        manager.getCursor().execute(check_event_query)
        result = manager.getCursor().fetchone()
        
        assert message == "That is not a valid door"
        assert result == None
    
        message = manager.addEvent(datetime(2022, 12, 28, 23, 55, 59), datetime(2023, 12, 28, 23, 55, 59), "Party A", "Room 403 Door")
        check_event_query = ("SELECT * FROM scheduledEvent")
        manager.getCursor().execute(check_event_query)
        result = manager.getCursor().fetchone()
        
        assert message == None
        assert result != None
        assert result[1] == datetime(2022, 12, 28, 23, 55, 59)
        assert result[2] == datetime(2023, 12, 28, 23, 55, 59)
        assert result[3] == "Party A"
        assert result[4] == 1
