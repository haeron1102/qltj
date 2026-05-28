from dotenv import load_dotenv
load_dotenv()

from openai import OpenAI
import os

client = OpenAI(
    api_key=os.getenv("OPENAI_API_KEY")
)


def summarize_email(email):

    response = client.chat.completions.create(
        model="gpt-4.1-mini",

        messages=[
            {
                "role": "system",
                "content": """
너는 메일 비서다.

핵심 내용만 짧게 요약해라.
불필요한 인사말은 제거해라.
"""
            },

            {
                "role": "user",
                "content": f"""
제목:
{email['subject']}

내용:
{email['content']}
"""
            }
        ],

        temperature=0.3
    )

    return (
        response
        .choices[0]
        .message
        .content
    )