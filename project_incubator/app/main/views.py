from flask import render_template, redirect, url_for, request, flash
from . import main
from .forms import RegistrationForm, LoginForm

@main.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        # Handle registration logic here
        flash('Registration successful!', 'success')
        return redirect(url_for('main.login'))
    return render_template('register.html', form=form)

@main.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        # Handle login logic here
        flash('Login successful!', 'success')
        return redirect(url_for('main.home'))
    return render_template('login.html', form=form)

@main.route('/settings', methods=['GET', 'POST'])
def settings():
    if request.method == 'POST':
        # Handle settings update logic here
        flash('Settings updated!', 'success')
    return render_template('settings.html')

@main.route('/')
def index():
    return redirect(url_for('main.login'))

@main.route('/home')
def home():
    return 'Welcome to the Home Page'
