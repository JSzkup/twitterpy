import pyodbc

cnxn = pyodbc.connect("Driver={ODBC Driver 17 for SQL Server};"
                  "Server=rivsqlb;"
                  "Database=twitterpy;"
                  "uid=twpyadmin;pwd=tw!tterapipains")

cursor = cnxn.cursor()


cursor.execute(f"""CREATE TABLE SEARCH_QUERY (
                      name VARCHAR(50) NOT NULL,
                      username VARCHAR(15) NOT NULL,
                      text VARCHAR(1000) NOT NULL,
                    );""")
cnxn.commit()

cursor.execute(f"""INSERT INTO SEARCH_QUERY (name, username, text) 
                VALUES ("name", "username", "text");""")
cnxn.commit()


