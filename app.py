from flask import Flask, request, render_template, g
import sqlite3 as sl
import os
from twilio.rest import TwilioRestClient

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
	num = request.form['yournum']
	g.db = connect_db()
	params = (str(name), str(email), str(num))
	curr = g.db.cursor()
	curr.execute("INSERT INTO registrations VALUES (?, ?, ?)", params)
	cur = g.db.execute('SELECT * FROM registrations')
	regs = [dict(name=row[0], email=row[1], phone=row[2]) for row in cur.fetchall()]
	g.db.commit()
	curr.close()
	return render_template('index.html', regs=regs)

@app.route('/unsubscribe')
def unsubscribe():
	return render_template('unsubscribe.html')

@app.route('/unsubscribe_handler', methods=['GET', 'POST'])
def unsubscribe_handler():
	name = request.form['yourname']
	email = request.form['youremail']
	num = request.form['yournum']
	params = (str(name), str(email), str(num))
	g.db = connect_db()
	c = g.db.cursor()
	c.execute("DELETE FROM registrations WHERE name=? AND email=? AND phone=?", params)
	g.db.commit()
	cur = g.db.execute('SELECT * FROM registrations')
	regs = [dict(name=row[0], email=row[1], phone=row[2]) for row in cur.fetchall()]
	c.close()
	return render_template('index.html', regs=regs)


@app.route('/text')
def text():
	return render_template('text.html')


@app.route('/text_handler', methods=['GET', 'POST'])
def text_handler():
	name = request.form['yourname']
	mesg = request.form['msg']
	params = (str(name),)
	g.db = connect_db()
	c = g.db.cursor()
	cur = c.execute("SELECT phone FROM registrations WHERE name=?", params)
	num = [dict(phone=row[0]) for row in cur.fetchall()][0]['phone']
	num = str(num)
	data = {'name' : name, 'phone' : num}
	send_msg(num, mesg)
	c.close()
	return render_template('text_output.html', data=data)

def send_msg(num, mesg):
	account_sid = "ACe85795fdf3a490fab8dfcf69bdf4d973"
	auth_token  = "47ff734df2b4c1d97f6a6640f8fd2ea5"
	client = TwilioRestClient(account_sid, auth_token)
	 
	message = client.messages.create(body=mesg,
	    to="+%s" % str(num),    # Replace with your phone number
	    from_="+19073121192") # Replace with your Twilio number
	return None

def connect_db():
	return sl.connect(app.database)


if __name__ == '__main__':
	app.run(debug=True)