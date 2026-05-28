from dotenv import load_dotenv
load_dotenv()

import json
import os
from telegram.ext import (
    ApplicationBuilder,
    MessageHandler,
    filters,
)

BOT_TOKEN = os.getenv("BOT_TOKEN")


async def handle_message(
    update,
    context
):
    text = update.message.text

    # 추가 제목 날짜
    if text.startswith("추가 "):

        try:
            _, title, date = text.split(" ")

            with open(
                "frontend/events.json",
                "r",
                encoding="utf-8"
            ) as file:
                events = json.load(file)

            events.append({
                "title": title,
                "date": date,
            })

            with open(
                "frontend/events.json",
                "w",
                encoding="utf-8"
            ) as file:
                json.dump(
                    events,
                    file,
                    ensure_ascii=False,
                    indent=2
                )

            await update.message.reply_text(
                "✅ 일정 추가 완료"
            )

        except:
            await update.message.reply_text(
                "형식: 추가 제목 날짜"
            )


app = (
    ApplicationBuilder()
    .token(BOT_TOKEN)
    .build()
)

app.add_handler(
    MessageHandler(
        filters.TEXT,
        handle_message
    )
)

print("봇 실행 중...")

app.run_polling()