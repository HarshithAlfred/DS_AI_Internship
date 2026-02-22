# columns: id, name, track (e.g., Data Science, Web Dev), and stipend.
import sqlite3
import pandas as pd

con = sqlite3.connect("internship.db")
cur = con.cursor()
cur.execute("DROP TABLE IF EXISTS student")
cur.execute("CREATE Table student( " \
"id INTEGER , name TEXT , track TEXT , stipend INTEGER )")

cur.execute("INSERT INTO student VALUES (01,'Mark','Data Science',12000)")
cur.execute("INSERT INTO student VALUES (02,'Britto','Web DEV',18000)")
cur.execute("INSERT INTO student VALUES (03,'Sean','Data Science',15000)")
cur.execute("INSERT INTO student VALUES (04,'Tom','Web Dev',18000)")
cur.execute("INSERT INTO student VALUES (05,'John','Data Science',21000)")
con.commit()
df = pd.read_sql_query("Select name , track from student",con)
print(df)
con.close()