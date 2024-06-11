from . import db

class Conversation(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_message = db.Column(db.Text, nullable=False)
    ai_response = db.Column(db.Text, nullable=False)

class RepositoryFile(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    file_path = db.Column(db.String(256), nullable=False)
    file_content = db.Column(db.Text, nullable=False)
    ai_comments = db.Column(db.Text)
