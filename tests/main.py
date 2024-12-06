from utils.db import Database
from app.schema import Library

if __name__ == "__main__":
    db = Database("library.db")
    library = Library(db)
    #library.create_table()

    library.add_book("The Great Gatsby", "F. Scott Fitzgerald", "9780743273565", "Novel", 1925)
    library.add_book("To Kill a Mockingbird", "Harper Lee", "9780061120084", "Novel", 1960)
    library.add_book("The Catcher in the Rye", "J.D. Salinger", "9780316769174", "Novel", 1951)

    print("All books:")
    for book in library.get_books():
        print(book)

    print("\nBooks by J.D. Salinger:")
    for book in library.search_books(author="j.d"):
        print(book)

    library.update_book(1, title="The Great Gatspy", author="F. Scott Fitzgerald", genre="Comic")
    print("\nUpdated book:")
    print(library.get_book(1))

    library.delete_book(2)
    print("\nBooks left:")
    for book in library.get_books():
        print(book)
