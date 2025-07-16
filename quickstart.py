# Portions of this software are derived from Gmail API Python quickstart
# Copyright 2018 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
import base64
import os.path
import re

from bs4 import BeautifulSoup
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

# If modifying these scopes, delete the file token.json.
SCOPES = ["https://www.googleapis.com/auth/gmail.readonly"]


def remove_hyperlinks(text):
  # Remove URLs starting with http/https
  text = re.sub(r'http\S+', '', text)
  # Remove URLs containing '.com'
  text = re.sub(r'\S+\.com\S*', '', text)
  text = re.sub(r'\S+\.net\S*', '', text)
  text = re.sub(r'\S+\.org\S*', '', text)
  return text

def get_emails_id(service):
  query = "label:work"
  response = service.users().messages().list(userId='me', q=query, ).execute()
  messages = []

  if 'messages' in response:
    messages.extend(response['messages'])

  while 'nextPageToken' in response:
    page_token = response['nextPageToken']
    response = service.users().messages().list(userId='me', q=query, pageToken=page_token).execute()

    if 'messages' in response:
      messages.extend(response['messages'])

  return messages


def extract_email_data(service, message_id):
  msg = service.users().messages().get(userId='me', id=message_id, format='full').execute()
  payload = msg['payload']
  headers = payload['headers']
  email_data = {'id': message_id}

  for header in headers:
    name = header['name']
    value = header['value']
    if name == 'From':
      email_data['from'] = value
    if name == 'Date':
      email_data['date'] = value
    if name == 'Subject':
      email_data['subject'] = value

  if 'parts' in payload:
    parts = payload['parts']
    data = None
    while data is None and parts is not None:
      for part in parts:
        if part['mimeType'] == 'text/plain':
          data = part['body']['data']
        elif part['mimeType'] == 'text/html':
          data = part['body']['data']
        else:
          try:
            parts = part['parts']
          except:
            pass

    text = base64.urlsafe_b64decode(data.encode('UTF-8'))
    soup = BeautifulSoup(text, 'html.parser')
    clean_text = soup.get_text()
    # clean_text = remove_hyperlinks(clean_text)
    email_data['text'] = clean_text

  return email_data


def main():
  """Shows basic usage of the Gmail API.
  Lists the user's Gmail labels.
  """
  creds = None
  # The file token.json stores the user's access and refresh tokens, and is
  # created automatically when the authorization flow completes for the first
  # time.
  if os.path.exists("token.json"):
    creds = Credentials.from_authorized_user_file("token.json", SCOPES)
  # If there are no (valid) credentials available, let the user log in.
  if not creds or not creds.valid:
    if creds and creds.expired and creds.refresh_token:
      creds.refresh(Request())
    else:
      flow = InstalledAppFlow.from_client_secrets_file(
          "credentials.json", SCOPES
      )
      creds = flow.run_local_server(port=0)
    # Save the credentials for the next run
    with open("token.json", "w") as token:
      token.write(creds.to_json())

  try:
    # Call the Gmail API
    service = build("gmail", "v1", credentials=creds)

  except HttpError as error:
    # TODO(developer) - Handle errors from gmail API.
    print(f"An error occurred: {error}")

  messages = get_emails_id(service)

  print("Found", len(messages), "emails\n")

  with open('work_emails.txt', 'w', encoding='utf8') as f:
    for message in messages:
      email_data = extract_email_data(service, message['id'])

      if 'text' in email_data:
        f.write('%s\n' % ' - '.join((email_data['from'], email_data['subject'], email_data['text'].replace('\n', ''))).encode('utf-8'))
      else:
        f.write('%s\n' % ' - '.join((email_data['from'], email_data['subject'])))


if __name__ == "__main__":
  main()