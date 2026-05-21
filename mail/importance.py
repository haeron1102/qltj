from datetime import datetime
from dateutil import parser
import re


def extract_deadline(text):

    patterns = [
        r"\d{4}-\d{2}-\d{2}",
        r"\d{4}/\d{2}/\d{2}"
    ]

    for pattern in patterns:

        matches = re.findall(pattern, text)

        for m in matches:

            try:
                return parser.parse(m)
            except:
                continue

    return None


def calculate_priority(email):

    text = email.get("content", "")

    deadline = extract_deadline(text)

    now = datetime.now()

    # 기본 점수
    score = 0

    # deadline 없으면 low priority
    if not deadline:
        return {
            "priority": 0,
            "deadline": None
        }

    delta = deadline - now
    hours_left = delta.total_seconds() / 3600

    # 이미 지난 경우
    if hours_left < 0:
        return {
            "priority": 0,
            "deadline": deadline
        }

    # 48시간 기준 핵심 로직
    if hours_left <= 48:
        score = 5

    elif hours_left <= 72:
        score = 3

    else:
        score = 1

    return {
        "priority": score,
        "deadline": deadline
    }