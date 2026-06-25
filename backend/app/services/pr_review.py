from app.core.celery_app import celery_app


@celery_app.task
def process_pull_request_event(repo_full_name: str, pr_number: int, action: str, title: str):
    print(f"[Celery] {repo_full_name} PR #{pr_number} {action} - {title}")