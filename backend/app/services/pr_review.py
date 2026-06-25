import httpx

from app.core.celery_app import celery_app
from app.services.llm_provider import generate_code_review
from app.core.config import settings

@celery_app.task
def process_pull_request_event(repo_full_name: str, pr_number: int, action: str, title: str):
    diff_url = f"https://api.github.com/repos/{repo_full_name}/pulls/{pr_number}"
    response = httpx.get(diff_url, headers={"Accept": "application/vnd.github.v3.diff"})
    diff_text = response.text

    review = generate_code_review(diff_text)

    comment_url = f"https://api.github.com/repos/{repo_full_name}/issues/{pr_number}/comments"
    httpx.post(
        comment_url,
        headers={
            "Authorization": f"Bearer {settings.github_bot_token}",
            "Accept": "application/vnd.github+json",
        },
        json={"body": review},
    )