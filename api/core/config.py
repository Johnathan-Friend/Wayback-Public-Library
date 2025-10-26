import os
import socket
from dotenv import load_dotenv

# Load environment variables from a .env file (in api/ folder)
load_dotenv()

# Get environment variables with safe defaults
MYSQL_USER = os.getenv("MYSQL_USER", "root")
MYSQL_PASSWORD = os.getenv("MYSQL_PASSWORD", "")
MYSQL_HOST = os.getenv("MYSQL_HOST", "localhost")
MYSQL_PORT = os.getenv("MYSQL_PORT", "3306")
MYSQL_DB = os.getenv("MYSQL_DB", "wayback_library")

# Resolve host safely (avoid crash if None)
try:
    MYSQL_HOST = socket.gethostbyname(MYSQL_HOST)
except Exception as e:
    print(f"⚠️ Warning: could not resolve MYSQL_HOST '{MYSQL_HOST}' — {e}")
