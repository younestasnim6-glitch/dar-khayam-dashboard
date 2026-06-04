import mysql.connector

def get_connection():
    return mysql.connector.connect(
        host="acela.proxy.rlwy.net",
        port=27644,
        user="root",
        password="coWAWYvrvZJwiVfbDpwYQrCDzzRNhPaa",
        database="railway"
    )
