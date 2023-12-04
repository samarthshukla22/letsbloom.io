from flask import Flask, jsonify, request
import mysql.connector

app = Flask(__name__)


db_config = {
    'host': 'localhost',
    'port': 3306,
    'database': 'library',
    'user': 'root',
    'password': 'samarth'
}

def connect_to_db():
    try:
    
        db_connection = mysql.connector.connect(**db_config)
        return db_connection
    except Exception as e:
        print(f"Error connecting to the database: {e}")
        raise

def fetch_all_books(db_connection):
    try:
        cursor = db_connection.cursor(dictionary=True)
        cursor.execute("SELECT * FROM books")
        books = cursor.fetchall()
        cursor.close()
        return books
    except Exception as e:
        print(f"Error fetching books from the database: {e}")
        raise

def close_db_connection(db_connection):
    try:
        db_connection.close()
    except Exception as e:
        print(f"Error closing the database connection: {e}")
        raise

def check_duplicate_book(db_connection, title, author):
    try:
        cursor = db_connection.cursor()
        cursor.execute("SELECT * FROM books WHERE title = %s AND author = %s", (title, author))
        duplicate = cursor.fetchone()
        cursor.close()
        return duplicate is not None
    except Exception as e:
        print(f"Error checking duplicate book in the database: {e}")
        raise

def add_book(db_connection, title, author, genre):
    try:
        cursor = db_connection.cursor()
        cursor.execute("INSERT INTO books (title, author, genre) VALUES (%s, %s, %s)", (title, author, genre))
        db_connection.commit()
        cursor.close()
    except Exception as e:
        print(f"Error adding book to the database: {e}")
        db_connection.rollback()
        raise

def find_book(db_connection, book_id):
    try:
        cursor = db_connection.cursor(dictionary=True)
        cursor.execute("SELECT * FROM books WHERE id = %s", (book_id,))
        book = cursor.fetchone()
        cursor.close()
        return book
    except Exception as e:
        print(f"Error finding book in the database: {e}")
        raise

def update_book(db_connection, book_id, title, author, genre):
    try:
        cursor = db_connection.cursor()
        cursor.execute("UPDATE books SET title = %s, author = %s, genre = %s WHERE id = %s",
                       (title, author, genre, book_id))
        db_connection.commit()
        cursor.close()
    except Exception as e:
        print(f"Error updating book in the database: {e}")
        db_connection.rollback()
        raise

# Getting the books details
@app.route('/api/books', methods=['GET'])
def get_all_books():
    try:
   
        db_connection = connect_to_db()
        books = fetch_all_books(db_connection)
        close_db_connection(db_connection)
        return jsonify({'books': books}), 200
    except Exception as e:
        return jsonify({'error': f'Error retrieving books: {str(e)}'}), 500

# Adding books details
@app.route('/api/books', methods=['POST'])
def add_new_book():
    try:
        new_book_data = request.get_json()

        if not new_book_data:
            return jsonify({'error': 'Invalid request body'}), 400
        book_title = new_book_data['title']
        book_author = new_book_data['author']
        book_genre = new_book_data['genre']

        db_connection = connect_to_db()

        is_duplicate = check_duplicate_book(db_connection, book_title, book_author)

        if is_duplicate:
            return jsonify({'error': 'Book already exists'}), 400

        add_book(db_connection, book_title, book_author, book_genre)

        close_db_connection(db_connection)

        return jsonify({'message': 'Book added successfully'}), 201
    except Exception as e:
        return jsonify({'error': f'Error adding book: {str(e)}'}), 500

#updating book details using id as a key parameter for identifying the book which we have to update
@app.route('/api/books/<int:id>', methods=['PUT'])
def update_book_details(id):
    try:
        updated_book_data = request.get_json()

        if not updated_book_data:
            return jsonify({'error': 'Invalid request body'}), 400

        updated_title = updated_book_data['title']
        updated_author = updated_book_data['author']
        updated_genre = updated_book_data['genre']

        db_connection = connect_to_db()
        book = find_book(db_connection, id)

        if not book:
            return jsonify({'error': 'Book not found'}), 404
        update_book(db_connection, id, updated_title, updated_author, updated_genre)


        close_db_connection(db_connection)


        return jsonify({'message': 'Book updated successfully'}), 200
    except Exception as e:
        return jsonify({'error': f'Error updating book: {str(e)}'}), 500
    
if __name__ == '__main__':
    app.run(debug=True)
