# email_utils.py
import sendgrid
from sendgrid.helpers.mail import Mail

SENDGRID_API_KEY = "sendgrid_api_key"

def send_email(to_email: str, subject: str, content: str):
    sg = sendgrid.SendGridAPIClient(api_key=SENDGRID_API_KEY)
    from_email = "nonreply@example.com"
    message = Mail(from_email=from_email, to_emails=to_email, subject=subject, plain_text_content=content)
    sg.send(message)
