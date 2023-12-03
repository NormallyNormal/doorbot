from dotenv import dotenv_values
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
except:
     sys.exit()

class TestDbManager:        
           
    def test_getDoorByName(self):        
        try:
            result = manager.getDoorByName("Random Door")
            assert False
        except ValueError as e:
            assert str(e) == "Door Does Not Exist"
            assert True
        
        result = manager.getDoorByName("Room 403 Door")
        assert result == 1
    
    def test_addEvent(self):

        result = manager.getEvents("Room 403 Door")
        assert len(result) == 1
        assert result[0] == (datetime(2008, 11, 9, 15, 45, 21), datetime(2008, 11, 11, 13, 23, 44), 'Party B', manager.getDoorByName("Room 403 Door"))

        try:
            message = manager.addEvent(datetime(2022, 12, 28, 23, 55, 59), datetime(2023, 12, 28, 23, 55, 59), "Party A", "Random Door")
            assert False
        except ValueError as e:
            assert str(e) == "Door Does Not Exist"
            assert True

        message = manager.addEvent(datetime(2022, 12, 28, 23, 55, 59), datetime(2023, 12, 28, 23, 55, 59), "Party A", "Room 403 Door")        
        assert message == None

        result = manager.getEvents("Room 403 Door")
        assert len(result) == 2
        assert result[0] == (datetime(2008, 11, 9, 15, 45, 21), datetime(2008, 11, 11, 13, 23, 44), 'Party B', manager.getDoorByName("Room 403 Door"))
        assert result[1] == (datetime(2022, 12, 28, 23, 55, 59), datetime(2023, 12, 28, 23, 55, 59), "Party A", manager.getDoorByName("Room 403 Door"))

    def test_getEvents(self):
        try:
            result = manager.getEvents("Random Door")
            assert False
        except ValueError as e:
            assert str(e) == "Door Does Not Exist"
            assert True

        result = manager.getEvents("Room 403 Door")
        assert len(result) == 2
        assert result[0] == (datetime(2008, 11, 9, 15, 45, 21), datetime(2008, 11, 11, 13, 23, 44), 'Party B', manager.getDoorByName("Room 403 Door"))
        assert result[1] == (datetime(2022, 12, 28, 23, 55, 59), datetime(2023, 12, 28, 23, 55, 59), "Party A", manager.getDoorByName("Room 403 Door"))
    
    def test_getUserByName(self):
        try:
            result = manager.getUserByName("joe")
            assert False
        except ValueError as e:
            assert str(e) == "User Does Not Exist"
            assert True

        result = manager.getUserByName("ccrollin")
        assert result == 1
    
    def test_getOpenTypeByName(self):
        try:
            result = manager.getOpenTypeByName("not added type")
            assert False
        except ValueError as e:
            assert str(e) == "Open Type Does Not Exist"
            assert True

        result = manager.getOpenTypeByName("manual")
        assert result == 1
        result = manager.getOpenTypeByName("bot")
        assert result == 2
        result = manager.getOpenTypeByName("scheduled")
        assert result == 3

    def test_getUserInstance(self):
        try:
            result = manager.getUserInstance(manager.getDoorByName("Room 403 Door"), manager.getUserByName("joe"))
            assert False
        except ValueError as e:
            assert str(e) == "User Does Not Exist"
            assert True
        
        try:
            result = manager.getUserInstance(manager.getDoorByName("Random Door"), manager.getUserByName("ccrollin"))
            assert False
        except ValueError as e:
            assert str(e) == "Door Does Not Exist"
            assert True

        result = manager.getUserInstance(manager.getDoorByName("Room 403 Door"), manager.getUserByName("ccrollin"))
        assert result == 1

    def test_doorOpened(self):
        try:
            manager.doorOpened("Random Door", "ccrollin", "images/abc.png", "bot")
            assert False
        except ValueError as e:
            assert str(e) == "Door Does Not Exist"
            assert True

        try:
            manager.doorOpened("Room 403 Door", "joe", "images/abc.png", "bot")
            assert False
        except ValueError as e:
            assert str(e) == "User Does Not Exist"
            assert True

        try:
            manager.doorOpened("Room 403 Door", "ccrollin", "images/abc.png", "random category")
            assert False
        except ValueError as e:
            assert str(e) == "Open Type Does Not Exist"
            assert True

        manager.doorOpened("Room 403 Door", "ccrollin", "images/abc.png", "bot")

        get_entryphoto_query = ("SELECT * FROM entryphoto")
        manager.getCursor().execute(get_entryphoto_query)
        results = manager.getCursor().fetchall()
        assert len(results) == 1
        result = results[0]        
        entryPhotoId = result[0]
        assert result[1] == "images/abc.png"
        assert result[2] == datetime.now().replace(microsecond=0)

        get_openlogs_query = ("SELECT timestamp, door_id_openlog, photo_id_openlog, userInstance_id_openlog, openType_id_openlog FROM openlog")
        manager.getCursor().execute(get_openlogs_query)
        results = manager.getCursor().fetchall()
        assert len(results) == 1
        assert results[0] == (datetime.now().replace(microsecond=0), manager.getDoorByName("Room 403 Door"), entryPhotoId, manager.getUserInstance(manager.getDoorByName("Room 403 Door"), manager.getUserByName("ccrollin")), manager.getOpenTypeByName("bot"))

    def test_getDoors(self):
        try:
            manager.getDoors("joe")
            assert False
        except ValueError as e:
            assert str(e) == "User Does Not Exist"
            assert True

        results = manager.getDoors("ccrollin")
        assert len(results) == 1
        result = results[0]
        assert result[0] ==  "Room 403 Door"
    
    def test_getMyEvents(self):
        try:
            manager.getMyEvents("joe")
            assert False
        except ValueError as e:
            assert str(e) == "User Does Not Exist"
            assert True

        results = manager.getMyEvents("ccrollin")
        assert len(results) == 1
        result = results[0]
        assert result[0] == "Party B"

    def test_checkPassword(self):
        try:
            manager.checkPassword(manager.getUserByName("ccrollin"), "wrongPassword")
            assert False
        except ValueError as e:
            assert str(e) == "Invalid Password"
            assert True

        try:
            manager.checkPassword(manager.getUserByName("ccrollin"), "password")
            assert True
        except:
            assert False
    
    def test_checkLoggedIn(self):
        assert manager.checkLoggedIn(manager.getUserByName("ccrollin")) == False
        assert manager.checkLoggedIn(manager.getUserByName("jtrobin6")) == True

    def test_login(self):
        assert manager.checkLoggedIn(manager.getUserByName("ccrollin")) == False

        try:
            manager.login("nobody", "password")
            assert False
        except ValueError as e:
            assert str(e) == "User Does Not Exist"
            assert True

        try:
            manager.login("jtrobin6", "password")
            assert False
        except ValueError as e:
            assert str(e) == "You are already logged in."
            assert True

        try:
            manager.login("ccrollin", "wrongPassword")
            assert False
        except ValueError as e:
            assert True
            assert str(e) == "Invalid Password"

        assert manager.login("ccrollin", "password") == True
        assert manager.checkLoggedIn(manager.getUserByName("ccrollin")) == True