import mysql.connector
import json, random
import string

try:
  with open('mysql.json', 'r') as file:
    config = json.load(file)
except FileNotFoundError:
  config = {}
  
db_host = config['host']
db_user = config['username']
db_pw = config['password']
db_name = config['database']

def check_mysql_connection():
    try:
        connection = mysql.connector.connect(
        host=db_host,
        user=db_user,
        password=db_pw,
        database=db_name
        )
        return True

    except mysql.connector.Error as err:
        print(f"Error: {err}")
        return False
    finally:
        if 'connection' in locals() and connection.is_connected():
            connection.close()
            
def reset_password(discord_id, new_password):
    connection = mysql.connector.connect(
        host=db_host,
        user=db_user,
        password=db_pw,
        database=db_name
    )

    try:
        cursor = connection.cursor()
        old_pin_query = "SELECT `verifycode` FROM `playerucp` WHERE `DiscordID` = %s"
        old_pin_data = (discord_id,)
        cursor.execute(old_pin_query, old_pin_data)
        old_pin_result = cursor.fetchone()
        old_pin = old_pin_result[0] if old_pin_result else None
        
        new_pin = generate_pin()
        
        pin_query = "UPDATE `playerucp` SET `verifycode` = %s WHERE `DiscordID` = %s"
        pin_data = (new_pin, discord_id)
        cursor.execute(pin_query, pin_data)
        
        password_query = "UPDATE `playerucp` SET `password` = %s WHERE `DiscordID` = %s"
        password_data = (new_password, discord_id)
        cursor.execute(password_query, password_data)
        
        connection.commit()
        return old_pin, new_pin
    except mysql.connector.Error as err:
        print(f"Error: {err}")
    finally:
        if 'cursor' in locals():
            cursor.close()
        if 'connection' in locals() and connection.is_connected():
            connection.close()

def generate_pin():
    return ''.join(random.choices('0123456789', k=5))
    
def register_user(ucp_name, verifycode, discord_id, password, salt, extrac):
    connection = mysql.connector.connect(
        host=db_host,
        user=db_user,
        password=db_pw,
        database=db_name
    )

    try:
        cursor = connection.cursor()
        query = "INSERT INTO playerucp (ucp, verifycode, DiscordID, password, salt, extrac) VALUES (%s, %s, %s, %s, %s, %s)"
        data = (ucp_name, verifycode, discord_id, password, salt, extrac)
        cursor.execute(query, data)
        connection.commit()
        
        return result
    except mysql.connector.Error as err:
        print(f"Error: {err}")
    finally:
        if 'cursor' in locals():
            cursor.close()
        if 'connection' in locals() and connection.is_connected():
            connection.close()

def check_id(user_id):
    connection = mysql.connector.connect(
        host=db_host,
        user=db_user,
        password=db_pw,
        database=db_name
    )

    try:
        cursor = connection.cursor(dictionary=True)
        query = "SELECT ucp FROM playerucp WHERE DiscordID = %s"
        data = (user_id,)
        cursor.execute(query, data)
        result = cursor.fetchone()

        return result
    except mysql.connector.Error as err:
        print(f"Error: {err}")
        return None
    finally:
        if 'cursor' in locals():
            cursor.close()
        if 'connection' in locals() and connection.is_connected():
            connection.close()
            
def ucp_check(ucp):
    connection = mysql.connector.connect(
        host=db_host,
        user=db_user,
        password=db_pw,
        database=db_name
    )

    try:
        cursor = connection.cursor(dictionary=True)
        query = "SELECT ucp FROM playerucp WHERE ucp = %s"
        data = (ucp,)
        cursor.execute(query, data)
        result = cursor.fetchone()

        return result
    except mysql.connector.Error as err:
        print(f"Error: {err}")
        return None
    finally:
        if 'cursor' in locals():
            cursor.close()
        if 'connection' in locals() and connection.is_connected():
            connection.close()
  
def get_user_info(user_id):
    connection = mysql.connector.connect(
        host=db_host,
        user=db_user,
        password=db_pw,
        database=db_name
    )

    try:
        cursor = connection.cursor(dictionary=True)
        query = "SELECT DiscordID, ucp, verifycode FROM playerucp WHERE DiscordID = %s"
        data = (user_id,)

        cursor.execute(query, data)
        result = cursor.fetchone()

        return result
    except mysql.connector.Error as err:
        print(f"Error: {err}")
        return None
    finally:
        if 'cursor' in locals():
            cursor.close()
        if 'connection' in locals() and connection.is_connected():
            connection.close()