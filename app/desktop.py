import sys
from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QTableWidget, 
    QTableWidgetItem, QDockWidget, QFormLayout, 
    QLineEdit, QWidget, QPushButton, QSpinBox, 
    QMessageBox, QToolBar, QHBoxLayout
)
from PyQt6.QtCore import Qt,QSize
from PyQt6.QtGui import QIcon, QAction

from utils.db import Database
from .schema import Library as Lib


class Desktop(QMainWindow):
    def __init__(self, library: Lib, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.setWindowTitle('Library Management System')
        self.setWindowIcon(QIcon('./library-logo.png'))
        self.setGeometry(100, 100, 800, 400)

        self.library : Lib = library

        # books in the library
        self.books = library.get_books()
        self.table = QTableWidget(self)
        self.setCentralWidget(self.table)

        self.table.setColumnCount(5)
        self.table.setColumnWidth(0, 150)
        self.table.setColumnWidth(1, 150)
        self.table.setColumnWidth(2, 150)
        self.table.setColumnWidth(3, 50)
        self.table.setColumnWidth(4, 50)

        self.table.setHorizontalHeaderLabels(['Title', 'Author', 'ISBN', 'Genre', 'Publication Year'])
        self.table.setRowCount(len(self.books))

        row = 0
        for book in self.books:
            self.table.setItem(row, 0, QTableWidgetItem(book[1]))
            self.table.setItem(row, 1, QTableWidgetItem(book[2]))
            self.table.setItem(row, 2, QTableWidgetItem(book[3]))
            self.table.setItem(row, 3, QTableWidgetItem(book[4]))
            self.table.setItem(row, 4, QTableWidgetItem(str(book[5])))
            row += 1

        # add book
        dock = QDockWidget("Add Book", self)
        self.addDockWidget(Qt.DockWidgetArea.RightDockWidgetArea, dock)

        widget = QWidget()
        layout = QFormLayout(widget)

        self.title = QLineEdit()
        self.author = QLineEdit()
        self.isbn = QLineEdit()
        self.genre = QLineEdit()
        self.publication_year = QLineEdit()

        layout.addRow('Title', self.title)
        layout.addRow('Author', self.author)
        layout.addRow('ISBN', self.isbn)
        layout.addRow('Genre', self.genre)
        layout.addRow('Publication Year', self.publication_year)

        add_book_button = QPushButton('Add Book or Update Existing')
        add_book_button.clicked.connect(self.add_book)
        layout.addRow(add_book_button)

        dock.setWidget(widget)

        # Delete book
        toolbar = QToolBar("Main Toolbar")
        toolbar.setIconSize(QSize(16, 16))
        self.addToolBar(toolbar)

        delete_action = QAction(QIcon('./assets/remove.png'), '&Delete', self)
        delete_action.setStatusTip('Delete a book from the library')
        delete_action.triggered.connect(self.delete_book)
        toolbar.addAction(delete_action)

        # update book
        toolbar = QToolBar("Update Toolbar")
        toolbar.setIconSize(QSize(16, 16))
        self.addToolBar(toolbar)

        update_action = QAction(QIcon('./assets/update.png'), '&Update', self)
        update_action.setStatusTip('Update a book in the library')
        update_action.triggered.connect(self.update_book)
        toolbar.addAction(update_action)

        # Search book
        toolbar = QToolBar("Search Toolbar")
        toolbar.setIconSize(QSize(16, 16))
        self.addToolBar(toolbar)

        search_layout = QHBoxLayout()
        self.search_bar = QLineEdit()
        self.search_bar.setPlaceholderText('Search by title, author, genre or ISBN')
        search_button = QPushButton('Search')
        search_button.clicked.connect(self.search_books)
        search_layout.addWidget(self.search_bar)
        search_layout.addWidget(search_button)
        layout.addRow(search_layout)


        # menu bar
        menu_bar = self.menuBar()
        file_menu = menu_bar.addMenu('File')
        file_menu.addAction('Exit', self.close)

        self.show()

    
    def delete_book(self):
        current_row = self.table.currentRow()
        if current_row < 0:
            return QMessageBox.warning(self, 'Warning','Please select a record to delete')

        button = QMessageBox.question(
            self,
            'Confirmation',
            'Are you sure that you want to delete the selected row?',
            QMessageBox.StandardButton.Yes |
            QMessageBox.StandardButton.No
        )
        if button == QMessageBox.StandardButton.Yes:
            book_id = self.books[current_row][0]
            self.books = self.library.delete_book(book_id)
            self.table.removeRow(current_row)

    def add_book(self):
        if not self.valid():
            return
        
        # check if book exists
        for book in self.books:
            if book[3] == self.isbn.text().strip() and book[2] == self.author.text().strip():
                # update the book
                # message them that we are updating the book becuase it already exists
                QMessageBox.information(
                    self,
                    'Information',
                    f'The book {self.title.text().strip()} by {self.author.text().strip()} already exists in the library. We are updating the book.'
                )
                # update the book
                self.library.update_book(
                    self.title.text().strip(),
                    self.author.text().strip(),
                    self.genre.text().strip(),
                    self.publication_year.text().strip()
                )

                # update the table
                self.table.setItem(self.table.currentRow(), 0, QTableWidgetItem(self.title.text().strip()))
                self.table.setItem(self.table.currentRow(), 1, QTableWidgetItem(self.author.text().strip()))
                self.table.setItem(self.table.currentRow(), 2, QTableWidgetItem(self.isbn.text().strip()))
                self.table.setItem(self.table.currentRow(), 3, QTableWidgetItem(self.genre.text().strip()))
                self.table.setItem(self.table.currentRow(), 4, QTableWidgetItem(self.publication_year.text().strip()))

                return

        # perform add opertion because book does not exist
        # add to the database
        self.library.add_book(
            self.title.text().strip(),
            self.author.text().strip(),
            self.isbn.text().strip(),
            self.genre.text().strip(),
            self.publication_year.text().strip()
        )

        # add to the table
        row = self.table.rowCount()
        self.table.insertRow(row)
        self.table.setItem(row, 0, QTableWidgetItem(self.title.text().strip()))
        self.table.setItem(row, 1, QTableWidgetItem(self.author.text().strip()))
        self.table.setItem(row, 2, QTableWidgetItem(self.isbn.text().strip()))
        self.table.setItem(row, 3, QTableWidgetItem(self.genre.text().strip()))
        self.table.setItem(row, 4, QTableWidgetItem(self.publication_year.text().strip()))


        self.reset()

    def update_book(self):
        current_row = self.table.currentRow()
        if current_row < 0:
            return QMessageBox.warning(self, 'Warning','Please select a record to edit')

        self.title.setText(self.table.item(current_row, 0).text())
        self.author.setText(self.table.item(current_row, 1).text())
        self.isbn.setText(self.table.item(current_row, 2).text())
        self.genre.setText(self.table.item(current_row, 3).text())
        self.publication_year.setText(self.table.item(current_row, 4).text())

        

    def search_books(self):
        search_term = self.search_bar.text().strip()
        self.books = self.library.search_books(search_term)
        self.table.setRowCount(len(self.books))
        row = 0
        for book in self.books:
            self.table.setItem(row, 0, QTableWidgetItem(book[1]))
            self.table.setItem(row, 1, QTableWidgetItem(book[2]))
            self.table.setItem(row, 2, QTableWidgetItem(book[3]))
            self.table.setItem(row, 3, QTableWidgetItem(book[4]))
            self.table.setItem(row, 4, QTableWidgetItem(str(book[5])))
            row += 1

    def valid(self):
        title = self.title.text().strip()
        author = self.author.text().strip()
        isbn = self.isbn.text().strip()
        genre = self.genre.text().strip()
        publication_year = self.publication_year.text().strip()

        if not title:
            QMessageBox.critical(self, 'Error', 'Please enter the title')
            self.title.setFocus()
            return False
        
        if not author:
            QMessageBox.critical(self, 'Error', 'Please enter the author')
            self.author.setFocus()
            return False
        
        if not isbn:
            QMessageBox.critical(self, 'Error', 'Please enter the ISBN')
            self.isbn.setFocus()
            return False
        
        if not genre:
            QMessageBox.critical(self, 'Error', 'Please enter the genre')
            self.genre.setFocus()
            return False
        
        if not publication_year:
            QMessageBox.critical(self, 'Error', 'Please enter the publication year')
            self.publication_year.setFocus()
            return False

        return title and author and isbn and genre and publication_year

    def reset(self):
        self.title.clear()
        self.author.clear()
        self.isbn.clear()
        self.genre.clear()
        self.publication_year.clear()