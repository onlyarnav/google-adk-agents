import os
import base64
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build

# If modifying these scopes, delete the file token.json.
SCOPES = ['https://www.googleapis.com/auth/gmail.modify']

class GmailAgent:
    """
    Professional Gmail Agent for automating email communication.
    Supports advanced features like CC, BCC, attachments, and HTML content.
    """
    def __init__(self):
        self.service = self._authenticate()

    def _authenticate(self):
        creds = None
        if os.path.exists('token.json'):
            creds = Credentials.from_authorized_user_file('token.json', SCOPES)

        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file(
                    'credentials.json', SCOPES)
                creds = flow.run_local_server(port=0)
            with open('token.json', 'w') as token:
                token.write(creds.to_json())

        return build('gmail', 'v1', credentials=creds)

    def send_email(self, to, subject, body, cc=None, bcc=None, attachments=None, is_html=False):
        """
        Sends a professional email.

        Args:
            to (list|str): Main recipient(s).
            subject (str): Email subject.
            body (str): Email content.
            cc (list|str, optional): CC recipients.
            bcc (list|str, optional): BCC recipients.
            attachments (list, optional): List of file paths to attach.
            is_html (bool): If True, renders body as HTML (allows links).
        """
        def format_recipients(recipients):
            if isinstance(recipients, list):
                return ", ".join(recipients)
            return recipients

        to_str = format_recipients(to)
        cc_str = format_recipients(cc) if cc else ""
        bcc_str = format_recipients(bcc) if bcc else ""

        message = MIMEMultipart()
        message['To'] = to_str
        message['Cc'] = cc_str
        message['Bcc'] = bcc_str
        message['Subject'] = subject

        mime_type = 'html' if is_html else 'plain'
        message.attach(MIMEText(body, mime_type))

        if attachments:
            for filepath in attachments:
                try:
                    with open(filepath, "rb") as attachment_file:
                        part = MIMEBase("application", "octet-stream")
                        part.set_payload(attachment_file.read())
                        encoders.encode_base64(part)
                        part['Content-Disposition'] = f"attachment; filename={os.path.basename(filepath)}"
                        message.attach(part)
                except Exception as e:
                    print(f"Failed to attach file {filepath}: {e}")

        raw = base64.urlsafe_b64encode(message.as_bytes()).decode()

        try:
            sent_msg = self.service.users().messages().send(userId='me', body={'raw': raw}).execute()
            print(f"Email sent successfully! Message ID: {sent_msg['id']}")
            return sent_msg
        except Exception as e:
            print(f"Error in send_email: {e}")
            return None

    def read_latest_emails(self, max_results=5):
        """Reads the latest emails from the inbox with robust parsing."""
        try:
            results = self.service.users().messages().list(userId='me', maxResults=max_results).execute()
            messages = results.get('messages', [])

            emails = []
            for msg in messages:
                try:
                    txt = self.service.users().messages().get(userId='me', id=msg['id']).execute()
                    payload = txt['payload']
                    headers = payload['headers']

                    subject = next((h['value'] for h in headers if h['name'] == 'Subject'), "No Subject")
                    sender = next((h['value'] for h in headers if h['name'] == 'From'), "Unknown Sender")

                    body = ""
                    if 'parts' in payload:
                        for part in payload['parts']:
                            if part['mimeType'] == 'text/plain':
                                data = part['body'].get('data', '')
                                if data:
                                    body = base64.urlsafe_b64decode(data).decode()
                    elif 'body' in payload:
                        data = payload['body'].get('data', '')
                        if data:
                            body = base64.urlsafe_b64decode(data).decode()

                    emails.append({'id': msg['id'], 'from': sender, 'subject': subject, 'body': body})
                except Exception as inner_e:
                    print(f"Error reading individual message {msg['id']}: {inner_e}")
                    continue

            return emails
        except Exception as e:
            print(f"Error in read_latest_emails: {e}")
            return []

    def summarize_email(self, email_content):
        """Summarizes email content (Placeholder for LLM integration)."""
        if not email_content:
            return "No content to summarize."
        return f"[Summary Placeholder]: The email is {len(email_content)} characters long."

    def mark_as_read(self, message_id):
        """Marks a specific email as read."""
        try:
            self.service.users().messages().batchModify(
                userId='me',
                body={'ids': [message_id], 'removeLabelIds': ['UNREAD']}
            ).execute()
            print(f"Message {message_id} marked as read.")
        except Exception as e:
            print(f"Error in mark_as_read: {e}")

    def search_emails(self, query):
        """Search for emails based on a query."""
        try:
            results = self.service.users().messages().list(userId='me', q=query).execute()
            return results.get('messages', [])
        except Exception as e:
            print(f"Error in search_emails: {e}")
            return []

if __name__ == "__main__":
    # Professional testing block
    agent = GmailAgent()
    # Example: send_email(to=["a@b.com"], subject="Test", body="Hello", is_html=True)
    pass
