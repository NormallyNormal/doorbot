# code snippet from azure deployment center
from dotenv import dotenv_values
import mysql.connector

# read username and password from db.env file and pass ssl ca cert
config = dotenv_values("db.env")
cnx = mysql.connector.connect(user=config["DB_USERNAME"], password=config["DB_PASSWORD"], host=config["DB_HOSTNAME"], port=config["DB_PORT"], database=config["DB_NAME"], ssl_ca="DigiCertGlobalRootG2.crt.pem", ssl_disabled=False)
print("Connected")
