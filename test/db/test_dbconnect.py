from dotenv import dotenv_values
import mysql.connector
import pytest

import socket
import time

config = dotenv_values("db.env")

@pytest.fixture(autouse=True)
def wait_for_server():
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    while sock.connect_ex((config["DB_HOSTNAME"], int(config["DB_PORT"]))) != 0:
        time.sleep(2)
    sock.close()
    yield

def test_dbconnection():
    try:
        cnx = mysql.connector.connect(user=config["DB_USERNAME"], password=config["DB_PASSWORD"], host=config["DB_HOSTNAME"], port=config["DB_PORT"], database=config["DB_NAME"], ssl_disabled=False)
        assert True
    except mysql.connector.Error as err:
        print(err)
        assert False
    else:
        cnx.close()
