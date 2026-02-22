import sqlite3
import pandas as pd

conn = sqlite3.connect("../day17/internship.db")
cur = conn.cursor()
query = """
SELECT *
FROM student where track=='Data Science' AND stipend>=5000
"""
df = pd.read_sql_query(query, conn)
print(df)
query = """
SELECT track,AVG(stipend) AS avg_stipend
FROM student GROUP BY track
"""
df = pd.read_sql_query(query, conn)
print(df)
print(pd.read_sql_query("SELECT COUNT(*) AS Intern FROM student;", conn))
cur.close()