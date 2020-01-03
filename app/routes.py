from datetime import datetime
from flask import render_template, flash, redirect, url_for, request
from flask_login import login_user, logout_user, current_user, login_required
from werkzeug.urls import url_parse
from app import app
from app.forms import LoginForm, RegistrationForm, BlockDomainForm
from app.models import User
import json
import os

@app.route('/', methods=['GET', 'POST'])
@app.route('/index', methods=['GET', 'POST'])
@login_required
def index():
    if os.name == 'posix':
        os.system('echo $PASSWORD | sudo -S sh resetPOSIX.sh')
        for domain in current_user.blocked_domains:
            os.system(f'echo $PASSWORD | sudo -S sh blockPOSIX.sh {domain}')
    elif os.name == 'nt':
        os.system('resetNT.bat')
        for domain in current_user.blocked_domains:
            os.system(f'blockNT.bat {domain}')

    form = BlockDomainForm()
    if form.validate_on_submit():
        current_user.blocked_domains = list(dict.fromkeys([form.domain.data.lower()] + current_user.blocked_domains))
        data = {}
        with open('data.json') as json_file:
            data = json.load(json_file)
        data[current_user.username]['blocked_domains'] = current_user.blocked_domains
        with open('data.json', 'w') as json_file:
            json.dump(data, json_file)

        flash(f'{form.domain.data} added to block list')
        return redirect(url_for('index'))
    return render_template('index.html', title='Home', form=form, domains=current_user.blocked_domains)

@app.route('/delete/<domain>', methods=['POST'])
def delete(domain):
    if domain in current_user.blocked_domains:
        current_user.blocked_domains.remove(domain)

    with open('data.json') as json_file:
        data = json.load(json_file)
    data[current_user.username]['blocked_domains'] = current_user.blocked_domains
    with open('data.json', 'w') as json_file:
        json.dump(data, json_file)

    return redirect(url_for('index'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.get(username=form.username.data)
        if user is None or not user.check_password(form.password.data):
            flash('Invalid username or password', category='error')
            return redirect(url_for('login'))
        login_user(user, remember=form.remember_me.data)
        next_page = request.args.get('next')
        if not next_page or url_parse(next_page).netloc != '':
            next_page = url_for('index')
        return redirect(next_page)
    return render_template('login.html', title='Sign In', form=form)


@app.route('/logout')
def logout():
    logout_user()
    if os.name == 'posix':
        os.system('echo $PASSWORD | sudo sh resetPOSIX.sh')
    elif os.name == 'nt':
        os.system('resetNT.bat')
    return redirect(url_for('index'))


@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User()
        user.username = form.username.data
        user.set_password(form.password.data)

        data = {}
        with open('data.json') as json_file:
            data = json.load(json_file)
        data[form.username.data] = {'password_hash':user.password_hash, 'blocked_domains':[]}
        with open('data.json', 'w') as json_file:
            json.dump(data, json_file)
        
        flash('Congratulations, you are now a registered user!')
        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form)