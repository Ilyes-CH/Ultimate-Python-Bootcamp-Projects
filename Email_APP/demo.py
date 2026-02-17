import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from dotenv import load_dotenv
import os

load_dotenv()
# Email credentials and configurations

sender_email = "ilyes.leo.ch@gmail.com"
receiver_email = "c.ilyes@crococoder.tn"
subject = "Test Email From Python"
body = "Hello! This is a test from python hope you are doing fine"

#  Compose Email

msg = MIMEMultipart()
msg["from"] = sender_email
msg["to"] = receiver_email
msg["subject"] = subject
msg.attach(MIMEText(body,"plain"))

# Gmail SMTP Server

smtp_server = "smtp.gmail.com"
port = 587
password= os.getenv("APP_PASSWORD")

#  Send Email
try:
    server = smtplib.SMTP(smtp_server,port)
    server.starttls()
    server.login(sender_email,password)
    server.send_message(msg)
    print("Email Sent Successfully")
except Exception as e:
    print(f"Error: {e}")
finally:
    server.quit()
