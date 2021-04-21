import csv
from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

app.config['SERVER_NAME'] = "localhost:5000"
app.config['SQLALCHEMY_DATABASE_URI'] = "postgres://wxgncdozyktlun:09e460eb130ae553eee73db6d86051c28cab55b6591075e58f635e45a57a9a0e@ec2-3-91-127-228.compute-1.amazonaws.com:5432/d8i4kufqlg4jnh"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy()
db.init_app(app)

class Book(db.Model):
    __tablename__ = "Books"
    isbn = db.Column(db.String, nullable=False, primary_key=True)
    title = db.Column(db.String, unique=True, nullable=False)
    author = db.Column(db.String, unique=True, nullable=False)
    year = db.Column(db.String, unique=True, nullable=False)

def main():
    db.create_all()
    file = open("books.csv")
    reader = csv.reader(file)

    for isbn, title, author, year in reader:
        book = Book(isbn=isbn, title=title, author=author, year=year)
        db.session.add(book)
        # print(book.title)
    
    db.session.commit()
    print('\n## DONE ##')

def m():
    Book.query.all()

if __name__ == "__main__":
    with app.app_context():
        main()