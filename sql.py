import sqlite3 as sl

with sl.connect("reg.db") as conn:
	c = conn.cursor()
	c.execute("CREATE TABLE registrations(name TEXT, email TEXT)")