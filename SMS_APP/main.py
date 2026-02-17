from taipy.gui import Gui
import os
from twilio.rest import Client
from dotenv import load_dotenv
from threading import Timer
from datetime import datetime, timedelta

load_dotenv()

account_sid = os.getenv('TWILIO_ACCOUNT_SID') 
auth_token = os.getenv('TWILIO_AUTH_TOKEN')  

print(account_sid,auth_token)

# State Varirables
destination = ""
message_body= ""
delay_minutes = 1
status_message=""
status_class = ""

def send_sms(destination,message_body):
    try:
        #  Creating the Twillio Client 
        client = Client(account_sid, auth_token)
        message = client.messages.create(
                    body=message_body,
                    from_='+17439026601',
                    to=destination
                )
        print(message.sid)
        print(f"[{datetime.now()}] ✅ SMS sent to {destination}")
    except Exception as e:
        
        print(f"[{datetime.now()}] ❌  SMS Failed to be sent: {e}")

def schedule_sms(state):
    try:
        send_time = datetime.now() + timedelta(minutes=int(state.delay_minutes))
        delay_seconds = (send_time - datetime.now()).total_seconds()

        Timer(delay_seconds,send_sms,args=(state.destination,state.message_body)).start()
        state.status_message = f" SMS Scheduled for {send_time.strftime('%Y-%m-%d %H:%M:%S')}"
        state.status_class = "my-status green"
    except Exception as e:
        state.status_message = f" SMS Scheduling failed {str(e)}"
        state.status_class = "my-status red"

page = """

## SMS Sender App

### Phone Number

<|{destination}|input|label= To (e.g +1234567890)|>

### Delay

<|{delay_minutes}|number|label=Send After How many minutes?|>


### Message

<|{message_body}|input|multiline=True|label= Message Body|>

<|Schedule|button|on_action=schedule_sms|>

### Status

<|{status_message}|text|class_name={status_class}|>


"""
# Run The App

Gui(page).run()