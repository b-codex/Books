import psycopg2, datetime

connection = psycopg2.connect(
    host="ec2-3-91-127-228.compute-1.amazonaws.com",
    database="d8i4kufqlg4jnh",
    user="wxgncdozyktlun",
    password="09e460eb130ae553eee73db6d86051c28cab55b6591075e58f635e45a57a9a0e"
)

cursor = connection.cursor()

def create_users_table(tableName):
    create_table = f"""
        CREATE TABLE {tableName} (
            username text NOT NULL,
            email text NOT NULL PRIMARY KEY,
            password text NOT NULL
        )
    """
    cursor.execute(create_table)
    connection.commit()
    print(f"Successfully Created Table {tableName}")

def create_ratings_table(tableName):
    command = f"""
        CREATE TABLE {tableName} (
            username text NOT NULL,
            isbn text NOT NULL,
            rating text NOT NULL
        )
    """
    cursor.execute(command)
    connection.commit()
    print(f"Successfully Created Table {tableName}")

def create_comments_table(tableName):
    create_table = f"""
        CREATE TABLE {tableName} (
            username text NOT NULL,
            isbn text NOT NULL,
            comment text NOT NULL, 
            time text NOT NULL
        )
    """
    cursor.execute(create_table)
    connection.commit()
    print(f"Successfully Created Table {tableName}")

def drop_table(tableName):
    command = f"DROP TABLE {tableName}"
    cursor.execute(command)
    connection.commit()
    print(f"Successfully Dropped {tableName}")

def insert_into(tableName, username, email, password):
    command = f'''
        INSERT INTO {tableName} (username, email, password) VALUES ('{username}', '{email}', '{password}')
    '''
    cursor.execute(command)
    connection.commit()
    print(f"Successfully Inserted User {email}")

def insert_comment(tableName, username, isbn, comment):
    time = datetime.datetime.now()
    time = time.strftime("%b %d %Y %H:%M:%S")
    command = f'''
        INSERT INTO {tableName} (username, isbn, comment, time) VALUES ('{username}', '{isbn}', '{comment}', '{time}')
    '''
    cursor.execute(command)
    connection.commit()
    print("Successfully Inserted Comment")

def find(tableName, query, entry):
    command = f'''
        SELECT * FROM {tableName} WHERE {query}='{entry}'
    '''
    cursor.execute(command)
    rows = cursor.fetchone()
    return (rows)

def findBooks(query, entry):
    command = f'''
        SELECT * FROM allBooks WHERE {query} iLIKE '{entry}%'
    '''
    cursor.execute(command)
    rows = cursor.fetchall()
    return (rows)

def find_comments(isbn):
    command = f'''
        SELECT * FROM Comments WHERE isbn='{isbn}'
    '''
    cursor.execute(command)
    rows = cursor.fetchall()
    return (rows)

def get_all_books():
    command = f'''
        SELECT * FROM allBooks
    '''
    cursor.execute(command)
    rows = cursor.fetchall()
    return rows