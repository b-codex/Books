from flask import render_template, url_for, flash, redirect, request, session
from flask_app import app, bcrypt
from flask_app.forms import Register, Login, Comment
import requests

from flask_app.dbModels import *

@app.route('/')
@app.route('/home')
def home():
    return render_template('index.html', session=session)

@app.route('/search', methods=['GET', 'POST'])
def search():
    if(request.method == "POST"):
        input = request.form.get('input')
        books = findBooks('title', input)
        # print(books)
        return render_template('home.html', books=books)

    if(request.method == "GET"):
        return ("<h1>Invalid Request</h1>")

@app.route('/login', methods=['POST', 'GET'])
def login():
    if ('user' in session):
        return redirect(url_for('home'))

    form = Login()
    if (form.validate_on_submit()):
        user = find("Users", "email", form.email.data)

        if (user and bcrypt.check_password_hash(user[2], form.password.data)):
            session.permanent = True
            session['user'] = user
            return redirect(url_for('home'))
        else:
            flash('Login Unsuccessful. Please check your credentials.', 'danger')        

    return render_template('login.html', form=form)

@app.route('/register', methods=['POST', 'GET'])
def register():
    if ('user' in session):
        return redirect(url_for('home'))

    form = Register()
    if (form.validate_on_submit()):
        hashed_pass = bcrypt.generate_password_hash(
            form.password.data).decode('utf-8')

        insert_into("Users", form.username.data, form.email.data, hashed_pass)

        flash('Your account has been created!', "success")
        return redirect(url_for('login'))

    return render_template('register.html', form=form)

@app.route('/logout')
def logout():
    session.pop('user', None)
    return redirect(url_for('login'))

@app.route('/api/<string:book>')
def api(book):
    query = f'{book}'
    res = requests.get(f'https://api.itbook.store/1.0/search/{query}')
    return res.json()

@app.route('/info/<string:id>', methods=['GET', 'POST'])
def info(id):
    res = requests.get(f'https://www.googleapis.com/books/v1/volumes?q=isbn:{id}')
    books = res.json()

    form = Comment()
    rating = request.form.get('rating')

    if (books['totalItems'] == 1):    
        info = {
            'imgSrc': books['items'][0]['volumeInfo']['imageLinks']['thumbnail'],
            'isbn': books['items'][0]['volumeInfo']['industryIdentifiers'][0]['identifier'],
            'title': books['items'][0]['volumeInfo']['title'],
            'authors': books['items'][0]['volumeInfo']['authors'][0],
            'year': books['items'][0]['volumeInfo']['publishedDate'],
            'pageCount': books['items'][0]['volumeInfo']['pageCount'],
            'averageRating': books['items'][0]['volumeInfo']['averageRating'],
            'ratingsCount': books['items'][0]['volumeInfo']['ratingsCount'],
            'category': books['items'][0]['volumeInfo']['categories'][0]
        }

        localCount = len(find('Rating', "isbn", info['isbn']))
        x = 0
        for rating in find('Rating', "isbn", info['isbn']):
            x += rating[2]
        localRating = x / localCount
        apiCount = info['averageRating'] * info['ratingsCount']

        newAverageRating = ((info['averageRating'] * apiCount) + (localRating * localCount)) / (apiCount + localCount)
        print(newAverageRating)

        comments = find_comments(info['isbn'])

        if('user' in session):
            user = session['user']
            if (form.validate_on_submit()):
                insert_comment("Comments", user[0], info['isbn'], form.text.data)
                print(rating)
                return redirect(url_for('info', id=info['isbn']))

        return render_template('info.html', form=form, comments=comments, info=info, newAverageRating=newAverageRating)
    
    else:
        book = findBooks('isbn', id)
        localCount = len(find('Rating', "isbn", info['isbn']))
        x = 0
        for rating in find('Rating', "isbn", info['isbn']):
            x += rating[2]
        localRating = x / localCount
        
        info = {
            'isbn': book[0][0],
            'title': book[0][1],
            'authors': book[0][2],
            'year': book[0][3]
        }
        comments = find_comments(info['isbn'])

        if('user' in session):
            user = session['user']
            if (form.validate_on_submit()):
                insert_comment("Comments", user[0], info['isbn'], form.text.data)
                return redirect(url_for('info', id=info['isbn']))

        return render_template('info.html', form=form, comments=comments, info=info, localRating=localRating)