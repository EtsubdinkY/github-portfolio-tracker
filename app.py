import requests
from flask import Flask, render_template, request, redirect, url_for, flash, session

from config import GITHUB_CLIENT_ID, GITHUB_CLIENT_SECRET
from database import init_db, get_db_connection
from services.github_service import get_repository, get_open_issues
from repositories.repo_repository import (
    save_repository,
    get_dashboard_stats,
    delete_repository
)
from repositories.issue_repository import (
    save_issue,
    get_saved_issues,
    update_issue_status,
    delete_saved_issue
)
from repositories.user_repository import get_or_create_user


app = Flask(__name__)
app.secret_key = "dev-secret-key"


@app.route("/")
def home():
    user_id = session.get("user_id")

    if user_id:
        conn = get_db_connection()
        repos = conn.execute(
            "SELECT * FROM repositories WHERE user_id = ?",
            (user_id,)
        ).fetchall()
        conn.close()

        stats = get_dashboard_stats(user_id)
    else:
        repos = []
        stats = {
            "total_repos": 0,
            "total_saved_issues": 0,
            "total_stars": 0,
            "languages": []
        }

    return render_template("dashboard.html", repos=repos, stats=stats)


@app.route("/add", methods=["GET", "POST"])
def add_repo():
    user_id = session.get("user_id")

    if not user_id:
        flash("Please login with GitHub first.")
        return redirect(url_for("login"))

    if request.method == "POST":
        owner = request.form.get("owner")
        repo_name = request.form.get("repo_name")

        repo = get_repository(owner, repo_name)

        if repo:
            save_repository(repo, user_id)
            flash("Repository added successfully!")
            return redirect(url_for("home"))
        else:
            flash("Repository not found.")

    return render_template("add_repo.html")


@app.route("/repo/<int:repo_id>")
def repo_detail(repo_id):
    user_id = session.get("user_id")

    if not user_id:
        flash("Please login with GitHub first.")
        return redirect(url_for("login"))

    conn = get_db_connection()
    repo = conn.execute(
        "SELECT * FROM repositories WHERE id = ? AND user_id = ?",
        (repo_id, user_id)
    ).fetchone()
    conn.close()

    if repo is None:
        return "Repository not found", 404

    issues = get_open_issues(repo["owner"], repo["name"])

    return render_template("repo_detail.html", repo=repo, issues=issues)


@app.route("/save-issue", methods=["POST"])
def save_issue_route():
    user_id = session.get("user_id")

    if not user_id:
        flash("Please login with GitHub first.")
        return redirect(url_for("login"))

    repo_id = request.form.get("repo_id")

    issue = {
        "issue_number": request.form.get("issue_number"),
        "title": request.form.get("title"),
        "issue_url": request.form.get("issue_url"),
        "labels": request.form.get("labels"),
        "note": request.form.get("note"),
        "priority": request.form.get("priority"),
        "target_date": request.form.get("target_date"),
        "user_id": user_id
    }

    save_issue(repo_id, issue)

    return redirect(url_for("repo_detail", repo_id=repo_id))


@app.route("/issues")
def saved_issues():
    user_id = session.get("user_id")

    if not user_id:
        flash("Please login with GitHub first.")
        return redirect(url_for("login"))

    issues = get_saved_issues(user_id)
    return render_template("saved_issues.html", issues=issues)


@app.route("/update-status", methods=["POST"])
def update_status():
    user_id = session.get("user_id")

    if not user_id:
        flash("Please login with GitHub first.")
        return redirect(url_for("login"))

    issue_id = request.form.get("issue_id")
    status = request.form.get("status")

    update_issue_status(issue_id, status, user_id)

    return redirect(url_for("saved_issues"))


@app.route("/delete-issue", methods=["POST"])
def delete_issue():
    user_id = session.get("user_id")

    if not user_id:
        flash("Please login with GitHub first.")
        return redirect(url_for("login"))

    issue_id = request.form.get("issue_id")

    delete_saved_issue(issue_id, user_id)

    return redirect(url_for("saved_issues"))


@app.route("/delete-repo", methods=["POST"])
def delete_repo():
    user_id = session.get("user_id")

    if not user_id:
        flash("Please login with GitHub first.")
        return redirect(url_for("login"))

    repo_id = request.form.get("repo_id")

    delete_repository(repo_id, user_id)

    return redirect(url_for("home"))


@app.route("/login")
def login():
    github_auth_url = (
        "https://github.com/login/oauth/authorize"
        f"?client_id={GITHUB_CLIENT_ID}"
        "&scope=read:user"
    )
    return redirect(github_auth_url)


@app.route("/github/callback")
def github_callback():
    code = request.args.get("code")

    token_response = requests.post(
        "https://github.com/login/oauth/access_token",
        headers={"Accept": "application/json"},
        data={
            "client_id": GITHUB_CLIENT_ID,
            "client_secret": GITHUB_CLIENT_SECRET,
            "code": code
        }
    )

    token_data = token_response.json()
    access_token = token_data.get("access_token")

    if not access_token:
        flash("GitHub login failed.")
        return redirect(url_for("home"))

    user_response = requests.get(
        "https://api.github.com/user",
        headers={
            "Authorization": f"Bearer {access_token}",
            "Accept": "application/json"
        }
    )

    github_user = user_response.json()

    user = get_or_create_user(
        str(github_user.get("id")),
        github_user.get("login"),
        github_user.get("avatar_url")
    )

    session["user_id"] = user["id"]
    session["github_username"] = user["username"]
    session["github_avatar"] = user["avatar_url"]

    return redirect(url_for("home"))


@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("home"))


if __name__ == "__main__":
    init_db()
    app.run(debug=True, port=5001)