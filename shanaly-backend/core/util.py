import os
import smtplib
from typing import List
from email.message import EmailMessage
from jinja2 import FileSystemLoader, Environment

# BASE URL
BACKEND_BASE_URL = os.getenv("BACKEND_BASE_URL")
# Google Account -> App Password
GMAIL_APP_PASSWORD = os.getenv("GMAIL_APP_PASSWORD")
AUTO_SENDER = os.getenv("AUTO_SENDER")
SMPT_SERVER_ADDRESS = os.getenv("SMPT_SERVER_ADDRESS")
SMPT_SERVER_PORT_NUMBER = int(os.getenv("SMPT_SERVER_PORT_NUMBER"))

def send_email(subject: str, sender: str, receiver: List[str], html_content: str) -> None:
    '''Common function for write an email with smptlib'''
    msg = EmailMessage()
    msg.add_header('Content-Type','text/html')
    msg["Subject"] = subject
    msg["From"] = AUTO_SENDER
    msg["To"] = ", ".join(receiver)
    msg.set_payload(html_content)
    
    if "xserver.jp" in SMPT_SERVER_ADDRESS:
        # I do not know why but the next code works for X-server in Japan
        with smtplib.SMTP_SSL(SMPT_SERVER_ADDRESS, SMPT_SERVER_PORT_NUMBER) as s:
            s.login(user=AUTO_SENDER, password=GMAIL_APP_PASSWORD)
            s.send_message(msg)
    else:
        with smtplib.SMTP(SMPT_SERVER_ADDRESS, SMPT_SERVER_PORT_NUMBER) as s:
            s.starttls()
            s.login(user=AUTO_SENDER, password=GMAIL_APP_PASSWORD)
            s.send_message(msg)

def send_verification_mail(receiver: str, subject: str, token: str) -> None:
    # Get a HTML template with Jinja2
    env = Environment(loader=FileSystemLoader(str(os.getcwd())+"/templates/"))
    template = env.get_template('email_verification.html')
    output_text = template.render(token=token, base_url=BACKEND_BASE_URL)
    # Send an email with the html content
    send_email(
        subject=subject,
        sender=AUTO_SENDER,
        receiver=[receiver],
        html_content=output_text.encode('utf-8')
    )

def send_reset_password_mail(receiver: str, subject: str, temp_password: str) -> None:
    # Get a HTML template with Jinja2
    env = Environment(loader=FileSystemLoader(str(os.getcwd())+"/templates/"))
    template = env.get_template('reset_password.html')
    output_text = template.render(temp_password=temp_password)
    # Send an email with the html content
    send_email(
        subject=subject,
        sender=AUTO_SENDER,
        receiver=[receiver],
        html_content=output_text.encode('utf-8')
    )