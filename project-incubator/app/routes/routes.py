from flask import Blueprint, render_template, redirect, url_for, request, flash, jsonify
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user, login_required, logout_user, current_user
from flask_socketio import emit, join_room, leave_room
from app import db, login_manager, socketio
from app.models.models import User, Project, Settings, Agent, AgentRole, AgentRoleAssignment, Chat  # Ensure all models are imported

routes_blueprint = Blueprint('routes', __name__)

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

@routes_blueprint.route('/')
def index():
    return render_template('index.html')

@routes_blueprint.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']
        hashed_password = generate_password_hash(password, method='pbkdf2:sha256')
        
        new_user = User(username=username, email=email, password_hash=hashed_password)
        db.session.add(new_user)
        db.session.commit()
        
        flash('Registration successful! Please log in.', 'success')
        return redirect(url_for('routes.login'))
    return render_template('register.html')

@routes_blueprint.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        user = User.query.filter_by(email=email).first()
        
        if user and check_password_hash(user.password_hash, password):
            login_user(user)
            flash('Logged in successfully.', 'success')
            return redirect(url_for('routes.index'))
        else:
            flash('Login failed. Check your email and password.', 'danger')
    return render_template('login.html')

@routes_blueprint.route('/logout')
@login_required
def logout():
    logout_user()
    flash('You have been logged out.', 'success')
    return redirect(url_for('routes.index'))

@routes_blueprint.route('/projects')
@login_required
def projects():
    projects = Project.query.filter_by(user_id=current_user.id).all()
    return render_template('projects.html', projects=projects)

@routes_blueprint.route('/project/<int:project_id>')
@login_required
def project(project_id):
    project = Project.query.get_or_404(project_id)
    return render_template('project.html', project=project)

@routes_blueprint.route('/project/<int:project_id>/edit', methods=['GET', 'POST'])
@login_required
def edit_project(project_id):
    project = Project.query.get_or_404(project_id)
    if request.method == 'POST':
        project.name = request.form['name']
        project.description = request.form['description']
        project.git_url = request.form['git_url']
        project.goals = request.form['goals']
        project.objectives = request.form['objectives']
        project.features = request.form['features']
        project.steps = request.form['steps']
        db.session.commit()
        return redirect(url_for('routes.project', project_id=project.id))
    return render_template('edit_project.html', project=project)

@routes_blueprint.route('/project/<int:project_id>/delete', methods=['POST'])
@login_required
def delete_project(project_id):
    project = Project.query.get_or_404(project_id)
    db.session.delete(project)
    db.session.commit()
    return redirect(url_for('routes.projects'))

@routes_blueprint.route('/project/add', methods=['GET', 'POST'])
@login_required
def add_project():
    if request.method == 'POST':
        name = request.form['name']
        description = request.form['description']
        git_url = request.form['git_url']
        goals = request.form['goals']
        objectives = request.form['objectives']
        features = request.form['features']
        steps = request.form['steps']
        new_project = Project(name=name, description=description, git_url=git_url, goals=goals, objectives=objectives, features=features, steps=steps, user_id=current_user.id)
        db.session.add(new_project)
        db.session.commit()
        flash('Project added successfully', 'success')
        return redirect(url_for('routes.projects'))
    return render_template('add_project.html')


@routes_blueprint.route('/settings', methods=['GET', 'POST'])
@login_required
def settings():
    if request.method == 'POST':
        for key, value in request.form.items():
            setting = Settings.query.filter_by(name=key).first()
            if setting:
                setting.value = value
            else:
                new_setting = Settings(name=key, value=value)
                db.session.add(new_setting)
        db.session.commit()
        flash('Settings updated successfully', 'success')
        return redirect(url_for('routes.settings'))
    settings = Settings.query.all()
    return render_template('settings.html', settings=settings)

@routes_blueprint.route('/manage_agents', methods=['GET', 'POST'])
@login_required
def manage_agents():
    if request.method == 'POST':
        name = request.form['name']
        api_key = request.form['api_key']
        endpoint = request.form['endpoint']
        model = request.form['model']
        new_agent = Agent(name=name, api_key=api_key, endpoint=endpoint, model=model)
        db.session.add(new_agent)
        db.session.commit()
        flash('Agent added successfully', 'success')
        return redirect(url_for('routes.manage_agents'))
    agents = Agent.query.all()
    roles = AgentRole.query.all()
    return render_template('manage_agents.html', agents=agents, roles=roles)

@routes_blueprint.route('/delete_agent/<int:agent_id>', methods=['POST'])
@login_required
def delete_agent(agent_id):
    agent = Agent.query.get_or_404(agent_id)
    db.session.delete(agent)
    db.session.commit()
    flash('Agent deleted successfully', 'success')
    return redirect(url_for('routes.manage_agents'))

@routes_blueprint.route('/add_role', methods=['GET', 'POST'])
@login_required
def add_role():
    if request.method == 'POST':
        name = request.form['name']
        system_prompt = request.form['system_prompt']
        new_role = AgentRole(name=name, system_prompt=system_prompt)
        db.session.add(new_role)
        db.session.commit()
        flash('Role added successfully', 'success')
        return redirect(url_for('routes.manage_agents'))
    return render_template('add_role.html')

@routes_blueprint.route('/assign_role', methods=['POST'])
@login_required
def assign_role():
    agent_id = request.form['agent_id']
    role_id = request.form['role_id']
    project_id = request.form['project_id']
    new_assignment = AgentRoleAssignment(agent_id=agent_id, role_id=role_id, project_id=project_id)
    db.session.add(new_assignment)
    db.session.commit()
    flash('Role assigned successfully', 'success')
    return redirect(url_for('routes.manage_agents'))

@routes_blueprint.route('/profile', methods=['GET', 'POST'])
@login_required
def profile():
    if request.method == 'POST':
        current_user.username = request.form['username']
        current_user.email = request.form['email']
        if request.form['password']:
            current_user.password_hash = generate_password_hash(request.form['password'], method='pbkdf2:sha256')
        db.session.commit()
        flash('Profile updated successfully', 'success')
        return redirect(url_for('routes.profile'))
    return render_template('profile.html')

@routes_blueprint.route('/project/<int:project_id>/chat')
@login_required
def project_chat(project_id):
    project = Project.query.get_or_404(project_id)
    return render_template('chat.html', project=project)

@socketio.on('send_message')
def handle_send_message_event(data):
    project_id = data['project_id']
    message = data['message']
    user_message = Chat(project_id=project_id, user_message=message, ai_response="Response from AI")  # Replace with actual AI response
    db.session.add(user_message)
    db.session.commit()
    emit('receive_message', {'message': message, 'project_id': project_id}, broadcast=True)

@socketio.on('join')
def handle_join_event(data):
    project_id = data['project_id']
    join_room(project_id)
    emit('status', {'msg': f'User has entered the project room {project_id}'}, room=project_id)

@socketio.on('leave')
def handle_leave_event(data):
    project_id = data['project_id']
    leave_room(project_id)
    emit('status', {'msg': f'User has left the project room {project_id}'}, room=project_id)
