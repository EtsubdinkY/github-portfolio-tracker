import sqlite3

DATABASE = "github_tracker.db"


def get_db_connection():
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    conn = get_db_connection()

    with open("schema.sql", "r") as file:
        conn.executescript(file.read())

    conn.commit()
    conn.close()

    migrate_db()


def migrate_db():
    conn = get_db_connection()

    repo_columns = [
        row["name"]
        for row in conn.execute("PRAGMA table_info(repositories)").fetchall()
    ]

    issue_columns = [
        row["name"]
        for row in conn.execute("PRAGMA table_info(saved_issues)").fetchall()
    ]

    if "user_id" not in repo_columns:
        conn.execute("ALTER TABLE repositories ADD COLUMN user_id INTEGER")

    if "user_id" not in issue_columns:
        conn.execute("ALTER TABLE saved_issues ADD COLUMN user_id INTEGER")

    conn.commit()
    conn.close()