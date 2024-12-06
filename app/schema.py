class Library:
    def __init__(self, db):
        self.db = db

    def create_table(self):
        self.db.execute("CREATE TABLE IF NOT EXISTS books (id INTEGER PRIMARY KEY, title TEXT, author TEXT, isbn TEXT, genre TEXT, publication_year INTEGER)")
        self.db.commit()

    def add_book(self, title, author, isbn, genre, publication_year):
        self.db.execute("INSERT INTO books (title, author, isbn, genre, publication_year) VALUES (?, ?, ?, ?, ?)", (title, author, isbn, genre, publication_year))
        self.db.commit()

    def update_book(self, book_id, title, author, genre):
        self.db.execute("UPDATE books SET title = ?, author = ?, genre = ? WHERE id = ?", (title, author, genre, book_id))
        self.db.commit()

    def get_book(self, book_id):
        self.db.execute("SELECT * FROM books WHERE id = ?", (book_id,))
        return self.db.fetchone()

    def get_books(self):
        self.db.execute("SELECT * FROM books")
        return self.db.fetchall()

    def delete_book(self, book_id):
        self.db.execute("DELETE FROM books WHERE id = ?", (book_id,))
        self.db.commit()
    
    def search_books(self, title=None, author=None, isbn=None, genre=None):
        query = "SELECT * FROM books WHERE 1=1"
        params = []

        if title:
            query += " AND title LIKE ?"
            params.append(f"%{title}%")
        if author:
            query += " AND author LIKE ?"
            params.append(f"%{author}%")
        if isbn:
            query += " AND isbn LIKE ?"
            params.append(f"%{isbn}%")
        if genre:
            query += " AND genre LIKE ?"
            params.append(f"%{genre}%")

        self.db.execute(query, params)
        return self.db.fetchall()
