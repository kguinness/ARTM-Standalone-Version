import sys
import os
from PyQt5.QtWidgets import QMainWindow, QStackedWidget, QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QApplication
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import Qt
from pages.profile_selection.profile_selection_page import ProfileSelectionPage
from pages.profile_creation.profile_creation_page import ProfileCreationPage
from pages.profile_view.profile_page import ProfilePage
from pages.home.home_page import HomePage
from pages.gesture_capture.gesture_capture_page import GestureCapturePage
from pages.settings.settings_page import SettingsPage
from config.config import ICON_PATH


class BasicFrontendApp(QMainWindow):
    def __init__(self):
        super(BasicFrontendApp, self).__init__()
        self.current_profile = None
        self.initUI()

    def initUI(self):
        # Create the login stack (holds Profile Selection and Profile Creation pages)
        self.login_stack = QStackedWidget()
        self.profile_selection_page = ProfileSelectionPage(self)
        self.profile_selection_page.profileSelected.connect(self.on_profile_selected)
        self.login_stack.addWidget(self.profile_selection_page)  # index 0: selection

        self.profile_creation_page = ProfileCreationPage(self)
        self.profile_creation_page.profileCreated.connect(self.on_profile_created)
        self.profile_creation_page.backRequested.connect(self.on_profile_creation_back)
        self.login_stack.addWidget(self.profile_creation_page)  # index 1: creation

        # Create the main widget (with top bar, side bar, and content stack)
        self.main_widget = QWidget()
        main_layout = QVBoxLayout(self.main_widget)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)

        # Top Bar
        self.top_bar = QWidget()
        self.top_bar.setObjectName("TopBar")
        top_layout = QHBoxLayout(self.top_bar)
        top_layout.setContentsMargins(10, 10, 10, 10)
        top_layout.setSpacing(10)
        top_layout.addStretch()
        self.title_button = QPushButton("ARTM")
        self.title_button.setObjectName("TitleButton")
        self.title_button.clicked.connect(self.show_home)
        top_layout.addWidget(self.title_button, alignment=Qt.AlignCenter)
        top_layout.addStretch()
        main_layout.addWidget(self.top_bar)

        # Content Area: Side Bar + Content Stack
        content_widget = QWidget()
        content_layout = QHBoxLayout(content_widget)
        content_layout.setContentsMargins(0, 0, 0, 0)
        content_layout.setSpacing(0)

        # Side Bar with navigation buttons
        self.side_bar = QWidget()
        self.side_bar.setObjectName("Sidebar")
        side_layout = QVBoxLayout(self.side_bar)
        side_layout.setAlignment(Qt.AlignTop)
        gesture_btn = QPushButton("Gesture Capture")
        gesture_btn.setObjectName("SidebarButton")
        gesture_btn.clicked.connect(lambda: self.content_stack.setCurrentWidget(self.gesture_capture_page))
        side_layout.addWidget(gesture_btn)
        profile_btn = QPushButton("Profile")
        profile_btn.setObjectName("SidebarButton")
        profile_btn.clicked.connect(lambda: self.content_stack.setCurrentWidget(self.profile_page))
        side_layout.addWidget(profile_btn)
        settings_btn = QPushButton("Settings")
        settings_btn.setObjectName("SidebarButton")
        settings_btn.clicked.connect(lambda: self.content_stack.setCurrentWidget(self.settings_page))
        side_layout.addWidget(settings_btn)
        content_layout.addWidget(self.side_bar, stretch=1)

        # Content Stack holds the main pages
        self.content_stack = QStackedWidget()
        self.home_page = HomePage(self)
        self.profile_page = ProfilePage(self)
        self.gesture_capture_page = GestureCapturePage(self)
        self.settings_page = SettingsPage(self)
        self.content_stack.addWidget(self.home_page)  # index 0: Home
        self.content_stack.addWidget(self.profile_page)  # index 1: Profile view
        self.content_stack.addWidget(self.gesture_capture_page)  # index 2: Gesture Capture
        self.content_stack.addWidget(self.settings_page)  # index 3: Settings
        content_layout.addWidget(self.content_stack, stretch=4)
        main_layout.addWidget(content_widget)

        # Overall stack: login stack vs. main widget
        self.overall_stack = QStackedWidget()
        self.overall_stack.addWidget(self.login_stack)  # index 0: login area (profile selection/creation)
        self.overall_stack.addWidget(self.main_widget)  # index 1: main app
        self.setCentralWidget(self.overall_stack)
        self.setCurrentPage("login")

        self.setWindowTitle("ARTM")
        self.setWindowIcon(QIcon(ICON_PATH))
        self.resize(900, 600)

    def setCurrentPage(self, page_name):
        mapping = {"login": 0, "main": 1}
        if page_name in mapping:
            self.overall_stack.setCurrentIndex(mapping[page_name])

    def on_profile_selected(self, profile_name):
        self.current_profile = profile_name
        self.profile_page.load_profile(profile_name)
        self.home_page.set_profile(profile_name)
        self.setCurrentPage("main")
        self.content_stack.setCurrentWidget(self.home_page)

    def on_profile_created(self):
        # Reload profiles and switch back to profile selection in the login stack.
        self.profile_selection_page.load_profiles()
        self.login_stack.setCurrentIndex(0)
        self.setCurrentPage("login")

    def on_profile_creation_back(self):
        # Switch the login stack back to profile selection.
        self.login_stack.setCurrentIndex(0)
        self.setCurrentPage("login")

    def show_home(self):
        self.content_stack.setCurrentWidget(self.home_page)


if __name__ == "__main__":
    from PyQt5.QtWidgets import QApplication
    import sys

    app = QApplication(sys.argv)

    # Get the absolute path to style.qss
    base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
    qss_path = os.path.join(base_dir, "style.qss")

    try:
        with open(qss_path, "r") as f:
            app.setStyleSheet(f.read())
    except Exception as e:
        print("Error loading style.qss:", e)

    window = BasicFrontendApp()
    window.show()

    sys.exit(app.exec_())