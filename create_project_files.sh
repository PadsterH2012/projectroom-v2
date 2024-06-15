#!/bin/bash

# Create directory structure
mkdir -p project_incubator/app/main
mkdir -p project_incubator/app/static
mkdir -p project_incubator/app/templates
mkdir -p project_incubator/instance
mkdir -p project_incubator/tests
mkdir -p project_incubator/venv

# Create __init__.py for app
cat <<EOL > project_incubator/app/__init__.py
from flask import Flask
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

def create_app(config_name):
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_object('config.Config')
    app.config.from_pyfile('config.py')

    db.init_app(app)
    
    from .main import main as main_blueprint
    app.register_blueprint(main_blueprint)
    
    return app
EOL

# Create __init__.py for main blueprint
cat <<EOL > project_incubator/app/main/__init__.py
from flask import Blueprint

main = Blueprint('main', __name__)

from . import views
EOL

# Create views.py for main blueprint
cat <<EOL > project_incubator/app/main/views.py
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

# Create instance config.py
cat <<EOL > project_incubator/instance/config.py
class Config:
    SECRET_KEY = 'you-will-never-guess'
    SQLALCHEMY_DATABASE_URI = 'sqlite:///site.db'

class TestingConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///:memory:'
    SERVER_NAME = 'localhost.localdomain'
EOL

# Create test_auth.py
cat <<EOL > project_incubator/tests/test_auth.py
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
cat <<EOL > project_incubator/tests/test_config.py
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
cat <<EOL > project_incubator/run.py
from app import create_app

app = create_app('default')

if __name__ == '__main__':
    app.run(debug=True)
EOL

# Create .flaskenv
cat <<EOL > project_incubator/.flaskenv
FLASK_APP=run.py
FLASK_ENV=development
EOL

# Create requirements.txt
cat <<EOL > project_incubator/requirements.txt
Flask
Flask-SQLAlchemy
EOL

# Create .gitignore
cat <<EOL > project_incubator/.gitignore
venv/
__pycache__/
instance/
*.pyc
.DS_Store
EOL

# Create Dockerfile
cat <<EOL > project_incubator/Dockerfile
FROM python:3.10-slim

WORKDIR /app

COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt

COPY . .

CMD ["flask", "run", "--host=0.0.0.0"]
EOL

# Create Jenkinsfile
cat <<EOL > project_incubator/Jenkinsfile
pipeline {
    agent any
    stages {
        stage('Build') {
            steps {
                sh 'python -m venv venv'
                sh './venv/bin/pip install -r requirements.txt'
            }
        }
        stage('Test') {
            steps {
                sh './venv/bin/python -m unittest discover tests'
            }
        }
    }
}
EOL

# Create empty __init__.py files
touch project_incubator/app/static/__init__.py
touch project_incubator/app/templates/__init__.py
touch project_incubator/tests/__init__.py

echo "Project structure created successfully!"
