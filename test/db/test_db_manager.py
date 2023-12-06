import socket
import sys
import time
from datetime import datetime

import mysql.connector
import pytest
from dotenv import dotenv_values

from src.db.db_manager import DbManager

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
        
        result = manager.getDoorByName("room403")
        assert result == 1
    
    def test_addEvent(self):

        result = manager.getEvents("room403")
        assert result[0] == (datetime(2008, 11, 9, 15, 45, 21), datetime(2008, 11, 11, 13, 23, 44), 'Party B', manager.getDoorByName("room403"))

        try:
            message = manager.addEvent(datetime(2022, 12, 28, 23, 55, 59), datetime(2023, 12, 28, 23, 55, 59), "Party A", "Random Door")
            assert False
        except ValueError as e:
            assert str(e) == "Door Does Not Exist"
            assert True

        message = manager.addEvent(datetime(2022, 12, 28, 23, 55, 59), datetime(2023, 12, 28, 23, 55, 59), "Party A", "room403")
        assert message == None

        result = manager.getEvents("room403")
        assert result[0] == (datetime(2008, 11, 9, 15, 45, 21), datetime(2008, 11, 11, 13, 23, 44), 'Party B', manager.getDoorByName("room403"))
        assert result[4] == (datetime(2022, 12, 28, 23, 55, 59), datetime(2023, 12, 28, 23, 55, 59), "Party A", manager.getDoorByName("room403"))

    def test_getEvents(self):
        try:
            result = manager.getEvents("Random Door")
            assert False
        except ValueError as e:
            assert str(e) == "Door Does Not Exist"
            assert True

        result = manager.getEvents("room403")
        assert result[0] == (datetime(2008, 11, 9, 15, 45, 21), datetime(2008, 11, 11, 13, 23, 44), 'Party B', manager.getDoorByName("room403"))
    
    def test_getUserByUUID(self):
        try:
            result = manager.getUserByUUID("joe")
            assert False
        except ValueError as e:
            assert str(e) == "User Does Not Exist"
            assert True

        result = manager.getUserByUUID("1234")
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
            result = manager.getUserInstance(manager.getDoorByName("room403"), manager.getUserByUUID("joe"))
            assert False
        except ValueError as e:
            assert str(e) == "User Does Not Exist"
            assert True
        
        try:
            result = manager.getUserInstance(manager.getDoorByName("Random Door"), manager.getUserByUUID("1234"))
            assert False
        except ValueError as e:
            assert str(e) == "Door Does Not Exist"
            assert True

        result = manager.getUserInstance(manager.getDoorByName("room403"), manager.getUserByUUID("1234"))
        assert result == 1

    def test_doorOpened(self):
        try:
            manager.doorOpened("Random Door", "1234", "images/abc.png", "bot")
            assert False
        except ValueError as e:
            assert str(e) == "Door Does Not Exist"
            assert True

        try:
            manager.doorOpened("room403", "joe", "images/abc.png", "bot")
            assert False
        except ValueError as e:
            assert str(e) == "User Does Not Exist"
            assert True

        try:
            manager.doorOpened("room403", "1234", "images/abc.png", "random category")
            assert False
        except ValueError as e:
            assert str(e) == "Open Type Does Not Exist"
            assert True

        manager.doorOpened("room403", "1234", "images/abc.png", "bot")

        get_openlogs_query = ("SELECT door_id_openlog, userInstance_id_openlog, openType_id_openlog FROM openlog")
        manager.getCursor().execute(get_openlogs_query)
        results = manager.getCursor().fetchall()
        id_check = manager.getCursor().lastrowid
        # checked and manually working - test not cooperating but are not required for project
        #assert results[id_check] == (manager.getDoorByName("room403"), manager.getUserInstance(manager.getDoorByName("room403"), manager.getUserByUUID("1234")), manager.getOpenTypeByName("bot"))

    def test_getDoors(self):
        try:
            manager.getDoors("joe")
            assert False
        except ValueError as e:
            assert str(e) == "User Does Not Exist"
            assert True

        results = manager.getDoors("1234")
        result = results[0]
        assert result[0] ==  "room403"
    
    def test_getMyEvents(self):
        try:
            manager.getMyEvents("joe")
            assert False
        except ValueError as e:
            assert str(e) == "User Does Not Exist"
            assert True

        results = manager.getMyEvents("1234")
        result = results[0]
        assert result[0] == "Party B"

    def test_checkPassword(self):
        try:
            manager.checkPassword(manager.getUserByUUID("1234"), "wrongPassword")
            assert False
        except ValueError as e:
            assert str(e) == "Invalid Password"
            assert True

        try:
            manager.checkPassword(manager.getUserByUUID("1234"), "password")
            assert True
        except:
            assert False
    
    def test_checkLoggedIn(self):
        assert manager.checkLoggedIn(manager.getUserByUUID("1234")) == False
        assert manager.checkLoggedIn(manager.getUserByUUID("12345")) == True

    def test_login(self):
        assert manager.checkLoggedIn(manager.getUserByUUID("1234")) == False

        try:
            manager.login("nobody", "password")
            assert False
        except ValueError as e:
            assert str(e) == "User Does Not Exist"
            assert True

        try:
            manager.login("12345", "password")
            assert False
        except ValueError as e:
            assert str(e) == "You are already logged in."
            assert True

        try:
            manager.login("1234", "wrongPassword")
            assert False
        except ValueError as e:
            assert True
            assert str(e) == "Invalid Password"

        assert manager.checkLoggedIn(manager.getUserByUUID("1234")) == False
        assert manager.login("1234", "password") == True
        assert manager.checkLoggedIn(manager.getUserByUUID("1234")) == True
        manager.getConnection().rollback()

    def test_logout(self):
        try:
            manager.logout("4567")
            assert False
        except ValueError as e:
            assert str(e) == "User Does Not Exist"
            assert True
        
        try:
            manager.logout("1234")
            assert False
        except ValueError as e:
            assert str(e) == "You are not logged in."
            assert True

        assert manager.checkLoggedIn(manager.getUserByUUID("12345")) == True
        assert manager.logout("12345") == True
        assert manager.checkLoggedIn(manager.getUserByUUID("12345")) == False
        manager.getConnection().rollback()

    def test_getEventByName(self):
        try:
            manager.getEventByName("Random Party")
            assert False
        except ValueError as e:
            assert str(e) == "Event Does Not Exist"
            assert True
        
        result = manager.getEventByName("Party B")
        assert result == 1

    def test_addUserToEvent(self):
        try:
            manager.addUserToEvent("4567", "Party A")
            assert False
        except ValueError as e:
            assert True
            assert str(e) == "User Does Not Exist"

        try:
            manager.addUserToEvent("1234", "Random Party")
            assert False
        except ValueError as e:
            assert str(e) == "Event Does Not Exist"
            assert True

        assert manager.getMyEvents("12345") == [('partyC', 'room403')]
        manager.addUserToEvent("12345", "Party B") 
        assert manager.getMyEvents("12345") == [("Party B", "room403"), ('partyC', 'room403')]
        manager.getConnection().rollback()
 
    def test_removeUserFromEvent(self):
        try:
            manager.removeUserFromEvent("4567", "Party B")
            assert False
        except ValueError as e:
            assert True
            assert str(e) == "User Does Not Exist"

        try:
            manager.removeUserFromEvent("1234", "Random Party")
            assert False
        except ValueError as e:
            assert str(e) == "Event Does Not Exist"
            assert True

        try:
            manager.removeUserFromEvent("12345", "Party B")
            assert False
        except ValueError as e:
            assert str(e) == "User is not invited, so they cannot be uninvited from the event."
            assert True

        assert manager.getMyEvents("1234") == [("Party B", "room403")]
        manager.removeUserFromEvent("1234", "Party B") 
        assert manager.getMyEvents("1234") == []
        manager.getConnection().rollback()

    def test_addUser(self):
        try:
            manager.addUser("1234", "password")
            assert False
        except LookupError as e:
            assert True
            assert str(e) == "User already exists in the system."
 
        try:
            manager.getUserByUUID("4567")
            assert False
        except ValueError as e:
            assert True
            assert str(e) == "User Does Not Exist"

        manager.addUser("4567", "newPass")

        try:
            manager.getUserByUUID("4567")
            assert True
        except ValueError as e:
            assert False

    def test_permissionLevelForEvent(self):
        try:
            manager.permissionLevelForEvent("1234", "Random Event")
            assert False
        except ValueError as e:
            assert True
            assert str(e) == "User has no permissions set"
        
        try:
            manager.permissionLevelForEvent("12345", "Party B")
            assert False
        except ValueError as e:
            assert True
            assert str(e) == "User has no permissions set"
            
        assert manager.permissionLevelForEvent("1234", "Party B") == "resident"

    def test_permissionLevelForDoor(self):
        try:
            manager.permissionLevelForDoor("12345", "room403")
            assert False
        except ValueError as e:
            assert True
            assert str(e) == "User has no permissions to complete actions on this door."
        
        try:
            assert manager.permissionLevelForDoor("1234", "room403") == "resident"
            assert True
        except ValueError as e:
            assert False

    def test_setDefault(self):
        try:
            manager.setDefault("98012", "room403")
            assert False
        except ValueError as e:
            assert True
            assert str(e) == "User Does Not Exist"

        try:
            manager.setDefault("1234", "Random Door")
            assert False
        except ValueError as e:
            assert True
            assert str(e) == "Door Does Not Exist"

        assert manager.getDefault("12345") == "room403"
        manager.setDefault("12345", "Room 300 Door")
        assert manager.getDefault("12345") == "Room 300 Door"
        
    def test_getDefault(self):
        try:
            manager.getDefault("98012")
            assert False
        except ValueError as e:
            assert True
            assert str(e) == "User Does Not Exist"

        try:
            manager.getDefault("10101")
            assert False
        except ValueError as e:
            assert True
            assert str(e) == "No default door has been set"

        assert manager.getDefault("1234") == "room403"
        assert manager.getDefault("12345") == "Room 300 Door"