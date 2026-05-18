from database import get_db_connection

def save_repository(repo):
    conn = get_db_connection()

    conn.execute("""
        INSERT OR IGNORE INTO repositories (
            owner, name, full_name, description,
            language, stars, forks, open_issues,
            github_url, last_updated
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        repo["owner"],
        repo["name"],
        repo["full_name"],
        repo["description"],
        repo["language"],
        repo["stars"],
        repo["forks"],
        repo["open_issues"],
        repo["github_url"],
        repo["last_updated"]
    ))

    conn.commit()
    conn.close()

def get_dashboard_stats():
    conn = get_db_connection()

    total_repos = conn.execute("""
        SELECT COUNT(*) AS count FROM repositories
    """).fetchone()["count"]

    total_stars = conn.execute("""
        SELECT COALESCE(SUM(stars), 0) AS total FROM repositories
    """).fetchone()["total"]

    total_saved_issues = conn.execute("""
        SELECT COUNT(*) AS count FROM saved_issues
    """).fetchone()["count"]

    languages = conn.execute("""
        SELECT 
            COALESCE(language, 'Not detected') AS language,
            COUNT(*) AS count
        FROM repositories
        GROUP BY COALESCE(language, 'Not detected')
        ORDER BY count DESC
    """).fetchall()

    conn.close()

    return {
        "total_repos": total_repos,
        "total_stars": total_stars,
        "total_saved_issues": total_saved_issues,
        "languages": languages
    }

def delete_repository(repo_id):
    conn = get_db_connection()

    # Delete saved issues linked to this repo first
    conn.execute("""
        DELETE FROM saved_issues
        WHERE repo_id = ?
    """, (repo_id,))

    # Then delete the repo
    conn.execute("""
        DELETE FROM repositories
        WHERE id = ?
    """, (repo_id,))

    conn.commit()
    conn.close()