#!/bin/bash

# Define the project directory
PROJECT_DIR="project_incubator"

# Create directory structure
mkdir -p $PROJECT_DIR/app/main
mkdir -p $PROJECT_DIR/app/static
mkdir -p $PROJECT_DIR/app/templates
mkdir -p $PROJECT_DIR/instance
mkdir -p $PROJECT_DIR/tests

# Create __init__.py for app
cat <<EOL > $PROJECT_DIR/app/__init__.py
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from dotenv import load_dotenv
import os

db = SQLAlchemy()

def create_app(config_name):
    load_dotenv()
    app = Flask(__name__, instance_relative_config=True)
    if config_name == 'testing':
        app.config.from_object('config.TestingConfig')
    else:
        app.config.from_object('config.Config')

    db.init_app(app)
    
    from .main import main as main_blueprint
    app.register_blueprint(main_blueprint)
    
    return app
EOL

# Create __init__.py for main blueprint
cat <<EOL > $PROJECT_DIR/app/main/__init__.py
from flask import Blueprint

main = Blueprint('main', __name__)

from . import views
EOL

# Create views.py for main blueprint
cat <<EOL > $PROJECT_DIR/app/main/views.py
from flask import render_template, redirect, url_for, request, flash
from . import main

@main.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        # Handle registration logic here
        return 'Registration successful'
    return render_template('register.html')

@main.route('/settings', methods=['GET', 'POST'])
def settings():
    if request.method == 'POST':
        # Handle settings update logic here
        return 'Settings updated'
    return render_template('settings.html')
EOL

# Create config.py in the root directory
cat <<EOL > $PROJECT_DIR/config.py
import os

class Config:
    SECRET_KEY = os.getenv('SECRET_KEY', 'you-will-never-guess')
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL', 'sqlite:///site.db')

class TestingConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///:memory:'
    SERVER_NAME = 'localhost.localdomain'
EOL

# Create test_auth.py
cat <<EOL > $PROJECT_DIR/tests/test_auth.py
import unittest
from flask import url_for
from app import create_app, db

class AuthTestCase(unittest.TestCase):
    def setUp(self):
        self.app = create_app('testing')
        self.app_context = self.app.app_context()
        self.app_context.push()
        self.client = self.app.test_client()
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def test_register_login_logout(self):
        with self.app.test_request_context():
            response = self.client.post(url_for('main.register'), data={
                'username': 'testuser',
                'email': 'test@example.com',
                'password': 'password',
                'password2': 'password'
            })
            self.assertEqual(response.status_code, 200)
EOL

# Create test_config.py
cat <<EOL > $PROJECT_DIR/tests/test_config.py
import unittest
from flask import url_for
from app import create_app, db

class ConfigTestCase(unittest.TestCase):
    def setUp(self):
        self.app = create_app('testing')
        self.app_context = self.app.app_context()
        self.app_context.push()
        self.client = self.app.test_client()
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def test_settings(self):
        with self.app.test_request_context():
            response = self.client.post(url_for('main.settings'), data={
                'setting1': 'value1',
                'setting2': 'value2'
            })
            self.assertEqual(response.status_code, 200)
EOL

# Create run.py
cat <<EOL > $PROJECT_DIR/run.py
from app import create_app

app = create_app('default')

if __name__ == '__main__':
    app.run(debug=True)
EOL

# Create .flaskenv
cat <<EOL > $PROJECT_DIR/.flaskenv
FLASK_APP=run.py
FLASK_ENV=development
EOL

# Create requirements.txt
cat <<EOL > $PROJECT_DIR/requirements.txt
Flask
Flask-SQLAlchemy
python-dotenv
gunicorn
pytest
Flask-WTF
EOL

# Create .gitignore
cat <<EOL > $PROJECT_DIR/.gitignore
venv/
__pycache__/
instance/
*.pyc
.DS_Store
EOL

# Create Dockerfile
cat <<EOL > $PROJECT_DIR/Dockerfile
FROM python:3.10-slim

WORKDIR /app

COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt

COPY . .

CMD ["gunicorn", "-w", "4", "-b", "0.0.0.0:8000", "run:app"]
EOL

# Create Jenkinsfile
cat <<EOL > $PROJECT_DIR/Jenkinsfile
pipeline {
    agent any
    stages {
        stage('Build') {
            steps {
                sh 'python3 -m venv venv'
                sh './venv/bin/pip install -r project_incubator/requirements.txt'
            }
        }
        stage('Test') {
            steps {
                sh './venv/bin/python3 -m pytest project_incubator/tests'
            }
        }
    }
}
EOL

# Create empty __init__.py files
touch $PROJECT_DIR/app/static/__init__.py
touch $PROJECT_DIR/app/templates/__init__.py
touch $PROJECT_DIR/tests/__init__.py

# Change to the project directory
cd $PROJECT_DIR

# Create and activate virtual environment
python3 -m venv venv
source venv/bin/activate

# Check if virtual environment is created successfully
if [ ! -f "venv/bin/python3" ]; then
    echo "Virtual environment was not created successfully."
    exit 1
fi

# Install dependencies
pip install -r requirements.txt

echo "Project structure created successfully!"
