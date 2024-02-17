import smtplib, ssl, dotenv, os

from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.message import EmailMessage
from email.policy import Policy

import os.path
import base64


from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

import string
alph_b36 = string.digits + string.ascii_uppercase


dotenv.load_dotenv()

SENDER = os.environ["GMAIL_SENDER"]
PASSWORD = os.environ["PASSWORD"]
YAHOO_SENDER = os.environ.get("YAHOO_SENDER")
YAHOO_PASSWORD = os.environ["YAHOO_PASSWORD"]


def sendmail(SUBJECT, MESSAGE, TO, SERVER=("smtp.mail.yahoo.com", 465)):
    print("starting sending mail")
    msg = MIMEMultipart()
    msg["Subject"] = SUBJECT
    msg["From"] = YAHOO_SENDER
    msg["To"] = TO
    msg.attach(MIMEText(MESSAGE, "html"))
    txt = msg.as_string()
    
    ssl_context = ssl.create_default_context()
    print("starting server")
    with smtplib.SMTP() as server:
        server.connect(SERVER[0], SERVER[1])
        server.starttls()
        print(YAHOO_SENDER, YAHOO_PASSWORD)
        server.login(user=YAHOO_SENDER, password=YAHOO_PASSWORD)
        print("sending mail")
        errs = server.sendmail(YAHOO_SENDER, [TO], txt)

    if errs:
        print(errs)
    return errs



# If modifying these scopes, delete the file token.json.
SCOPES = ["https://www.googleapis.com/auth/gmail"]


def gmail_sendmail(SUBJECT, MESSAGE, TO):
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
    message = EmailMessage()

    message.set_content(MESSAGE)

    message["To"] = TO
    message["From"] = os.environ.get("GMAIL_SENDER")
    message["Subject"] = SUBJECT

    # encoded message
    encoded_message = base64.urlsafe_b64encode(message.as_bytes()).decode()

    create_message = {"raw": encoded_message}
    # pylint: disable=E1101
    send_message = (
        service.users()
        .messages()
        .send(userId="me", body=create_message)
        .execute()
    )
    print(f'Message Id: {send_message["id"]}')
    send_message.send()
  except HttpError as error:
    print(f"An error occurred: {error}")
    send_message = None
  return send_message

def base36encode(number):
    if not isinstance(number, int):
        raise ValueError(
            f"La fonction 'encode_base36' n'accepte que des paramètres de type 'int' et non de type '{type(number)}'"
        )
    
    base36 = ""
    sign = ""
    
    if number < 0:
        sign = "-"
        number = -number
    
    if 0 <= number < len(alph_b36):
        return sign + alph_b36[number]
    
    while number != 0:
        number, i = divmod(number, len(alph_b36))
        base36 = alph_b36[i] + base36
    
    return sign + base36

def base36decode(base36):
    return int(base36, base=36)