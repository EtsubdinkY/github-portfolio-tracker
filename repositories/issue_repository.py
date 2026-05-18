from database import get_db_connection


def save_issue(repo_id, issue):
    conn = get_db_connection()

    conn.execute("""
        INSERT INTO saved_issues (
            repo_id,
            issue_number,
            title,
            issue_url,
            labels,
            note,
            status,
            priority,
            target_date
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        repo_id,
        issue["issue_number"],
        issue["title"],
        issue["issue_url"],
        issue["labels"],
        issue["note"],
        "Planned",
        issue["priority"],
        issue["target_date"]
    ))

    conn.commit()
    conn.close()


def get_saved_issues():
    conn = get_db_connection()

    issues = conn.execute("""
        SELECT saved_issues.*, repositories.full_name
        FROM saved_issues
        JOIN repositories
        ON saved_issues.repo_id = repositories.id
    """).fetchall()

    conn.close()
    return issues

def update_issue_status(issue_id, status):
    conn = get_db_connection()

    conn.execute("""
        UPDATE saved_issues
        SET status = ?
        WHERE id = ?
    """, (status, issue_id))

    conn.commit()
    conn.close()

def delete_saved_issue(issue_id):
    conn = get_db_connection()

    conn.execute("""
        DELETE FROM saved_issues
        WHERE id = ?
    """, (issue_id,))

    conn.commit()
    conn.close()