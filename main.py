from app.desktop import Desktop
from app.desktop import QApplication
from app.schema import Library
from utils.db import Database
import sys


db = Database("library.db")
library = Library(db)
if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = Desktop(library)

    sys.exit(app.exec())