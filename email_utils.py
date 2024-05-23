# email_utils.py
import sendgrid
from sendgrid.helpers.mail import Mail

SENDGRID_API_KEY = "API_KEY"

def send_email(to_email: str, subject: str, content: str):
    sg = sendgrid.SendGridAPIClient(api_key=SENDGRID_API_KEY)
    # TODO sendGrid API requires an authenticated sender (cannot use personal email)
    from_email = "company_email@company.com"
    message = Mail(from_email=from_email, to_emails=to_email, subject=subject, plain_text_content=content)
    sg.send(message)
