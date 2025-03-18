import sys
from PyQt5.QtWidgets import QApplication
from ARTM import BasicFrontendApp  # Adjust if your main window file has a different name

def main():
    app = QApplication(sys.argv)

    # Load the global stylesheet from style.qss
    with open("style.qss", "r") as f:
        style_sheet = f.read()
    app.setStyleSheet(style_sheet)

    window = BasicFrontendApp()
    window.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()
