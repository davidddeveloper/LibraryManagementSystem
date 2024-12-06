# Documentation for Library Management System

![library-management-gui-interface](/assets/gui-of-library-management-system.png)
## Overview
The Library Management System is a desktop application built with Python and PyQt6. It provides functionalities for managing a library's collection of books, allowing users to add, update, delete, and search for books in the library. The application uses an SQLite database to store book information.

## Components

### Main Application
- **`main.py`**: Initiates the application by creating instances of `Database` and `Library`, then launches the `Desktop` interface.

### GUI Interface
- **`app/desktop.py`**: Contains the `Desktop` class which sets up the main window of the application. It includes:
  - A table to display books.
  - A dock widget to add new books.
  - Methods to add, update, delete, reset, and search books.

### Database Management
- **`utils/db.py`**: Defines the `Database` class for managing database connections and executing SQL queries. Key methods include `execute`, `commit`, `fetchall`, `fetchone`, and `rollback`.

### Data Model
- **`app/schema.py`**: Contains the `Library` class which acts as a bridge between the application and the database. It includes methods for:
  - Creating the books table (`create_table`).
  - Adding (`add_book`), updating (`update_book`), retrieving (`get_book` and `get_books`), deleting (`delete_book`), and searching books (`search_books`).

### Testing
- **`tests/main.py`**: Provides basic tests for the `Library` class by adding, updating, and deleting books, and printing the results to the console.

## Key Classes and Methods

### `Desktop` Class (app/desktop.py)
- **Constructor (`__init__`)**: Sets up the GUI, initializes the book table, and adds a dock widget for adding books.
- **`add_book`**: Validates inputs and adds a new book to the library, updating the table.
- **`update_book`**: Updates the selected book's details.
- **`delete_book`**: Deletes a selected book from the library.
- **`search_books`**: Searches for books based on a search term.
- **`reset`**: Clears input fields.

### `Library` Class (app/schema.py)
- **Constructor (`__init__`)**: Initializes with a `Database` instance.
- **`create_table`**: Creates the books table if it does not exist.
- **`add_book`**: Inserts a new book into the database.
- **`update_book`**: Updates an existing book's information.
- **`get_book`** / **`get_books`**: Retrieves a single book or all books from the database.
- **`delete_book`**: Removes a book from the database.
- **`search_books`**: Searches for books using various criteria.

### `Database` Class (utils/db.py)
- **Constructor (`__init__`)**: Establishes a connection to the SQLite database.
- **`execute`**: Executes a SQL query.
- **`commit`**: Commits the current transaction.
- **`fetchall`** / **`fetchone`** / **`fetchmany`**: Fetches results from the database.
- **`rollback`**: Rolls back the current transaction in case of errors.

## Running the Application
1. Ensure Python and PyQt6 are installed.
2. Run `main.py` to start the application.
3. Use the interface to manage the library's book collection.

## Conclusion
This documentation provides an overview of the components and functionalities of the Library Management System. The application serves as a simple yet effective tool for managing a library's book database using a graphical interface.
