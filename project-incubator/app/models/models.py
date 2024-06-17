from app import db
from flask_login import UserMixin

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(150), unique=True, nullable=False)
    email = db.Column(db.String(150), unique=True, nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)
    projects = db.relationship('Project', back_populates='user')

    @property
    def is_authenticated(self):
        return True

    @property
    def is_active(self):
        return True

    @property
    def is_anonymous(self):
        return False

    def get_id(self):
        return str(self.id)

class Project(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(150), nullable=False)
    description = db.Column(db.Text, nullable=False)
    git_url = db.Column(db.String(255), nullable=False)
    goals = db.Column(db.Text, nullable=True)
    objectives = db.Column(db.Text, nullable=True)
    features = db.Column(db.Text, nullable=True)
    steps = db.Column(db.Text, nullable=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    user = db.relationship('User', back_populates='projects')
    chats = db.relationship('Chat', backref='project', lazy=True)

class Chat(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    project_id = db.Column(db.Integer, db.ForeignKey('project.id'), nullable=False)
    user_message = db.Column(db.Text, nullable=False)
    ai_response = db.Column(db.Text, nullable=False)
    timestamp = db.Column(db.DateTime, default=db.func.current_timestamp())

class Settings(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(150), nullable=False)
    value = db.Column(db.String(255), nullable=False)

class Agent(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(150), nullable=False)
    api_key = db.Column(db.String(255), nullable=False)
    endpoint = db.Column(db.String(255), nullable=False)
    model = db.Column(db.String(150), nullable=False)

class AgentRole(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(150), nullable=False)
    system_prompt = db.Column(db.Text, nullable=False)

class AgentRoleAssignment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    agent_id = db.Column(db.Integer, db.ForeignKey('agent.id'), nullable=False)
    role_id = db.Column(db.Integer, db.ForeignKey('agent_role.id'), nullable=False)
    project_id = db.Column(db.Integer, db.ForeignKey('project.id'), nullable=False)

    agent = db.relationship('Agent', backref=db.backref('assignments', cascade='all, delete-orphan'))
    role = db.relationship('AgentRole', backref=db.backref('assignments', cascade='all, delete-orphan'))
    project = db.relationship('Project', backref=db.backref('assignments', cascade='all, delete-orphan'))
