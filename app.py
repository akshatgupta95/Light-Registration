from flask import Flask, session, request, render_template, g
import sqlite3 as sl
import os

app = Flask(__name__)

sec_k = os.urandom(24)
app.secret_key = sec_k

app.database = "reg.db"

@app.route('/')
def index():
	return render_template('index.html')

@app.route('/subscribe')
def subscribe():
	return render_template('subscribe.html')

@app.route('/request_handler', methods=['GET', 'POST'])
def request_handler():
	name = request.form['yourname']
	email = request.form['youremail']
	g.db = connect_db()
	params = (str(name), str(email))
	print (params)
	g.db.execute("INSERT INTO registrations VALUES (?, ?)", params)
	print ("Inserted")
	g.db.close()
	return render_template('index.html')

@app.route('/unsubscribe')
def unsubscribe():
	return render_template('unsubscribe.html')

@app.route('/unsubscribe_handler', methods=['GET', 'POST'])
def unsubscribe_handler():
	name = request.form['yourname']
	email = request.form['youremail']
	g.db = connect_db()
	cur = g.db.execute('SELECT * FROM registrations')
	posts = [dict(name=row[0], email=row[1]) for row in cur.fetchall()]
	print (posts)
	return render_template('index.html')



def connect_db():
	return sl.connect(app.database)


if __name__ == '__main__':
	app.run(debug=True)