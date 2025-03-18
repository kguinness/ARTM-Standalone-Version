# src/main.py

import sys
from PyQt5.QtWidgets import QApplication
from config.config import STYLE_PATH
from app import BasicFrontendApp

def main():
    app = QApplication(sys.argv)
    with open(STYLE_PATH, "r") as f:
        app.setStyleSheet(f.read())
    window = BasicFrontendApp()
    window.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()
