import re


ACADEMIC_KEYWORDS = [
    "assignment",
    "exam",
    "quiz",
    "lecture",
    "course",
    "submission",
    "deadline",
    "professor",
    "homework",
]

PROMOTION_KEYWORDS = [
    "sale",
    "discount",
    "offer",
    "promotion",
    "unsubscribe",
    "coupon",
]

NOTIFICATION_KEYWORDS = [
    "github",
    "notification",
    "alert",
    "security",
    "login",
]

SOCIAL_KEYWORDS = [
    "discord",
    "instagram",
    "facebook",
    "twitter",
]


IMPORTANT_SENDERS = [
    "kaist",
    "university",
    "professor",
]


def classify_email(email_document):

    subject = email_document.get(
        "subject",
        ""
    ).lower()

    content = email_document.get(
        "content",
        ""
    ).lower()

    sender = email_document.get(
        "sender",
        ""
    ).lower()

    text = f"{subject} {content}"

    # academic
    if contains_keywords(
        text,
        ACADEMIC_KEYWORDS
    ):
        return "academic"

    # promotion
    if contains_keywords(
        text,
        PROMOTION_KEYWORDS
    ):
        return "promotion"

    # notification
    if contains_keywords(
        text,
        NOTIFICATION_KEYWORDS
    ):
        return "notification"

    # social
    if contains_keywords(
        text,
        SOCIAL_KEYWORDS
    ):
        return "social"

    # important sender
    if contains_keywords(
        sender,
        IMPORTANT_SENDERS
    ):
        return "important"

    return "unknown"


def contains_keywords(text, keywords):

    for keyword in keywords:

        if keyword in text:
            return True

    return False