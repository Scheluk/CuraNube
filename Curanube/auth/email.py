from inspect import ArgSpec
from threading import Thread
from flask_mail import Message
from Curanube import mail
from flask import current_app

def send_email(to, subject, template):  #send a email to an reipient with a subject and template (content of mail)
    msg = Message(
        subject, 
        recipients=[to],
        html=template,
        sender=current_app.config["MAIL_DEFAULT_SENDER"]    #the sender as defined in the app.config
        )
    mail.send(msg)