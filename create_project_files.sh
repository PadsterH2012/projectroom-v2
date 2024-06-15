#!/bin/bash

# Define the project name
PROJECT_NAME="project_incubator"

# Create project structure
mkdir -p ${PROJECT_NAME}/{app/{templates,static},tests,venv}

# Create blank Python files
touch ${PROJECT_NAME}/{app/{__init__.py,models.py,routes.py,forms.py,config.py},tests/{__init__.py,test_auth.py,test_config.py,test_home.py,test_settings.py},run.py,requirements.txt}

# Create HTML template files
touch ${PROJECT_NAME}/app/templates/{base.html,home.html,login.html,register.html,settings.html}

# Create a .flaskenv file
cat <<EOL > ${PROJECT_NAME}/.flaskenv
FLASK_APP=run.py
FLASK_ENV=development
EOL

# Create a .gitignore file
cat <<EOL > ${PROJECT_NAME}/.gitignore
venv/
__pycache__/
*.pyc
*.pyo
*.pyd
.Python
.env
build/
dist/
*.egg-info/
.installed.cfg
*.egg
.DS_Store
*.log
*.sqlite3
instance/
.cache/
*.pyc
coverage.xml
*.cover
.hypothesis/
.tox/
.pytest_cache/
.coverage
*.bak
EOL

# Create a .dockerignore file
cat <<EOL > ${PROJECT_NAME}/.dockerignore
venv/
__pycache__/
*.pyc
*.pyo
*.pyd
.Python
.env
build/
dist/
*.egg-info/
.installed.cfg
*.egg
.DS_Store
*.log
*.sqlite3
instance/
.cache/
*.pyc
coverage.xml
*.cover
.hypothesis/
.tox/
.pytest_cache/
.coverage
*.bak
EOL

# Create a Dockerfile
cat <<EOL > ${PROJECT_NAME}/Dockerfile
# Use an official Python runtime as a parent image
FROM python:3.10-slim

# Set the working directory in the container
WORKDIR /usr/src/app

# Copy the requirements file into the container at /usr/src/app
COPY requirements.txt ./

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application code to /usr/src/app
COPY . .

# Make port 5000 available to the world outside this container
EXPOSE 5000

# Define environment variable
ENV FLASK_APP=run.py
ENV FLASK_ENV=production

# Run app.py when the container launches
CMD ["flask", "run", "--host=0.0.0.0"]
EOL

# Create a Jenkinsfile
cat <<EOL > ${PROJECT_NAME}/Jenkinsfile
pipeline {
    agent any

    stages {
        stage('Build') {
            steps {
                script {
                    if (fileExists('venv')) {
                        dir('venv') {
                            deleteDir()
                        }
                    }
                }
                sh 'python -m venv venv'
                sh './venv/bin/pip install -r requirements.txt'
            }
        }

        stage('Test') {
            steps {
                sh './venv/bin/python -m unittest discover tests'
            }
        }

        stage('Build Docker Image') {
            steps {
                script {
                    docker.build("project_incubator:latest")
                }
            }
        }

        stage('Push Docker Image') {
            environment {
                DOCKERHUB_CREDENTIALS = credentials('your-dockerhub-credentials-id')
            }
            steps {
                script {
                    docker.withRegistry('https://registry.hub.docker.com', 'DOCKERHUB_CREDENTIALS') {
                        docker.image('project_incubator:latest').push('latest')
                    }
                }
            }
        }
    }

    post {
        always {
            cleanWs()
        }
    }
}
EOL

# Provide initial content to config.py
cat <<EOL > ${PROJECT_NAME}/app/config.py
class Config:
    SECRET_KEY = 'your_secret_key'
    SQLALCHEMY_DATABASE_URI = 'sqlite:///site.db'
EOL

echo "Project structure and files created successfully!"
