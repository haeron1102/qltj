import imaplib
import email

EMAIL = "dear1005@kaist.ac.kr"
PASSWORD = "gkgusals^^1"

imap = imaplib.IMAP4_SSL(
    "imap.dooray.com",
    993
)

imap.login(EMAIL, PASSWORD)

print("로그인 성공")

imap.select("INBOX")

status, messages = imap.search(
    None,
    "ALL"
)

mail_ids = messages[0].split()

latest_mail_id = mail_ids[-1]

status, msg_data = imap.fetch(
    latest_mail_id,
    "(RFC822)"
)

raw_email = msg_data[0][1]

msg = email.message_from_bytes(
    raw_email
)

print("제목:")
print(msg["subject"])