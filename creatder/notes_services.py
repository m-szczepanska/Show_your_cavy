import smtplib, ssl
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from django.core.exceptions import ValidationError


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
    mail_contents = \
        f'Reset token is file:///Users/marsza/workspace/zwierzu_front/register.html?token={token}'
    msg.attach(MIMEText(mail_contents,'plain'))
    text = msg.as_string()

    server = smtplib.SMTP('smtp.gmail.com', 2525)
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
    port = 25  # For SSL
    server_email = 'sending.from.python@gmail.com'
    server_email_password = 'gmail9393'
    subject = 'Show your pig and rate other cavies!'


    msg = MIMEMultipart()
    msg['From'] = server_email
    msg['To'] = user_email
    msg['Subject'] = subject
    mail_contents = \
        f'To register go to the link - file:///Users/marsza/workspace/zwierzu_front/register.html?token={token}'
    msg.attach(MIMEText(mail_contents, 'plain'))
    text = msg.as_string()



    # Create a secure SSL context
    context = ssl.create_default_context()

    with smtplib.SMTP_SSL("smtp.gmail.com", port, context=context) as server:
        # TODO: Send email here


    # try:
    #     context = ssl.create_default_context()
    #     server = smtplib.SMTP('smtp.gmail.com', 587)
    # server.ehlo()
        # server.starttls(context=context)
    # server.ehlo() # Can be omitted?
        server.login(server_email, server_email_password)
        server.sendmail(server_email, user_email, text)
        # server.quit()
    # except ConnectionResetError:
        # pass  # server.quit() always cries - but sends mails anyway so...
