# GitHub Portfolio Tracker

A multi-user Flask web application for tracking GitHub repositories, monitoring issues, and organizing open-source contribution plans.

## Features

- GitHub OAuth authentication
- Per-user repository tracking
- Open GitHub issue retrieval
- Save issues with notes, priority, and target dates
- Issue status tracking
- Dashboard analytics
- Multi-user SQLite data isolation
- Automatic database initialization

---

## Requirements

- Python 3.10+
- Git
- GitHub account

---

## Setup

### 1. Clone the repository

```bash
git clone https://github.com/EtsubdinkY/github-portfolio-tracker.git
cd github-portfolio-tracker
```

---

### 2. Create virtual environment

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

### 4. Create environment file

Create a file named:

```bash
.env
```

Add the provided GitHub OAuth credentials:

```env
GITHUB_CLIENT_ID=Ov23liygDInVoFiZbbEF
GITHUB_CLIENT_SECRET=77737f52dfbaecf60612a6b2c8c765b765b4e396
```

---

## Run the Application

Start the Flask application:

```bash
python3 app.py
```

Open in browser:

```text
http://127.0.0.1:5001
```

Then:

- Click **Login with GitHub**
- Sign in using your GitHub account
- Start tracking repositories and issues

---

## Project Structure

```text
github-portfolio-tracker/
│
├── app.py
├── database.py
├── schema.sql
├── config.py
├── requirements.txt
│
├── repositories/
│   ├── repo_repository.py
│   ├── issue_repository.py
│   └── user_repository.py
│
├── services/
│   └── github_service.py
│
├── templates/
├── static/
```

---

## Database Behavior

- Database tables are automatically created on first run
- Existing schema updates are handled automatically
- Each user only sees their own repositories and saved issues
- SQLite database remains local to each machine

---

## Troubleshooting

### GitHub login fails

Check:

- `.env` file exists
- Credentials were copied correctly
- Application is running on:

```text
http://127.0.0.1:5001
```

---

### Repositories not appearing

Try:

- Logging out and back in
- Confirming GitHub login completed successfully

---

### Port already in use

Restart the Flask application:

```bash
python3 app.py
```

---

## Technologies Used

- Python
- Flask
- SQLite
- GitHub REST API
- GitHub OAuth 2.0
- HTML/CSS

echo "CI test" >> README.md