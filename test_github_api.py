from services.github_service import get_repository
from repositories.repo_repository import save_repository

repo = get_repository("EtsubdinkY", "github-portfolio-tracker")

if repo:
    save_repository(repo)
    print("Repository saved to database!")
else:
    print("Failed to fetch repository")