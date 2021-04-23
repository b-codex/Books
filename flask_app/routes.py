from flask import render_template, url_for, flash, redirect, request, session
from flask_app import app, bcrypt
from flask_app.forms import Register, Login, Comment
import requests, math

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

        if (user and bcrypt.check_password_hash(user[0][2], form.password.data)):
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

@app.route('/api/<string:isbn>')
def api(isbn):
    query = f'{isbn}'
    res = requests.get(f'https://www.googleapis.com/books/v1/volumes?q=isbn:{query}')
    return res.json()

@app.route('/info/<string:id>', methods=['GET', 'POST'])
def info(id):
    res = requests.get(f'https://www.googleapis.com/books/v1/volumes?q=isbn:{id}')
    books = res.json()

    user = ""
    loggedIn = False
    if 'user' in session:
        loggedIn = True
        user = session['user']

    form = Comment()
    rating_user = request.form.get('rating')
    if rating_user == None:
        rating_user = 0

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

        users = find_users_commented(info['isbn'])
        usersArray = []
        for x in users:
            usersArray.append(x[0])
        
        alreadyCommented = False

        if loggedIn:
            if (user[0][0] in usersArray):
                alreadyCommented = True

        newAverageRating = 0
        localCount = len(find('Ratings', "isbn", info['isbn']))
        
        x = 0
        if find('Ratings', "isbn", info['isbn']):    
            for rating in find('Ratings', "isbn", info['isbn']):
                x += int(rating[2])
            
            localRating = 0
            if localCount != 0:
                localRating = x / localCount

            apiCount = info['averageRating'] * info['ratingsCount']
            newAverageRating = math.ceil(((info['averageRating'] * apiCount) + (localRating * localCount)) / (apiCount + localCount))
            
        comments = find_comments(info['isbn'])

        if('user' in session):
            if (form.validate_on_submit()):
                insert_comment("Comments", user[0][0], info['isbn'], form.text.data)
                insert_ratings(user[0][0], info['isbn'], rating_user)
                flash('You have successfully rated & commented on this book.', 'success')
                return redirect(url_for('info', id=info['isbn']))

        return render_template('info.html', form=form, comments=comments, info=info, newAverageRating=newAverageRating, alreadyCommented=alreadyCommented)
    
    else:
        
        book = findBooks('isbn', id)
        info = {
            'imgSrc' : 'https://westsiderc.org/wp-content/uploads/2019/08/Image-Not-Available.png',
            'isbn': book[0][0],
            'title': book[0][1],
            'authors': book[0][2],
            'year': book[0][3],
            'pageCount' : 'N/A',
            'category' : 'N/A'
        }

        users = find_users_commented(info['isbn'])
        usersArray = []
        for x in users:
            usersArray.append(x[0])
        
        alreadyCommented = False
        if loggedIn:
            if (user[0][0] in usersArray):
                alreadyCommented = True

        localCount = len(find('Ratings', "isbn", info['isbn']))
        localRating = 0
        
        if (localCount != 0):
            x = 0
            for rating in find('Ratings', "isbn", info['isbn']):
                x += int(rating[2])
            localRating = math.ceil(x / localCount)
        comments = find_comments(info['isbn'])

        if('user' in session):
            user = session['user']
            if (form.validate_on_submit()):
                insert_comment("Comments", user[0][0], info['isbn'], form.text.data)
                insert_ratings(user[0][0], info['isbn'], rating_user)
                flash('You have successfully rated & commented on this book.', 'success')
                return redirect(url_for('info', id=info['isbn']))

        return render_template('info.html', form=form, comments=comments, info=info, newAverageRating=localRating, alreadyCommented=alreadyCommented)