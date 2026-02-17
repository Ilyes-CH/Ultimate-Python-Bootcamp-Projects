from taipy.gui import Gui
import os
from dotenv import load_dotenv
from threading import Timer
from datetime import datetime, timedelta
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

load_dotenv()

# Email credentials and configurations

sender_email = os.getenv("SENDER")
receiver_email = ""
subject = ""
body = ""


smtp_server = "smtp.gmail.com"
port = 587
password= os.getenv("APP_PASSWORD")


# State Varirables

delay_minutes = 1
status_message=""
status_class = ""

def send_email(to, subject, body):
    # Compose Email
    msg = MIMEMultipart()
    msg["from"] = sender_email
    msg["to"] = to
    msg["subject"] = subject
    msg.attach(MIMEText(body, "plain"))

    try:
        server = smtplib.SMTP(smtp_server, port)
        server.starttls()
        server.login(sender_email, password)
        server.send_message(msg)
        print(f"[{datetime.now()}] ✅ Email sent")
    except Exception as e:
        print(f"[{datetime.now()}] ❌ Email Failed to be sent: {str(e)}")
    finally:
        server.quit()


def schedule_email(state):
    try:
        to = state.receiver_email
        subject = state.subject
        email_body = state.body
        delay_minutes_local = int(state.delay_minutes)

        send_time = datetime.now() + timedelta(minutes=delay_minutes_local)
        delay_seconds = (send_time - datetime.now()).total_seconds()

        Timer(delay_seconds, send_email, args=(to, subject, email_body)).start()

        state.status_message = f" Email scheduled for {send_time.strftime('%Y-%m-%d %H:%M:%S')}"
        state.status_class = "my-status green"
    except Exception as e:
        state.status_message = f" Email scheduling failed: {str(e)}"
        state.status_class = "my-status red"

page = """
<style>
main,body{

background-color:#023020 !important;
}
input{
flex:1;
}
main{
display:flex;
justify-content:center;
align-items:center;
}
h1,h2,h3{
text-align:center;
}
button{
}
.my-status {
  font-weight: bold;
}
.my-status.green {
  color: green;
}
.my-status.red {
  color: red;
}
</style>

## Email Sender App

### Email Address

<|{receiver_email}|input|label= To (e.g example@example.com)|>

### Delay

<|{delay_minutes}|number|label=Send After How many minutes?|>


### Message
<|{subject}|input|multiline=True|label= Email Subject|>

<|{body}|input|multiline=True|label= Email Body|>

<|Schedule|button|on_action=schedule_email|>

### Status

<|{status_message}|text|class_name={status_class}|>


"""
# Run The App

Gui(page).run()