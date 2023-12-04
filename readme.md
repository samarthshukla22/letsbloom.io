# Library Management API

This is a simple Flask API for managing a library's book inventory. The API allows you to retrieve all books, add a new book, and update the details of an existing book.

## Setup

1. Install the required dependencies:

   ```bash
   pip install Flask mysql-connector-python
Create a MySQL database named library with the following table:
CREATE TABLE books (
    id INT AUTO_INCREMENT PRIMARY KEY,
    title VARCHAR(255) NOT NULL,
    author VARCHAR(255) NOT NULL,
    genre VARCHAR(255),
    UNIQUE KEY (title, author)
);
2. Update the db_config dictionary in the app.py file with your MySQL database credentials.
   python app.py
  The API will run on http://127.0.0.1:5000/ by default.
 Endpoints
  1. Get All Books
     Endpoint: /api/books
     Method: GET
     Description: Retrieve details of all books in the library.
  2. Add a New Book
     Endpoint: /api/books
     Method: POST
     Description: Add a new book to the library.
  Request Body:
  {
    "title": "The Great Gatsby",
    "author": "F. Scott Fitzgerald",
    "genre": "Fiction"
  }
  3. Update Book Details
     Endpoint: /api/books/<int:id>
     Method: PUT
     Description: Update the details of a specific book identified by its id.
  Request Body:
 {
    "title": "Updated Title",
    "author": "Updated Author",
    "genre": "Updated Genre"
 }
 Error Handling
 The API provides appropriate error messages and status codes for invalid requests or database errors.
 Contributions
 Feel free to contribute to the project by submitting pull requests or reporting issues.


Make sure to customize the instructions and details based on your specific application and requirements.
