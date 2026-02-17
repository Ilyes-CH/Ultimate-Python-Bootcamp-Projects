from flask import Flask, render_template, request, redirect, url_for, flash
import smtplib
from email.message import EmailMessage
from dotenv import load_dotenv
import os

load_dotenv()

app = Flask(__name__)
app.secret_key = os.getenv("SECRET")
# Email Config
SMTP_SERVER = "smtp.gmail.com"
SMTP_PORT = 587
EMAIL_ADDRESS = os.getenv("EMAIL_ADDRESS")
EMAIL_PASSWORD = os.getenv("APP_SECRET")


@app.route("/")
def home():
    return render_template("index.html")

@app.route("/resume")
def resume():
    return render_template("resume.html")


@app.route("/contact",methods=["GET","POST"])
def contact():

    if request.method == "POST":
        name = request.form.get("name")
        sender_email = request.form.get("email")
        message = request.form.get("message")

        if not name or not message or not sender_email:
            flash("Please Fill In All Fields","error")
            return redirect(url_for("contact"))
        
        # Compose Email
        email_message = EmailMessage()
        email_message["subject"] = f"Portfolio Contact From {name}"
        email_message["From"] = EMAIL_ADDRESS
        email_message["To"] = EMAIL_ADDRESS
        email_message.set_content(f"Name: {name}\nEmail: {sender_email}\nMessage: \n{message}")

        try:
            with smtplib.SMTP(SMTP_SERVER,SMTP_PORT) as smtp:
                smtp.starttls()
                smtp.login(EMAIL_ADDRESS,EMAIL_PASSWORD)
                smtp.send_message(email_message)
                flash("Message Sent Successfully","success")
                return redirect(url_for("contact"))
        except Exception as e:
            flash("Falied To Send Message","error")
            print("Error in sending Email: ",e)

    return render_template("contact.html")

if __name__ == "__main__":
    app.run(debug=True)