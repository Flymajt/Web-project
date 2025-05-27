# pip install mysql-connector
import mysql.connector

mydb = mysql.connector.connect(
    host = "db4free.net",
    user = "toneyadmin",
    password = "qW4rVG58i",
    database = "toneysql"
)

mycursor = mydb.cursor()

mycursor.close()
mydb.close()