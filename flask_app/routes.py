from flask import render_template, url_for, flash, redirect, request
from flask_app import app, db, bcrypt
from flask_app.forms import Register, Login
from flask_app.models import User
from flask_login import login_user, current_user, logout_user
import requests


@app.route('/')
@app.route('/home')
def home():
    # res = requests.get('https://api.itbook.store/1.0/new')
    # res = res.json()
    # books = res['books']
    res = requests.get('https://www.googleapis.com/books/v1/volumes?q=search+terms')
    res = res.json()
    books = res
    return render_template('index.html', books=books)

@app.route('/search', methods=['GET', 'POST'])
def search():
    if(request.method == "POST"):
        input = request.form.get('input')
        print(input)
        res = requests.get(f'https://api.itbook.store/1.0/search/{input}')
        res = res.json()
        books = res['books']
        return render_template('index.html', books=books)

    if(request.method == "GET"):
        return ("<h1>Invalid Request</h1>")

@app.route('/login', methods=['POST', 'GET'])
def login():
    if (current_user.is_authenticated):
        return redirect(url_for('login'))

    form = Login()
    if (form.validate_on_submit()):
        user = User.query.filter_by(email=form.email.data).first()
        if (user and bcrypt.check_password_hash(user.password, form.password.data)):
            login_user(user, remember=form.remember.data)
            return redirect(url_for('home'))
        else:
            flash('Login Unsuccessful. Please check your credentials.', 'danger')

    return render_template('login.html', form=form)

@app.route('/register', methods=['POST', 'GET'])
def register():
    if (current_user.is_authenticated):
        return redirect(url_for('login'))

    form = Register()
    if (form.validate_on_submit()):
        hashed_pass = bcrypt.generate_password_hash(
            form.password.data).decode('utf-8')
        user = User(username=form.username.data,
                    email=form.email.data, password=hashed_pass)
        # print(user)
        db.session.add(user)
        db.session.commit()
        flash('Your account has been created!', "success")
        return redirect(url_for('login'))
    return render_template('register.html', form=form)

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('login'))

@app.route('/api/<string:book>')
def api(book):
    query = f'{book}'
    res = requests.get(f'https://api.itbook.store/1.0/search/{query}')
    return res.json()
