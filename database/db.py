import mysql.connector

def get_connection():
    connection = mysql.connector.connect(
        host="localhost",
        user="root",
        password="welcome",
        database="ai_code_review_portal"
    )
    return connection