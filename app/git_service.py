import git
import os
import shutil
from .models import db, RepositoryFile

def clone_repo(repo_url, clone_dir):
    if os.path.exists(clone_dir):
        shutil.rmtree(clone_dir)
    git.Repo.clone_from(repo_url, clone_dir)

def ingest_repo_to_db(clone_dir):
    for root, _, files in os.walk(clone_dir):
        for file in files:
            file_path = os.path.join(root, file)
            with open(file_path, 'r') as f:
                content = f.read()
            repo_file = RepositoryFile(
                file_path=file_path,
                file_content=content
            )
            db.session.add(repo_file)
    db.session.commit()
