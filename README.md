# Books

This project is based on the Google Books API to get information about any book and it already has about 5000 books stored in the application database to make searching a lot easier.

# Overview
You can use this app to find books, see their information, rate & comment on a book.
Click on this [[link]](#https://web-prog-project-one.herokuapp.com/) to visit the website.

# Getting Started
## PostgreSQL
I used PostgresSQL database to store basic information on a book such as ISBN, Title, Author and Published Year. I also used this database to store information about users such as Username, Email and Password. Another use is to store the user ratings and comments.

## Framework
This app is built by using the flask framework of python.
I have used many modules in-order to run the app such as wt-forms to create and manage forms, datetime module to take the time when a user leaves a comment and most important of all flask-sqlalchemy used to build the database and connect to it in-order for it to use the data inside it.

# Usage

1. A user can browse the website freely, but in-order to rate a book such user must register an account on the website and proceed to the login page.
   After a successful login, such user can search for a book and rate it.
2. The file import.py is used to import books from books.csv to a database so that the app can use it later to find a book from this same database.
3. Each book has details about it such as ISBN, Authors, Title, Rating and Page Count.
4. Any user can rate and comment on a book, BUT ONLY ONCE.

# API
To send an API request you use the link [[https://web-prog-project-one.herokuapp.com/api/isbn]](#https://web-prog-project-one.herokuapp.com/api/isbn).
Note: Don't forget to replace isbn with a books isbn number, either ISBN10 orISBN13.
The API gives a response as follows:

```json

{
    "items": [{
        "accessInfo": {
            "accessViewStatus": "NONE",
            "country": "ET",
            "embeddable": false,
            "epub": {
                "isAvailable": false
            },
            "pdf": {
                "isAvailable": false
            },
            "publicDomain": false,
            "quoteSharingAllowed": false,
            "textToSpeechPermission": "ALLOWED",
            "viewability": "NO_PAGES",
            "webReaderLink": "http://play.google.com/books/reader?id=cWtglGzhPPEC&hl=&printsec=frontcover&source=gbs_api"
        },
        "etag": "s0XY8231mzo",
        "id": "cWtglGzhPPEC",
        "kind": "books#volume",
        "saleInfo": {
            "country": "ET",
            "isEbook": false,
            "saleability": "NOT_FOR_SALE"
        },
        "searchInfo": {
            "textSnippet": "A historical chronicle of Victorian London&#39;s worst cholera outbreak traces the day-by-day efforts of Dr. John Snow, who put his own life on the line in his efforts to prove his previously dismissed contagion theory about how the epidemic ..."
        },
        "selfLink": "https://www.googleapis.com/books/v1/volumes/cWtglGzhPPEC",
        "volumeInfo": {
            "allowAnonLogging": false,
            "authors": [
                "Steven Johnson"
            ],
            "averageRating": 4,
            "canonicalVolumeLink": "https://books.google.com/books/about/The_Ghost_Map.html?hl=&id=cWtglGzhPPEC",
            "categories": [
                "History"
            ],
            "contentVersion": "0.1.1.0.preview.0",
            "description": "A historical chronicle of Victorian London's worst cholera outbreak traces the day-by-day efforts of Dr. John Snow, who put his own life on the line in his efforts to prove his previously dismissed contagion theory about how the epidemic was spreading. 80,000 first printing.",
            "imageLinks": {
                "smallThumbnail": "http://books.google.com/books/content?id=cWtglGzhPPEC&printsec=frontcover&img=1&zoom=5&source=gbs_api",
                "thumbnail": "http://books.google.com/books/content?id=cWtglGzhPPEC&printsec=frontcover&img=1&zoom=1&source=gbs_api"
            },
            "industryIdentifiers": [{
                    "identifier": "1594489254",
                    "type": "ISBN_10"
                },
                {
                    "identifier": "9781594489259",
                    "type": "ISBN_13"
                }
            ],
            "infoLink": "http://books.google.com/books?id=cWtglGzhPPEC&dq=isbn:1594489254&hl=&source=gbs_api",
            "language": "en",
            "maturityRating": "NOT_MATURE",
            "pageCount": 299,
            "panelizationSummary": {
                "containsEpubBubbles": false,
                "containsImageBubbles": false
            },
            "previewLink": "http://books.google.com/books?id=cWtglGzhPPEC&dq=isbn:1594489254&hl=&cd=1&source=gbs_api",
            "printType": "BOOK",
            "publishedDate": "2006",
            "publisher": "Penguin",
            "ratingsCount": 98,
            "readingModes": {
                "image": false,
                "text": false
            },
            "subtitle": "The Story of London's Most Terrifying Epidemic--and how it Changed Science, Cities, and the Modern World",
            "title": "The Ghost Map"
        }
    }],
    "kind": "books#volumes",
    "totalItems": 1
}

```










