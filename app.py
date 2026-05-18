from flask import Flask, render_template, request, redirect, url_for, flash
from database import init_db, get_db_connection
from services.github_service import get_repository, get_open_issues
from repositories.repo_repository import save_repository, get_dashboard_stats
from repositories.issue_repository import save_issue, get_saved_issues, update_issue_status
from repositories.issue_repository import save_issue, get_saved_issues, update_issue_status, delete_saved_issue
from repositories.repo_repository import save_repository, get_dashboard_stats, delete_repository

app = Flask(__name__)
app.secret_key = "dev-secret-key"


@app.route("/")
def home():
    conn = get_db_connection()
    repos = conn.execute("SELECT * FROM repositories").fetchall()
    conn.close()

    stats = get_dashboard_stats()

    return render_template("dashboard.html", repos=repos, stats=stats)


@app.route("/add", methods=["GET", "POST"])
def add_repo():
    if request.method == "POST":
        owner = request.form.get("owner")
        repo_name = request.form.get("repo_name")

        repo = get_repository(owner, repo_name)

        if repo:
            save_repository(repo)
            flash("Repository added successfully!")
            return redirect(url_for("home"))
        else:
            flash("Repository not found.")

    return render_template("add_repo.html")


@app.route("/repo/<int:repo_id>")
def repo_detail(repo_id):
    conn = get_db_connection()
    repo = conn.execute(
        "SELECT * FROM repositories WHERE id = ?",
        (repo_id,)
    ).fetchone()
    conn.close()

    if repo is None:
        return "Repository not found", 404

    issues = get_open_issues(repo["owner"], repo["name"])

    return render_template("repo_detail.html", repo=repo, issues=issues)


@app.route("/save-issue", methods=["POST"])
def save_issue_route():
    repo_id = request.form.get("repo_id")

    issue = {
        "issue_number": request.form.get("issue_number"),
        "title": request.form.get("title"),
        "issue_url": request.form.get("issue_url"),
        "labels": request.form.get("labels"),
        "note": request.form.get("note"),
        "priority": request.form.get("priority"),
        "target_date": request.form.get("target_date")
    }

    save_issue(repo_id, issue)

    return redirect(url_for("repo_detail", repo_id=repo_id))


@app.route("/issues")
def saved_issues():
    issues = get_saved_issues()
    return render_template("saved_issues.html", issues=issues)


@app.route("/update-status", methods=["POST"])
def update_status():
    issue_id = request.form.get("issue_id")
    status = request.form.get("status")

    update_issue_status(issue_id, status)

    return redirect(url_for("saved_issues"))

@app.route("/delete-issue", methods=["POST"])
def delete_issue():
    issue_id = request.form.get("issue_id")

    delete_saved_issue(issue_id)

    return redirect(url_for("saved_issues"))

@app.route("/delete-repo", methods=["POST"])
def delete_repo():
    repo_id = request.form.get("repo_id")

    delete_repository(repo_id)

    return redirect(url_for("home"))


if __name__ == "__main__":
    init_db()
    app.run(debug=True)