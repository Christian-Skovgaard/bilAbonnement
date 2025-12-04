import os
import time
import mysql.connector
from dotenv import load_dotenv

load_dotenv()

def get_connection(retries=3, delay=1):
    """Return a new mysql.connector connection using env vars."""
    host = os.getenv('DB_HOST')
    user = os.getenv('DB_USER')
    password = os.getenv('DB_PASSWORD')
    database = os.getenv('DB_NAME')

    last_exc = None
    for _ in range(retries):
        try:
            conn = mysql.connector.connect(
                host=host,
                user=user,
                password=password,
                database=database
            )
            return conn
        except Exception as e:
            last_exc = e
            time.sleep(delay)
    raise last_exc