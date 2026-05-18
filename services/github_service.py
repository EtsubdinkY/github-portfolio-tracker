import requests

def get_repository(owner, repo):
    url = f"https://api.github.com/repos/{owner}/{repo}"

    response = requests.get(url)

    if response.status_code != 200:
        return None

    data = response.json()

    return {
        "owner": data["owner"]["login"],
        "name": data["name"],
        "full_name": data["full_name"],
        "description": data.get("description"),
        "language": data.get("language"),
        "stars": data.get("stargazers_count", 0),
        "forks": data.get("forks_count", 0),
        "open_issues": data.get("open_issues_count", 0),
        "github_url": data.get("html_url"),
        "last_updated": data.get("updated_at")
    }
def get_open_issues(owner, repo):
    url = f"https://api.github.com/repos/{owner}/{repo}/issues"

    response = requests.get(url)

    if response.status_code != 200:
        return []

    issues_data = response.json()

    issues = []

    for issue in issues_data:
        if "pull_request" in issue:
            print("This is a pull request, not an issue:")
            print(issue)
            continue

        labels = []
        for label in issue.get("labels", []):
            labels.append(label.get("name"))

        issues.append({
            "issue_number": issue.get("number"),
            "title": issue.get("title"),
            "author": issue.get("user", {}).get("login"),
            "labels": ", ".join(labels),
            "issue_url": issue.get("html_url")
        })

    return issues