import asyncio

import httpx

from app.core.celery_app import celery_app
from app.services.llm_provider import generate_code_review
from app.core.config import settings
from app.core.database import async_session
from app.models import Review, ReviewIssue


async def _save_review(repo_full_name: str, pr_number: int, title: str, author: str, review_data: dict) -> None:
    async with async_session() as session:
        review = Review(
            repo_full_name=repo_full_name,
            pr_number=pr_number,
            title=title,
            author=author,
            summary=review_data["summary"],
        )
        session.add(review)
        await session.flush()

        for issue in review_data["issues"]:
            session.add(ReviewIssue(review_id=review.id, **issue))

        await session.commit()


def _format_comment(review_data: dict) -> str:
    severity_emoji = {"critical": "🔴", "warning": "🟡", "info": "🔵"}
    lines = ["## 🤖 CodeLens 코드 리뷰", "", review_data["summary"], ""]

    for issue in review_data["issues"]:
        emoji = severity_emoji.get(issue["severity"], "")
        lines.append(f"### {emoji} `{issue['file']}` — {issue['title']}")
        lines.append(issue["description"])
        lines.append(f"\n**제안:** {issue['suggestion']}\n")

    return "\n".join(lines)


@celery_app.task
def process_pull_request_event(repo_full_name: str, pr_number: int, action: str, title: str, author: str):
    diff_url = f"https://api.github.com/repos/{repo_full_name}/pulls/{pr_number}"
    response = httpx.get(diff_url, headers={"Accept": "application/vnd.github.v3.diff"})
    diff_text = response.text

    review_data = generate_code_review(diff_text)

    asyncio.run(_save_review(repo_full_name, pr_number, title, author, review_data))

    comment_url = f"https://api.github.com/repos/{repo_full_name}/issues/{pr_number}/comments"
    httpx.post(
        comment_url,
        headers={
            "Authorization": f"Bearer {settings.github_bot_token}",
            "Accept": "application/vnd.github+json",
        },
        json={"body": _format_comment(review_data)},
    )