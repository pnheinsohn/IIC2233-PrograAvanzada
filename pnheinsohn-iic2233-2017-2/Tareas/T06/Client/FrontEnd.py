from PyQt5.QtCore import pyqtSignal
from PyQt5.QtGui import QIcon, QPixmap
from PyQt5.QtWidgets import QMainWindow, QWidget, QAction, QApplication, QPushButton, QLineEdit, QLabel, QHBoxLayout
from PyQt5.QtWidgets import QVBoxLayout, QMessageBox, QScrollArea, QDesktopWidget
from PyQt5.QtCore import Qt
import os
from random import shuffle
from Variables import t06_path


class MainWindow(QMainWindow):

    start_editing_signal = pyqtSignal()
    status_bar_signal = pyqtSignal(str)
    main_widget_signal = pyqtSignal(str)
    show_gallery_images_signal = pyqtSignal()
    end_client_connection_signal = pyqtSignal()
    raise_username_pop_up_signal = pyqtSignal(str)
    actualize_commentaries_signal = pyqtSignal(list)
    message_to_server_json_signal = pyqtSignal(dict)
    raise_spectator_mode_pop_up_signal = pyqtSignal()

    def __init__(self, parent, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Widgets
        self.log_in_window = LogInWindow(self, self.message_to_server_json_signal)
        self.dashboard_window = DashboardWindow(self, self.message_to_server_json_signal)
        # Signals
        self.end_client_connection_signal.connect(parent.end_connection)
        self.start_editing_signal.connect(self.dashboard_window.open_image_editor)
        self.message_to_server_json_signal.connect(parent.send_message_to_server_json)
        self.show_gallery_images_signal.connect(self.dashboard_window.show_gallery_images)
        self.raise_username_pop_up_signal.connect(self.log_in_window.raise_username_pop_up)
        self.actualize_commentaries_signal.connect(self.dashboard_window.actualize_commentaries)
        self.raise_spectator_mode_pop_up_signal.connect(self.dashboard_window.raise_spectator_pop_up)
        # Window Structure
        self.setWindowTitle("Prograshop")
        self.file_menu = self.menuBar().addMenu("&File")
        self.status_bar = self.statusBar()
        self.main_menu_action = QAction(QIcon(None), "&M&a&i&n &M&e&n&u", self)
        # Set Up
        self.init_set_up()

    def init_set_up(self):
        # Basics
        self.setObjectName("MainWindow")
        self.setWindowTitle("Prograshop")
        self.setStyleSheet("#MainWindow{background-image: url(" +
                           "{}/Server/Imagenes/Background/show_me_what_you_got.png);"
                           .format(t06_path.replace("\\", "/")) + "}")
        self.showFullScreen()

        exit_action = QAction(QIcon(None), "&E&x&i&t", self)
        exit_action.setShortcut("Ctrl+Q")
        exit_action.setStatusTip("Exit Application")
        exit_action.triggered.connect(self.exit_app)

        self.main_menu_action.setStatusTip("Return To Main Menu")
        self.main_menu_action.triggered.connect(self.return_to_main_menu)

        # Menu Bar
        self.file_menu.addAction(self.main_menu_action)
        self.file_menu.addAction(exit_action)
        self.main_menu_action.setVisible(False)

        # Widget
        self.setCentralWidget(self.log_in_window)
        self.main_widget_signal.connect(self.update_main_widget)

        # Status Bar
        self.status_bar_signal.connect(self.update_status_bar)

    def return_to_main_menu(self):
        if self.dashboard_window.editing:
            self.dashboard_window.editing = False
        self.message_to_server_json_signal.emit({"status": "log_out"})
        self.update_main_widget("LogInWidget")

    def update_main_widget(self, widget):
        if widget == "LogInWidget":
            self.dashboard_window = self.takeCentralWidget()
            self.dashboard_window.close()
            self.log_in_window = LogInWindow(self, self.message_to_server_json_signal)
            self.setCentralWidget(self.log_in_window)
            self.main_menu_action.setVisible(False)
        elif widget == "DashboardWidget":
            self.log_in_window = self.takeCentralWidget()
            self.log_in_window.close()
            self.dashboard_window = DashboardWindow(self, self.message_to_server_json_signal)
            self.start_editing_signal.connect(self.dashboard_window.open_image_editor)
            self.show_gallery_images_signal.connect(self.dashboard_window.show_gallery_images)
            self.actualize_commentaries_signal.connect(self.dashboard_window.actualize_commentaries)
            self.raise_spectator_mode_pop_up_signal.connect(self.dashboard_window.raise_spectator_pop_up)
            self.setCentralWidget(self.dashboard_window)
            self.main_menu_action.setVisible(True)

    def update_status_bar(self, message):
        self.status_bar.showMessage(message)

    def exit_app(self):
        self.end_client_connection_signal.emit()
        QApplication.quit()


class LogInWindow(QWidget):

    username_signal = pyqtSignal(dict)

    def __init__(self, parent, message_to_server_signal, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Labels
        self.title_label = QLabel("Prograshop", self)
        title_label_font = self.title_label.font()
        title_label_font.setBold(True)
        title_label_font.setPointSize(48)
        self.title_label.setFont(title_label_font)
        self.title_label.setStyleSheet("color: darkblue")

        self.username_label = QLabel("Username: ", self)
        username_label_font = self.username_label.font()
        username_label_font.setBold(True)
        username_label_font.setPointSize(12)
        self.username_label.setFont(username_label_font)
        self.username_label.setStyleSheet("color: darkblue")

        # Line Edits
        self.username_line_edit = QLineEdit("", self)
        username_line_edit_font = self.username_line_edit.font()
        username_line_edit_font.setPointSize(10)
        self.username_line_edit.setFont(username_line_edit_font)
        self.username_line_edit.setStyleSheet("color: darkblue; background: transparent")

        # Buttons
        self.username_button = QPushButton("\t\tSend\t\t", self)
        username_button_font = self.username_button.font()
        username_button_font.setBold(True)
        username_button_font.setPointSize(12)
        self.username_button.setFont(username_button_font)
        self.username_button.setStyleSheet(
            "QPushButton{color: darkblue; background: transparent; border: 2px solid darkblue; border-radius: 8px}"
            "QPushButton:pressed{color: #fcf7e3; background-color: darkblue}")
        self.username_button.setStatusTip("Press To Enter")
        self.username_button.clicked.connect(self.handle_button)

        # Signals
        self.message_to_server_signal = message_to_server_signal
        self.init_set_up()

    def init_set_up(self):
        hbox = QHBoxLayout()
        hbox.addStretch(2)
        hbox.addWidget(self.username_label)
        hbox.addWidget(self.username_line_edit)
        hbox.addStretch(2)

        hbox1 = QHBoxLayout()
        hbox1.addStretch(2)
        hbox1.addWidget(self.username_button)
        hbox1.addStretch(2)

        title_hbox = QHBoxLayout()
        title_hbox.addStretch(1)
        title_hbox.addWidget(self.title_label)
        title_hbox.addStretch(1)

        vbox = QVBoxLayout()
        vbox.addLayout(title_hbox)
        vbox.addStretch(1)
        vbox.addLayout(hbox)
        vbox.addLayout(hbox1)
        vbox.addStretch(3)

        self.setLayout(vbox)

    def handle_button(self):
        if len(self.username_line_edit.text()) != 0:
            message = {"status": "check_username", "data": self.username_line_edit.text()}
            self.message_to_server_signal.emit(message)

    def raise_username_pop_up(self, message):
        QMessageBox().critical(self, "Username Error", message, QMessageBox.Ok, QMessageBox.NoButton)


class DashboardWindow(QWidget):

    def __init__(self, parent, message_to_server_signal, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.downloaded_image_number = number_image()
        # Signals
        self.message_to_server_signal = message_to_server_signal
        # Main Menu Buttons
        self.main_menu_button = QPushButton("  Main Menu  ", self)
        self.gallery_button = QPushButton("  Photo Gallery  ", self)
        self.initial_buttons = [self.gallery_button, self.main_menu_button]
        self.main_menu_button.clicked.connect(parent.return_to_main_menu)
        # Window
        self.title_label = QLabel("Prograshop", self)
        # Gallery
        self.gallery_title_label = QLabel("Photo Gallery", self)
        self.gallery_go_back_button = QPushButton("  Go Back  ", self)
        self.gallery_gui = [self.gallery_title_label, self.gallery_go_back_button]
        self.gallery_images = [ImageLabel(self), ImageLabel(self), ImageLabel(self),
                               ImageLabel(self), ImageLabel(self), ImageLabel(self)]
        # Edition Window
        self.editing = False
        self.editing_path = None
        self.image_edit_label = QLabel(self)
        self.editing_title_label = QLabel("Photo Editor", self)
        self.download_button = QPushButton(" Download Photo ", self)
        self.send_changes_button = QPushButton(" Send Changes ", self)
        self.commentaries_button = QPushButton(" Commentaries ", self)
        self.editor_gui = [self.image_edit_label, self.editing_title_label, self.download_button,
                           self.send_changes_button, self.commentaries_button]
        # Spectator Window
        self.spectator_title_label = QLabel("Photo Spectator", self)
        self.spectator_gui = [self.image_edit_label, self.spectator_title_label]
        # Connection
        self.users_scroll = QScrollArea(self)
        self.connected_users_label = QLabel(" Connected Users:", self)
        # Commentaries
        self.commentaries_scroll = QScrollArea(self)
        self.commentaries_line_edit = QLineEdit("", self)
        self.commentaries_send_button = QPushButton(" Send ", self)
        self.commentaries_label = QLabel(" Commentaries:", self)
        self.close_commentaries_button = QPushButton(" Close Commentaries ", self)
        self.commentaries_gui = [self.image_edit_label, self.commentaries_scroll, self.close_commentaries_button,
                                 self.commentaries_line_edit, self.commentaries_send_button]
        # Set Up
        self.init_set_up()

    def init_set_up(self):
        # Buttons
        button_font = self.gallery_button.font()
        button_font.setBold(True)
        button_font.setPointSize(12)
        button_stylesheet = '''
            QPushButton{color: darkblue; background: transparent; border: 2px solid darkblue; border-radius: 8px}
            QPushButton:pressed{color: #fcf7e3; background-color: darkblue}
            '''
        self.gallery_button.setFont(button_font)
        self.gallery_button.setStyleSheet(button_stylesheet)
        self.gallery_button.setStatusTip("Press To See Some Images")
        self.gallery_button.clicked.connect(self.ask_initial_photos)

        self.main_menu_button.setFont(button_font)
        self.main_menu_button.setStatusTip("Return To Main Menu")
        self.main_menu_button.setStyleSheet(button_stylesheet)

        self.gallery_go_back_button.setFont(button_font)
        self.gallery_go_back_button.setStyleSheet(button_stylesheet)
        self.gallery_go_back_button.setStatusTip("Press To Go Back")
        self.gallery_go_back_button.clicked.connect(self.set_main_layout)

        self.download_button.setFont(button_font)
        self.download_button.setStyleSheet(button_stylesheet)
        self.download_button.setStatusTip("Press To Download")
        self.download_button.clicked.connect(self.pre_download_image)

        self.send_changes_button.setFont(button_font)
        self.send_changes_button.setStyleSheet(button_stylesheet)
        self.send_changes_button.setStatusTip("Press To Send Changes")
        self.send_changes_button.clicked.connect(self.send_changes)

        self.commentaries_button.setFont(button_font)
        self.commentaries_button.setStyleSheet(button_stylesheet)
        self.commentaries_button.setStatusTip("Press To See Commentaries")
        self.commentaries_button.clicked.connect(self.open_commentaries)

        self.close_commentaries_button.setFont(button_font)
        self.close_commentaries_button.setStyleSheet(button_stylesheet)
        self.close_commentaries_button.setStatusTip("Press To Close Commentaries")
        self.close_commentaries_button.clicked.connect(self.close_commentaries)

        self.commentaries_send_button.setFont(button_font)
        self.commentaries_send_button.setStyleSheet(button_stylesheet)
        self.commentaries_send_button.setStatusTip("Press To Send Message")
        self.commentaries_send_button.clicked.connect(self.send_commentary_message)
        self.commentaries_send_button.setMaximumWidth(50)
        # Gallery Images
        for qlabel in self.gallery_images:
            qlabel.setStatusTip("Click To Edit")
            qlabel.hide()

        # Gui's
        for gallery_gui in self.gallery_gui:
            gallery_gui.hide()
        for editor_gui in self.editor_gui:
            editor_gui.hide()
        for spectator_gui in self.spectator_gui:
            spectator_gui.hide()
        for commentaries_gui in self.commentaries_gui:
            commentaries_gui.hide()

        # Labels
        title_font = self.title_label.font()
        title_font.setPointSize(48)
        title_font.setBold(True)

        self.title_label.setFont(title_font)
        self.title_label.setStyleSheet("color: darkblue")

        self.gallery_title_label.setFont(title_font)
        self.gallery_title_label.setStyleSheet("color: darkblue")

        self.spectator_title_label.setFont(title_font)
        self.spectator_title_label.setStyleSheet("color: darkblue")

        self.editing_title_label.setFont(title_font)
        self.editing_title_label.setStyleSheet("color: darkblue")

        user_label_font = self.connected_users_label.font()
        user_label_font.setPointSize(10)
        self.connected_users_label.setFont(user_label_font)
        self.connected_users_label.setAlignment(Qt.AlignTop)
        self.connected_users_label.setStyleSheet("color: darkblue")
        self.users_scroll.setWidget(self.connected_users_label)
        self.users_scroll.setWidgetResizable(True)
        self.users_scroll.setFixedHeight(170)
        self.users_scroll.setFixedWidth(150)
        self.users_scroll.setStyleSheet("background-color: transparent")

        self.commentaries_label.setFont(user_label_font)
        self.commentaries_label.setAlignment(Qt.AlignTop)
        self.commentaries_label.setStyleSheet("color: darkblue")
        self.commentaries_scroll.setWidget(self.commentaries_label)
        self.commentaries_scroll.setWidgetResizable(True)
        self.commentaries_scroll.setFixedHeight(270)
        self.commentaries_scroll.setFixedWidth(150)
        self.commentaries_scroll.setStyleSheet("background-color: transparent")
        self.commentaries_line_edit.setFont(user_label_font)
        self.commentaries_line_edit.setStyleSheet("color: darkblue; background-color: transparent")
        self.commentaries_line_edit.setMaximumWidth(150)

        # Layouts
        buttons_vbox = QVBoxLayout()
        buttons_vbox.addStretch(1)
        buttons_vbox.addWidget(self.gallery_button)
        buttons_vbox.addWidget(self.main_menu_button)
        buttons_vbox.addStretch(3)

        central_hbox = QHBoxLayout()
        central_hbox.addStretch(4)
        central_hbox.addLayout(buttons_vbox)
        central_hbox.addStretch(5)

        top_hbox = QHBoxLayout()
        top_hbox.addStretch(8)
        top_hbox.addWidget(self.title_label)
        top_hbox.addWidget(self.gallery_title_label)
        top_hbox.addWidget(self.editing_title_label)
        top_hbox.addWidget(self.spectator_title_label)
        top_hbox.addStretch(9)
        top_hbox.addWidget(self.gallery_go_back_button)
        top_hbox.addStretch(1)

        commentaries_hbox = QHBoxLayout()
        commentaries_hbox.addWidget(self.commentaries_line_edit)
        commentaries_hbox.addWidget(self.commentaries_send_button)

        top_left_vbox = QVBoxLayout()
        top_left_vbox.addWidget(self.users_scroll)
        top_left_vbox.addStretch(1)
        top_left_vbox.addWidget(self.commentaries_scroll)
        top_left_vbox.addLayout(commentaries_hbox)
        top_left_vbox.addWidget(self.close_commentaries_button)
        top_left_vbox.addWidget(self.send_changes_button)
        top_left_vbox.addWidget(self.commentaries_button)
        top_left_vbox.addWidget(self.download_button)
        top_left_vbox.addStretch(3)

        top_right_vbox = QVBoxLayout()
        top_right_vbox.addLayout(top_hbox)
        top_right_vbox.addStretch(1)
        top_right_vbox.addLayout(central_hbox)
        top_right_vbox.addStretch(2)

        main_hbox = QHBoxLayout()
        main_hbox.addLayout(top_left_vbox)
        main_hbox.addLayout(top_right_vbox)

        self.setLayout(main_hbox)

    def set_main_layout(self):
        if self.editing:
            self.editing = False
            index = int("".join([string for string in self.editing_path if string.isdigit()]))
            self.message_to_server_signal.emit({"status": "stop_editing", "data": index})
        self.title_label.show()
        for commentaries_gui in self.commentaries_gui:
            commentaries_gui.hide()
        for editor_gui in self.editor_gui:
            editor_gui.hide()
        for spectator_gui in self.spectator_gui:
            spectator_gui.hide()
        for gallery_gui in self.gallery_gui:
            gallery_gui.hide()
        for qlabel in self.gallery_images:
            qlabel.hide()
        for button in self.initial_buttons:
            button.show()

    def set_gallery_layout(self):
        self.title_label.hide()
        self.spectator_title_label.hide()
        for button in self.initial_buttons:
            button.hide()
        for editor_gui in self.editor_gui:
            editor_gui.hide()
        for gallery_gui in self.gallery_gui:
            gallery_gui.show()

    def set_pre_edition_layout(self, path):
        self.editing_path = path
        self.image_edit_label = EditLabel(self.editing_path, self)
        self.editor_gui[0] = self.image_edit_label
        self.spectator_gui[0] = self.image_edit_label
        self.commentaries_gui[0] = self.image_edit_label
        for gallery_gui in self.gallery_gui:
            if gallery_gui != self.gallery_go_back_button:
                gallery_gui.hide()
        for qlabel in self.gallery_images:
            qlabel.hide()
        index = int("".join([string for string in self.editing_path if string.isdigit()]))
        self.message_to_server_signal.emit({"status": "available_for_editing", "data": index})

    def set_editor_layout(self):
        self.editing = True
        for commentaries_gui in self.commentaries_gui:
            commentaries_gui.hide()
        for editor_gui in self.editor_gui:
            editor_gui.show()

    def set_commentaries_layout(self):
        for editor_gui in self.editor_gui:
            editor_gui.hide()
        for commentaries_gui in self.commentaries_gui:
            commentaries_gui.show()
        if self.editing:
            self.editing_title_label.show()
        else:
            self.spectator_title_label.show()

    def set_spectator_layout(self):
        for commentaries_gui in self.commentaries_gui:
            commentaries_gui.hide()
        for editor_gui in self.editor_gui:
            editor_gui.hide()
        for spectator_gui in self.spectator_gui:
            spectator_gui.show()
        self.commentaries_button.show()

    def ask_initial_photos(self):
        self.message_to_server_signal.emit({"status": "ask_initial_photos"})

    def show_online_clients(self, client_usernames):
        string = " Connected Users:"
        for i, username in enumerate(client_usernames):
            string += "\n    {}. {}".format(i + 1, username)
        self.connected_users_label.setText(string)
        self.connected_users_label.setStyleSheet("color: darkblue")

    def show_gallery_images(self):
        self.set_gallery_layout()
        for root, dirs, files in os.walk("Imagenes"):
            shuffle(files)
            for file, qlabel in zip(files, self.gallery_images):
                qlabel.path = os.path.join(root, file)
                pixmap = QPixmap(qlabel.path)
                qlabel.setPixmap(pixmap.scaled(pixmap.width() / 2, pixmap.height() / 2))
                qlabel.resize(qlabel.sizeHint())

        self.gallery_images = sorted(self.gallery_images, key=lambda pixmap: pixmap.width(), reverse=True)
        for i, qlabel in enumerate(self.gallery_images):
            if i == 0:
                qlabel.move(200, 120)
            elif i < 3:
                qlabel.move(self.gallery_images[i - 1].pos().x() + self.gallery_images[i - 1].width() + 30, 120)
            else:
                qlabel.move(self.gallery_images[i - 3].pos().x(),
                            max(self.gallery_images[0:3], key=lambda image: image.height()).pos().y() +
                            max(self.gallery_images[0:3], key=lambda image: image.height()).height() + 30)
            qlabel.show()

    def open_image_editor(self):
        self.set_editor_layout()

    def open_image_spectator(self):
        self.set_spectator_layout()

    def raise_spectator_pop_up(self):
        spectator = QMessageBox().question(self, "Photo is locked", "Do you want to enter spectator mode?",
                                           QMessageBox.Yes, QMessageBox.No)
        if spectator == QMessageBox.Yes:
            self.open_image_spectator()
        else:
            self.show_gallery_images()

    def pre_download_image(self):
        self.send_changes()
        with open("Imagenes/downloaded_image_{}.png".format(next(self.downloaded_image_number)), "wb") as image:
            with open(self.editing_path, "rb") as image_2:
                image.write(image_2.read())

    def send_changes(self):
        pass

    def open_commentaries(self):
        self.set_commentaries_layout()
        index = int("".join([string for string in self.editing_path if string.isdigit()]))
        self.message_to_server_signal.emit({"status": "get_commentaries", "data": index})

    def close_commentaries(self):
        if self.editing:
            self.set_editor_layout()
        else:
            self.set_spectator_layout()

    def actualize_commentaries(self, commentaries):
        index = int("".join([string for string in self.editing_path if string.isdigit()]))
        commentary = commentaries[index][1]
        self.commentaries_label.setText("Commentaries:\n\n" + commentary)

    def send_commentary_message(self):
        if self.commentaries_line_edit.text() == "":
            return
        string = self.commentaries_line_edit.text()
        index = int("".join([string for string in self.editing_path if string.isdigit()]))
        self.message_to_server_signal.emit({"status": "new_commentary_message", "data": [index, string]})
        self.commentaries_line_edit.setText("")


class ImageLabel(QLabel):

    set_editor_window_signal = pyqtSignal(str)

    def __init__(self, parent=None):
        super().__init__(parent)
        self.set_editor_window_signal.connect(parent.set_pre_edition_layout)

    def mousePressEvent(self, QMouseEvent):
        self.set_editor_window_signal.emit(self.path)


class EditLabel(QLabel):

    def __init__(self, path, parent=None):
        super().__init__(parent)
        self.setPixmap(QPixmap(path))
        self.resize(self.sizeHint())
        self.setAlignment(Qt.AlignCenter)
        self.move((QDesktopWidget().availableGeometry().width() - self.geometry().width()) / 2,
                  (QDesktopWidget().availableGeometry().height() - self.geometry().height()) / 2)
        self.setScaledContents(True)


def number_image():
    i = 0
    while True:
        yield i
        i += 1
