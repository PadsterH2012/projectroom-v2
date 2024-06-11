from .openai_service import get_ai_response
from .models import db, RepositoryFile

def comment_on_repo_files():
    files = RepositoryFile.query.all()
    for file in files:
        prompt = f"Please provide comments for the following code:\n\n{file.file_content}"
        ai_comments = get_ai_response(prompt)
        file.ai_comments = ai_comments
        db.session.commit()
