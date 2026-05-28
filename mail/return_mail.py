from mail.gmail import (
    authenticate_gmail,
    get_unread_emails
)

from mail.classify import classify_email
from mail.importance import calculate_priority
from mail.summarize import summarize_email


def return_mail():

    service = authenticate_gmail()

    emails = get_unread_emails(service)

    processed = []

    for email in emails:

        category = classify_email(email)
        email["category"] = category

        result = calculate_priority(email)

        email["priority"] = result["priority"]
        email["deadline"] = result["deadline"]

        summary = summarize_email(email)
        email["summary"] = summary

        processed.append(email)

    processed.sort(
        key=lambda x: x["priority"],
        reverse=True
    )

    return processed