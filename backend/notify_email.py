import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import os

def send_signup_notification(name, email, to_emails):
    """
    Send an email notification to the specified addresses when a new signup occurs.
    """
    smtp_server = 'smtp.gmail.com'
    smtp_port = 587
    gmail_user = os.getenv('NOTIFY_GMAIL_USER', 'zemouli.abdelkarim.2005@gmail.com')
    gmail_password = os.getenv('NOTIFY_GMAIL_PASS')  # Set this in your environment

    if not gmail_user or not gmail_password:
        raise RuntimeError('Gmail credentials not set in environment variables.')

    subject = 'New Cyndro Landing Page Registration'
    body = f"""
    A new user has registered on the Cyndro landing page.\n\n    Name: {name}\n    Email: {email}\n    """

    msg = MIMEMultipart()
    msg['From'] = gmail_user
    msg['To'] = ', '.join(to_emails)
    msg['Subject'] = subject
    msg.attach(MIMEText(body, 'plain'))

    try:
        server = smtplib.SMTP(smtp_server, smtp_port)
        server.starttls()
        server.login(gmail_user, gmail_password)
        server.sendmail(gmail_user, to_emails, msg.as_string())
        server.quit()
    except Exception as e:
        print(f"Failed to send notification email: {e}")
