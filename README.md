# Light-Registration

This a light-weight registration (subscription and unsubscription) tool built using Python Flask, HTML/CSS.
The subscriptions are stored/queried using sqlite3.

Send texts to Twilio verifed numbers.

You may download the latest working release (Light Registration with Texting).

Before running this app, replace the following lines in ```app.py``` with your own Twilio details.
```
account_sid = ""	# insert your account_sid
auth_token  = ""	# your own auth_token
message = client.messages.create(body=mesg,
	    to="+%s" % str(num),    
	    from_="+") # Replace with your Twilio number
```

```
./light_reg
```
This should by default, run on localhost port 5000.
