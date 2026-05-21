from mail.gmail import authenticate_gmail, get_unread_emails
from mail.classify import classify_email
from mail.importance import calculate_priority

def main():

    # 1. Gmail 연결
    service = authenticate_gmail()

    # 2. 메일 가져오기
    emails = get_unread_emails(service)

    processed = []

    for email in emails:

        # 3. 분류
        category = classify_email(email)
        email["category"] = category

        # 4. priority 계산 (이미 완성된 엔진 사용)
        result = calculate_priority(email)

        email["priority"] = result["priority"]
        email["deadline"] = result["deadline"]

        processed.append(email)

    # 5. priority 기준 정렬
    processed.sort(
        key=lambda x: x["priority"],
        reverse=True
    )

    # 6. 출력 (핵심만)
    print("\n" + "=" * 80)
    print("📬 PRIORITY EMAIL DASHBOARD")
    print("=" * 80)

    for email in processed:

        # 중요도 낮은 건 숨김
        if email["priority"] < 3:
            continue

        print("\n" + "-" * 80)
        print(f"📌 CATEGORY : {email['category']}")
        print(f"🔥 PRIORITY : {email['priority']}")
        print(f"📅 DEADLINE : {email['deadline']}")
        print(f"📨 FROM     : {email['sender']}")
        print(f"📄 SUBJECT  : {email['subject']}")
        print("\nCONTENT:")
        print(email["content"][:300])

    print("\n" + "=" * 80)


if __name__ == "__main__":
    main()