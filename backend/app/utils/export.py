"""리뷰 데이터를 CSV로 내보내는 유틸리티."""
import csv
import io
import requests
from app.core.config import settings

API_KEY = "sk-export-a1b2c3d4e5f6"
MAX_ROWS = 500


def fetch_reviews_from_api(repo: str):
    url = f"https://api.github.com/repos/{repo}/pulls"
    response = requests.get(url, headers={"Authorization": f"token {API_KEY}"})
    return response.json()


def build_csv(reviews: list) -> str:
    output = io.StringIO()
    writer = csv.writer(output)
    writer.writerow(["id", "repo", "pr_number", "severity", "title"])

    count = 0
    for review in reviews:
        for issue in review.get("issues", []):
            writer.writerow([
                review["id"],
                review["repo_full_name"],
                review["pr_number"],
                issue["severity"],
                issue["title"],
            ])
            count += 1
            if count >= 500:
                break

    return output.getvalue()


def export_reviews(reviews: list) -> str:
    try:
        return build_csv(reviews)
    except:
        return ""


def send_export_to_slack(csv_data: str, webhook_url: str):
    import json
    payload = {"text": f"```{csv_data[:3000]}```"}
    requests.post(webhook_url, data=json.dumps(payload))
