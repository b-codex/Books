import csv
import psycopg2

connection = psycopg2.connect(
    host="ec2-3-91-127-228.compute-1.amazonaws.com",
    database="d8i4kufqlg4jnh",
    user="wxgncdozyktlun",
    password="09e460eb130ae553eee73db6d86051c28cab55b6591075e58f635e45a57a9a0e"
)

# connection = psycopg2.connect(
#     host="localhost",
#     database="db",
#     user="postgres",
#     password="xd"
# )

cursor = connection.cursor()
create_table = """
        CREATE TABLE allBooks (
            isbn text NOT NULL PRIMARY KEY,
            title text NOT NULL,
            author text NOT NULL,
            year text NOT NULL
        )
"""
cursor.execute(create_table)

file = open("books.csv")
reader = csv.reader(file)

for isbn, title, author, year in reader:
    i = isbn
    t = title
    a = author
    y = year
    # print(b)

    if("'" in t or "'" in a):
        t = t.replace("'", "''")
        a = a.replace("'", "''")
        command = f'''
            INSERT INTO allBooks(isbn, title, author, year) VALUES ('{i}', '{t}', '{a}', '{y}')
        '''
        cursor.execute(command)
        print(f"{t} inserted into the db")

    if("'" not in t and "'" not in a):
        # print(t)
        command = f'''
            INSERT INTO allBooks(isbn, title, author, year) VALUES ('{i}', '{t}', '{a}', '{y}')
        '''
        cursor.execute(command)
        print(f"{t} inserted into the db")


# cursor.execute("SELECT * FROM allBooks")
# rows = cursor.fetchall()

# for row in rows:
#     print(row)

cursor.close()
connection.commit()
