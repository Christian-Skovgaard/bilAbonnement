import mysql.connector
from mysql.connector import Error
from dotenv import load_dotenv
import os

load_dotenv()

DB_CONFIG = {
    'host': os.getenv("DB_HOST"),      # husk at ændre fra localhost
    'port': os.getenv("DB_PORT"),
    'user': os.getenv("DB_USERNAME"),
    'password': os.getenv("DB_PASSWORD"),
    'database': 'user_db'
}

def create_connection():
        connection = mysql.connector.connect(**DB_CONFIG)
        if connection.is_connected():
            print("Touchdown!!!!")
            return connection
        else:
             print("failed to connect to DB")
             return None

def fetch_all_users(): 
    conn = create_connection()
   
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM users;")
    results = cursor.fetchall()
    
    cursor.close()
    conn.close()

    return results

def fetch_user_by_username(username):
    conn = create_connection()

    cursor = conn.cursor(dictionary=True)
    query = "SELECT * FROM users WHERE username = %s;" # på den her måde beskytter vi mod sql injection som er vigtigt her fordi det er tilgængeligt for alle
    
    cursor.execute(query, (username,))
    result = cursor.fetchone()

    cursor.close()
    conn.close()

    return result


def insert_user():
    None
