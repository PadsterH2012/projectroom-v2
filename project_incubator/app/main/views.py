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
