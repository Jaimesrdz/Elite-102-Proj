import mysql.connector

connection = mysql.connector.connect(user = 'root', database = 'example', password = 'creeperS!1')

cursor = connection.cursor()

 
addData = ("INSERT INTO example_table (id, name, country) "
           "VALUES ('5', 'cri', 'Mexico')")



cursor.execute(addData)

connection.commit()
cursor.close()

connection.close()