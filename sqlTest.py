import pyodbc

cnxn = pyodbc.connect("Driver={ODBC Driver 17 for SQL Server};"
                  "Server=rivsqlb;"
                  "Database=twitterpy;"
                  "uid=twpyadmin;pwd=tw!tterapipains")

cursor = cnxn.cursor()

tableName = "BillyTable"

name = "billy"
username = "@billybee"
text = "this is what billy would say"

cursor.execute(f"""CREATE TABLE {tableName} (
                      Name VARCHAR(50) NOT NULL,
                      Username VARCHAR(15) NOT NULL,
                      Text VARCHAR(1000) NOT NULL);""")
cnxn.commit()

#DONT USE DOUBLE QUOTES
cursor.execute(f"""INSERT INTO {tableName} (Name, Username, Text) 
                VALUES ('{name}', '{username[1:]}', '{text.replace(" ", "_")}');""")
cnxn.commit()


