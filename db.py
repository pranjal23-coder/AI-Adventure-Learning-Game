import mysql.connector

connection= mysql.connector.connect(
    host="localhost",
    user="root",
    password="pranjal",
    database="ai_game"
)



if connection.is_connected():
    print("Database Connected Successfully")