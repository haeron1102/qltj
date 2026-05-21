from __future__ import print_function

import sys
sys.stdout.reconfigure(encoding='utf-8')

import base64
import os.path
import re

from bs4 import BeautifulSoup

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build


SCOPES = ["https://www.googleapis.com/auth/gmail.readonly"]


def authenticate_gmail():
    creds = None

    if os.path.exists("token.json"):
        creds = Credentials.from_authorized_user_file(
            "token.json",
            SCOPES
        )

    if not creds or not creds.valid:

        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())

        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                "credentials.json",
                SCOPES
            )

            creds = flow.run_local_server(port=0)

        with open("token.json", "w") as token:
            token.write(creds.to_json())

    return build("gmail", "v1", credentials=creds)


def get_unread_emails(service, max_results=10):

    results = service.users().messages().list(
        userId="me",
        q="is:unread category:primary",
        maxResults=max_results
    ).execute()

    messages = results.get("messages", [])

    if not messages:
        print("No unread messages found.")
        return []

    email_list = []

    for msg in messages:

        try:
            msg_data = service.users().messages().get(
                userId="me",
                id=msg["id"],
                format="full"
            ).execute()

            headers = msg_data["payload"]["headers"]

            subject = ""
            sender = ""
            date = ""

            for header in headers:

                if header["name"] == "Subject":
                    subject = header["value"]

                elif header["name"] == "From":
                    sender = header["value"]

                elif header["name"] == "Date":
                    date = header["value"]

            body = extract_body(msg_data["payload"])

            body = clean_text(body)

            body = remove_urls(body)

            body = body[:3000]

            email_document = {
                "source": "gmail",
                "id": msg["id"],
                "sender": sender,
                "subject": subject,
                "content": body,
                "date": date
            }

            email_list.append(email_document)

        except Exception as e:
            print(f"ERROR processing email: {e}")

    return email_list


def extract_body(payload):

    # multipart email
    if "parts" in payload:

        for part in payload["parts"]:

            mime_type = part.get("mimeType", "")

            # plain text 우선
            if mime_type == "text/plain":

                data = part.get("body", {}).get("data")

                if data:
                    return decode_base64(data)

            # html fallback
            elif mime_type == "text/html":

                data = part.get("body", {}).get("data")

                if data:
                    return decode_base64(data)

            # nested multipart recursion
            result = extract_body(part)

            if result:
                return result

    else:
        data = payload.get("body", {}).get("data")

        if data:
            return decode_base64(data)

    return ""


def decode_base64(data):

    try:
        decoded_bytes = base64.urlsafe_b64decode(data)

        return decoded_bytes.decode(
            "utf-8",
            errors="ignore"
        )

    except Exception:
        return ""


def clean_text(text):

    soup = BeautifulSoup(
        text,
        "html.parser"
    )

    cleaned = soup.get_text(
        separator=" ",
        strip=True
    )

    return cleaned


def remove_urls(text):

    return re.sub(
        r"http\S+|www\S+",
        "",
        text
    )


def main():

    service = authenticate_gmail()

    emails = get_unread_emails(service)

    for idx, email in enumerate(emails, 1):

        print("=" * 60)

        print(f"EMAIL #{idx}")

        print(f"FROM: {email['sender']}")

        print(f"SUBJECT: {email['subject']}")

        print(f"DATE: {email['date']}")

        print(f"BODY:\n{email['content'][:500]}")

        print("=" * 60)


if __name__ == "__main__":
    main()