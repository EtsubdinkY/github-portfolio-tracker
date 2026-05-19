from database import get_db_connection


def get_or_create_user(github_id, username, avatar_url):
    conn = get_db_connection()

    user = conn.execute(
        "SELECT * FROM users WHERE github_id = ?",
        (github_id,)
    ).fetchone()

    if user:
        conn.close()
        return user

    conn.execute("""
        INSERT INTO users (github_id, username, avatar_url)
        VALUES (?, ?, ?)
    """, (github_id, username, avatar_url))

    conn.commit()

    user = conn.execute(
        "SELECT * FROM users WHERE github_id = ?",
        (github_id,)
    ).fetchone()

    conn.close()
    return user