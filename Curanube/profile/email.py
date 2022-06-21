from flask_mail import Message, Mail
#from Curanube import mail
from Curanube.profile import bp as app

def send_email(to, subject, template):
    msg = Message(
        subject,
        recipients=[to],
        html=template,
        sender=app.config["MAIL_DEFAULT_SENDER"]
    )
    Mail(app).send(msg)