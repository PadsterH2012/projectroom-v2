from flask import Blueprint, request, render_template, jsonify
from .models import db, Conversation
from .openai_service import get_ai_response
from .git_service import clone_repo, ingest_repo_to_db
from .ai_commenting import comment_on_repo_files

main_routes = Blueprint('main_routes', __name__)

@main_routes.route('/')
def index():
    return render_template('index.html')

@main_routes.route('/chat', methods=['POST'])
def chat():
    user_message = request.form['message']
    ai_response = get_ai_response(user_message)
    conversation = Conversation(user_message=user_message, ai_response=ai_response)
    db.session.add(conversation)
    db.session.commit()
    return jsonify({'user_message': user_message, 'ai_response': ai_response})

@main_routes.route('/ingest_repo', methods=['POST'])
def ingest_repo():
    repo_url = request.form['repo_url']
    clone_dir = 'cloned_repo'
    clone_repo(repo_url, clone_dir)
    ingest_repo_to_db(clone_dir)
    comment_on_repo_files()
    return jsonify({'status': 'success'})
