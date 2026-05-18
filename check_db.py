from database import get_db_connection

conn = get_db_connection()
repos = conn.execute("SELECT * FROM repositories").fetchall()

for repo in repos:
    print(dict(repo))

conn.close()