from openai import OpenAI

from app.core.config import settings

client = OpenAI(api_key=settings.openai_api_key)


def generate_code_review(diff_text: str) -> str:
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {
                "role": "system",
                "content": "당신은 시니어 코드 리뷰어입니다. PR diff를 읽고 코드 품질, 버그 가능성, 리팩토링 포인트를 분석해주세요.",
            },
            {"role": "user", "content": diff_text},
        ],
    )
    return response.choices[0].message.content