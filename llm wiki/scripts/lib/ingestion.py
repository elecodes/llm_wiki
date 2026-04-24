import os.path
import base64
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build

# If modifying these scopes, delete the file token.json.
SCOPES = ['https://www.googleapis.com/auth/gmail.modify']

class GmailIngestor:
    def __init__(self, credentials_path='credentials.json', token_path='token.json'):
        self.creds = None
        # Adjust paths to project root if needed
        self.credentials_path = credentials_path
        self.token_path = token_path
        
        if os.path.exists(self.token_path):
            self.creds = Credentials.from_authorized_user_file(self.token_path, SCOPES)
            
        if not self.creds or not self.creds.valid:
            if self.creds and self.creds.expired and self.creds.refresh_token:
                self.creds.refresh(Request())
            else:
                if not os.path.exists(self.credentials_path):
                    raise FileNotFoundError(f"Gmail credentials not found at {self.credentials_path}")
                flow = InstalledAppFlow.from_client_secrets_file(self.credentials_path, SCOPES)
                self.creds = flow.run_local_server(port=0)
            with open(self.token_path, 'w') as token:
                token.write(self.creds.to_json())
                
        self.service = build('gmail', 'v1', credentials=self.creds)

    def list_messages(self, query='', max_results=10):
        """List messages matching a query (e.g. label:KNOWLEDGE)."""
        results = self.service.users().messages().list(userId='me', q=query, maxResults=max_results).execute()
        return results.get('messages', [])

    def get_message_content(self, msg_id):
        """Fetches message content and extracts subject, date, and body."""
        message = self.service.users().messages().get(userId='me', id=msg_id, format='full').execute()
        
        payload = message.get('payload', {})
        headers = payload.get('headers', [])
        
        subject = next((h['value'] for h in headers if h['name'].lower() == 'subject'), 'No Subject')
        date = next((h['value'] for h in headers if h['name'].lower() == 'date'), 'No Date')
        
        body = ""
        if 'parts' in payload:
            for part in payload['parts']:
                if part['mimeType'] == 'text/plain' or part['mimeType'] == 'text/html':
                    data = part['body'].get('data')
                    if data:
                        body += base64.urlsafe_b64decode(data).decode()
        else:
            data = payload.get('body', {}).get('data')
            if data:
                body = base64.urlsafe_b64decode(data).decode()
                
        return {
            'id': msg_id,
            'subject': subject,
            'date': date,
            'body': body,
            'snippet': message.get('snippet', '')
        }

    def get_label_id(self, label_name):
        """Finds the ID of a label by its name."""
        results = self.service.users().labels().list(userId='me').execute()
        labels = results.get('labels', [])
        for label in labels:
            if label['name'].lower() == label_name.lower():
                return label['id']
        return None

    def modify_labels(self, msg_id, add_label_ids=None, remove_label_ids=None):
        """Adds or removes labels from a message."""
        body = {}
        if add_label_ids:
            body['addLabelIds'] = add_label_ids
        if remove_label_ids:
            body['removeLabelIds'] = remove_label_ids
            
        if not body:
            return None
            
        return self.service.users().messages().modify(
            userId='me', id=msg_id, body=body).execute()
