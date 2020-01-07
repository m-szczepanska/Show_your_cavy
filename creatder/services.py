import smtplib, ssl
import os
import sys

from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

from django.core.exceptions import ValidationError
try:
    from production import DOMAIN_URL
except ImportError:
    print('You should create a production.py settings file.')
    from settings import DOMAIN_URL


class MinimumLengthValidator:
    min_length = 8

    @classmethod
    def validate(cls, password):
        if len(password) < cls.min_length:
            return False
        return True


class NumericPasswordValidator:

    @classmethod
    def validate(cls, password):
        return any(i.isdigit() for i in password)


def send_password_reset_mail(user_email, token):
    server_email = 'sending.from.python@gmail.com'
    server_email_password = 'gmail9393'
    subject = 'Password Reset'

    msg = MIMEMultipart()
    msg['From'] = server_email
    msg['To'] = user_email
    msg['Subject'] = subject
    # TODO: Make this text better
    mail_contents = f'<html><body><h1>Squeakoo Password Reset</h1><br><p>Click <a href="{DOMAIN_URL}/password_reset.html?token={token}">here</a> to set your new password on Squeakoo</p></body></html>'
    msg.attach(MIMEText(mail_contents,'html', 'utf-8'))
    text = msg.as_string()

    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.ehlo()
    server.starttls()
    server.login(server_email, server_email_password)
    server.sendmail(server_email,user_email, text)
    server.quit()


def check_token_validity(cls, token_uuid):
        # Check if token is in db (bad: user tried to hack and typed their own
        # token)
        try:
            token = cls.objects.get(uuid=token_uuid)
        except:
            context = {"error": "Invalid token"}
            return context

        # Check if token is valid
        if not token.is_valid:
            context = {"error": "Token expired"}
            return context

        return None


def send_user_register_mail(user_email, token):
        server_email = 'sending.from.python@gmail.com'
        server_email_password = 'gmail9393'
        subject = 'Password Reset'

        msg = MIMEMultipart()
        msg['From'] = server_email
        msg['To'] = user_email
        msg['Subject'] = subject
        # TODO: Make this text better
        mail_contents = \
            f'Click this link to create your account on Squeakoo --> file:///Users/marsza/workspace/zwierzu_front/register.html?token={token}'
        msg.attach(MIMEText(mail_contents,'plain'))
        text = msg.as_string()

        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.ehlo()
        server.starttls()
        server.login(server_email, server_email_password)
        server.sendmail(server_email,user_email, text)
        server.quit()



def delete_pig_photo(pig_photo):

    print('print', pig_photo)

    if os.path.exists(f'/Users/marsza/workspace/media/{pig_photo}'):
        os.remove(f'/Users/marsza/workspace/media/{pig_photo}')
    else:
        print("The file does not exist")
