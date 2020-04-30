import pyodbc

cnxn = pyodbc.connect("Driver={ODBC Driver 17 for SQL Server};"
                      r"Server=JON\SQLEXPRESS;"
                      "Database=msdb;"
                      "Trusted_Connection=yes")

cursor = cnxn.cursor()

cursor.execute(f"""CREATE TABLE TableName (
                        tweet_name NVARCHAR(60) NOT NULL,
                        tweet_user NVARCHAR(20) NOT NULL,
                        tweet_text NVARCHAR(1000) NOT NULL);""")
cnxn.commit()

cursor.execute(f"""INSERT INTO TableName
                        (tweet_name, tweet_user, tweet_text)
                    VALUES
                    ('Bop'),
                    ('@Bloop'),
                    ('I_am_Blop_Boop');""")
cnxn.commit()
cnxn.close()
