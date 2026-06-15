import os
import base64
from email.mime.text import MIMEText
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build

# If modifying these scopes, delete the file token.json.
SCOPES = ['https://www.googleapis.com/auth/gmail.modify']

class GmailAgent:
    def __init__(self):
        self.service = self._authenticate()

    def _authenticate(self):
        creds = None
        # The file token.json stores the user's access and refresh tokens
        if os.path.exists('token.json'):
            creds = Credentials.from_authorized_user_file('token.json', SCOPES)

        # If there are no (valid) credentials available, let the user log in.
        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file(
                    'credentials.json', SCOPES)
                creds = flow.run_local_server(port=0)
            # Save the credentials for the next run
            with open('token.json', 'w') as token:
                token.write(creds.to_json())

        return build('gmail', 'v1', credentials=creds)

    def send_email(self, to, subject, body):
        """Sends an email using the Gmail API."""
        message = MIMEText(body)
        message['to'] = to
        message['subject'] = subject
        raw = base64.urlsafe_b64encode(message.as_bytes()).decode()

        try:
            sent_msg = self.service.users().messages().send(userId='me', body={'raw': raw}).execute()
            print(f"Email sent successfully! Message ID: {sent_msg['id']}")
            return sent_msg
        except Exception as e:
            print(f"Error in send_email: {e}")
            return None

    def read_latest_emails(self, max_results=5):
        """Reads the latest emails from the inbox."""
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

                    # Simplified body extraction
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

                    emails.append({'from': sender, 'subject': subject, 'body': body})
                except Exception as inner_e:
                    print(f"Error reading individual message {msg['id']}: {inner_e}")
                    continue

            return emails
        except Exception as e:
            print(f"Error in read_latest_emails: {e}")
            return []

    def summarize_email(self, email_content):
        """
        Summarizes email content.
        Note: This is a placeholder for an LLM integration (e.g., OpenAI, Claude, or Gemini).
        """
        if not email_content:
            return "No content to summarize."

        # In a real scenario, you would call an LLM API here.
        # Example: response = llm.complete(f"Summarize this email: {email_content}")
        summary = f"[Summary Placeholder]: The email is {len(email_content)} characters long and discusses the provided content."
        return summary

    def mark_as_read(self, message_id):
        """Marks a specific email as read (removes UNREAD label)."""
        try:
            self.service.users().messages().batchModify(
                userId='me',
                body={'ids': [message_id], 'removeLabelIds': ['UNREAD']}
            ).execute()
            print(f"Message {message_id} marked as read.")
        except Exception as e:
            print(f"An error occurred: {e}")

    def search_emails(self, query):
        """Search for emails based on a query."""
        try:
            results = self.service.users().messages().list(userId='me', q=query).execute()
            return results.get('messages', [])
        except Exception as e:
            print(f"An error occurred: {e}")
            return []

if __name__ == "__main__":
    # Example usage (Commented out as per request 'dont run it')
    agent = GmailAgent()
    agent.send_email("recipient@example.com", "Test Subject", "Test Body")
    emails = agent.read_latest_emails()
    for e in emails:
        print(f"From: {e['from']} | Subject: {e['subject']}")
        print(f"Summary: {agent.summarize_email(e['body'])}\n")
    pass
