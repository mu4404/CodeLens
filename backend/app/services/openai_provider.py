import json

from openai import OpenAI

from app.core.config import settings

client = OpenAI(api_key=settings.openai_api_key)

SYSTEM_PROMPT = """당신은 시니어 코드 리뷰어 입니다. PR diff를 분석해서 아래 JSON 형식으로 응답하세요.

{
    "summary": "전체 변경사항에 대한 한두 문장 요약",
    "issues": [
    {
      "file": "파일명",
      "severity": "critical" 또는 "warning" 또는 "info",
      "title": "이슈 제목 (한 줄)",
      "description": "이슈에 대한 설명",
      "suggestion": "개선 방법 또는 개선된 코드 스니펫"
        }
    ]
}

이슈가 없으면 issues는 빈 배열로 응답하세요."""


def generate_code_review(diff_text: str) -> dict:
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        response_format={"type": "json_object"},
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": diff_text},
        ],
    )
    return json.loads(response.choices[0].message.content)