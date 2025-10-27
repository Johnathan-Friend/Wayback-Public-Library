import os
from dotenv import load_dotenv
import socket

load_dotenv()

### DATABASE CONFIGURATION VARIABLES
MYSQL_HOST = socket.gethostbyname(os.getenv("MYSQL_HOST"))
MYSQL_PORT = os.getenv("MYSQL_PORT")
MYSQL_DB = os.getenv("MYSQL_DB")
MYSQL_USER = os.getenv("MYSQL_USER")
MYSQL_PASSWORD = os.getenv("MYSQL_PASSWORD")
