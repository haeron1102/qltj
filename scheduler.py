from dotenv import load_dotenv
load_dotenv()

import requests
import schedule
import time
from datetime import datetime, timedelta
import json
import os

from mail.return_mail import return_mail


BOT_TOKEN = os.getenv("BOT_TOKEN")
CHAT_ID = os.getenv("CHAT_ID")

with open(
    "frontend/events.json",
    "r",
    encoding="utf-8"
) as file:
    events = json.load(file)

def send_telegram_message(message):
    url = (
        f"https://api.telegram.org/bot"
        f"{BOT_TOKEN}/sendMessage"
    )

    requests.post(
        url,
        json={
            "chat_id": CHAT_ID,
            "text": message,
        },
    )

def send_mail_summary():

    emails = return_mail()

    if not emails:
        return

    message = "📬 오늘의 중요 메일 요약\n"

    for email in emails:

        if email["priority"] < 3:
            continue

        message += f"""

📌 {email['subject']}

🔥 Priority:
{email['priority']}

🧠 Summary:
{email['summary']}
"""

    send_telegram_message(message)

def check_tomorrow_events():
    tomorrow = (
        datetime.now() + timedelta(days=1)
    ).strftime("%Y-%m-%d")

    tomorrow_events = []

    for event in events:
        if event["date"] == tomorrow:
            tomorrow_events.append(
                f"• {event['title']}"
            )

    if tomorrow_events:
        message = (
            "📌 내일 일정\n\n"
            + "\n".join(tomorrow_events)
        )

        send_telegram_message(message)

        print("메시지 전송 완료")
    else:
        print("내일 일정 없음")

def check_today_events():
    today = (
        datetime.now()
    ).strftime("%Y-%m-%d")

    today_events = []

    for event in events:
        if event["date"] == today:
            today_events.append(
                f"• {event['title']}"
            )

    if today_events:
        message = (
            "today's events\n\n"
            + "\n".join(today_events)
        )

        send_telegram_message(message)

        print("done")
    else:
        print("there is no event")


schedule.every().day.at("21:00").do(
    check_tomorrow_events
)

schedule.every().day.at("08:00").do(
    check_today_events
)

schedule.every().day.at("08:00").do(
    send_mail_summary
)


while True:
    schedule.run_pending()
    time.sleep(1)