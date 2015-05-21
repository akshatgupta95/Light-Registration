import sqlite3 as sl

with sl.connect("reg.db") as conn:
	c = conn.cursor()
	c.execute("DROP TABLE IF EXISTS registrations")
	c.execute("CREATE TABLE registrations(name TEXT, email TEXT)")