# GitHub Portfolio Tracker

A Flask web app that helps users track GitHub repositories, monitor issues, and save issues for contribution planning.

## Features

- GitHub OAuth login
- Per-user repository tracking
- Save GitHub issues
- Dashboard analytics
- Multi-user SQLite support

---

## Setup

### 1. Clone the repo

```bash
git clone https://github.com/EtsubdinkY/github-portfolio-tracker.git
cd github-portfolio-tracker
```

---

### 2. Create virtual environment

Mac/Linux:

```bash
python3 -m venv venv
source venv/bin/activate
```

---

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

---

### 4. Create .env file

Create a file named:

```bash
.env
```

Add:

```env
GITHUB_CLIENT_ID=your_client_id
GITHUB_CLIENT_SECRET=your_client_secret
```

---

## GitHub OAuth Setup

Create a GitHub OAuth App:

GitHub → Settings → Developer Settings → OAuth Apps → New OAuth App

Use:

Homepage URL:

```text
http://127.0.0.1:5001
```

Authorization callback URL:

```text
http://127.0.0.1:5001/github/callback
```

---

## Run

```bash
python3 app.py
```

Then open:

```text
http://127.0.0.1:5001
```

Click:

```text
Login with GitHub
```

That’s it.

Database is created automatically on first run.

---

## Notes

- Each user only sees their own repositories and saved issues.
- SQLite database is local to each machine.
- No manual database setup required.