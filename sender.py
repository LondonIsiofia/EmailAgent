import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from config import EMAIL_SENDER, EMAIL_RECIEVER, EMAIL_PASS

def send_email(subject: str, body: str, to_email: str = None):
    to_email = to_email or EMAIL_RECIEVER
    msg = MIMEMultipart()
    msg["From"] = EMAIL_SENDER
    msg["To"] = to_email
    msg["Subject"] = subject
    msg.attach(MIMEText(body, "plain"))
    
    with smtplib.SMTP("smtp.gmail.com", 587) as server:
        server.starttls()
        server.login(EMAIL_SENDER, EMAIL_PASS)
        server.send_message(msg)
    print(f"[email] Sent: {subject} -> {to_email}")