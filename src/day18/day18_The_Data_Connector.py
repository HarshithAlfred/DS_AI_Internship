#Create a second table mentors with mentor_id, mentor_name, and track.
import sqlite3
import pandas as pd
con = sqlite3.connect("../day17/internship.db")

cur = con.cursor()
cur.execute('DROP Table IF EXISTS mentor')
cur.execute("CREATE TABLE mentor(mentor_id INTEGER,mentor_name TEXT ,track TEXT)")
cur.execute("INSERT INTO mentor VALUES (01,'Clara','Data Science')")
cur.execute("INSERT INTO mentor VALUES (02,'Jarold','Web Dev')")
con.commit()
query = pd.read_sql_query("Select * from mentor",con)
print(query)
query = pd.read_sql_query("Select student.name , mentor.mentor_name from student INNER JOIN mentor on student.track=mentor.track",con)
print(query)
cur.close()