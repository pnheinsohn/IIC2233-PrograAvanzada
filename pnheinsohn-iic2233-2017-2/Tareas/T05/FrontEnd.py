import sys
from os import path
from BackEnd import GameManager
from Events import MovePlayerEvent, RotatePlayerEvent
from PyQt5.QtCore import pyqtSignal, Qt
from PyQt5.QtGui import QIcon, QPixmap, QTransform
from PyQt5.QtWidgets import QWidget, QApplication, QMainWindow, QLabel, QHBoxLayout, QVBoxLayout, QPushButton, QAction
from PyQt5.QtWidgets import QProgressBar, QLineEdit
from PyQt5.Qt import QTest


class MainWindow(QMainWindow):

    # FrontEnd Signals
    hide_store_signal = pyqtSignal()
    status_bar_signal = pyqtSignal(str)
    background_signal = pyqtSignal(str)
    main_widget_signal = pyqtSignal(str)
    show_store_signal = pyqtSignal(bool)

    # BackEnd Signals
    stop_moving_signal = pyqtSignal()
    kill_enemy_signal = pyqtSignal(int)
    start_game_signal = pyqtSignal(bool)
    pause_game_signal = pyqtSignal(bool)
    move_entity_signal = pyqtSignal(MovePlayerEvent)
    check_store_item_signal = pyqtSignal(str, str, int)  # item_name, sprite, index
    rotate_entity_signal = pyqtSignal(RotatePlayerEvent)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.setObjectName("MainWidget")
        self.last_central_widget = None
        self.player_image = QLabel(self)
        self.player_image.setAlignment(Qt.AlignCenter)
        self.player_image.hide()
        self.player_life = QProgressBar(self)
        self.player_life.setMaximumSize(100, 15)
        self.player_life.setAlignment(Qt.AlignCenter)
        self.life_font = self.player_life.font()
        self.life_font.setBold(True)
        self.player_life.setFont(self.life_font)
        self.player_life.hide()
        self.paused = False
        self.store_is_shown = False
        self.init_GUI()

    def init_GUI(self):
        # Basics
        self.setWindowTitle('DCCells')
        self.setStyleSheet("#MainWidget{background-image: url(Assets/Fondos/Etapa0);}")
        self.setGeometry(280, 150, 1360, 768)

        # Actions
        exit_action = QAction(QIcon(None), "&E&x&i&t", self)
        exit_action.setShortcut("Ctrl+Q")
        exit_action.setStatusTip("Exit Application")
        exit_action.triggered.connect(self.exit_app)

        self.main_menu_action = QAction(QIcon(None), "&M&a&i&n &M&e&n&u", self)
        self.main_menu_action.setStatusTip("Return To Main Menu")
        self.main_menu_action.triggered.connect(self.go_main_menu)

        # Menu Bar
        self.file_menu = self.menuBar().addMenu("&File")
        self.file_menu.addAction(self.main_menu_action)
        self.file_menu.addAction(exit_action)
        self.main_menu_action.setVisible(False)

        # Main Widget & Game Widget
        self.main_menu_widget = PreGameWidget(self.main_widget_signal, self.background_signal)
        self.game_widget = GameWidget(self.player_image, self.player_life, self.main_widget_signal,
                                      self.start_game_signal, self.background_signal, self.hide_store_signal,
                                      self.check_store_item_signal)
        self.setCentralWidget(self.main_menu_widget)
        self.main_widget_signal.connect(self.update_main_widget)

        # Store
        self.show_store_signal.connect(self.game_widget.show_store_method)
        self.hide_store_signal.connect(self.change_store_boolean)

        # Status Bar
        self.status_bar = self.statusBar()
        self.status_bar_signal.connect(self.update_status_bar)
        self.background_signal.connect(self.setStyleSheet)

        # BackEnd & BackEnd Signals
        self.game_manager = GameManager(self.game_widget, self.check_store_item_signal)
        self.start_game_signal.connect(self.game_manager.start)
        self.pause_game_signal.connect(self.game_manager.pause)
        self.move_entity_signal.connect(self.game_manager.move_entity)
        self.stop_moving_signal.connect(self.game_manager.stop_entity)
        self.rotate_entity_signal.connect(self.game_manager.rotate_entity)

    def update_status_bar(self, message):
        self.status_bar.showMessage(message)

    def go_main_menu(self):
        self.game_widget.go_to_main_menu()

    def update_main_widget(self, message):
        if message == "GameWidget":
            self.main_menu_widget = self.takeCentralWidget()
            self.main_menu_widget.close()
            self.setStyleSheet("#MainWidget{background-image: url(Assets/Fondos/Etapa1)}")
            self.setCentralWidget(self.game_widget)
            self.player_image.show()
            self.player_life.show()
            self.start_game_signal.emit(True)
            self.main_menu_action.setVisible(True)
        elif message == "MainMenuWidget":
            self.start_game_signal.emit(False)
            self.game_widget = self.takeCentralWidget()
            self.player_image.hide()
            self.player_life.hide()
            self.game_widget.close()
            self.setStyleSheet("#MainWidget{background-image: url(Assets/Fondos/Etapa0)}")
            self.setCentralWidget(self.main_menu_widget)
            self.main_menu_action.setVisible(False)

    def exit_app(self):
        self.start_game_signal.emit(False)
        QApplication.quit()

    def keyPressEvent(self, event):
        ctrl = event.modifiers() & Qt.ControlModifier
        if self.centralWidget() == self.game_widget:
            if event.key() == Qt.Key_P and ctrl:
                self.paused = not self.paused
                if self.paused:
                    self.status_bar_signal.emit("Paused")
                else:
                    self.status_bar_signal.emit("")
                self.pause_game_signal.emit(self.paused)
            elif event.key() == Qt.Key_T and ctrl:
                self.store_is_shown = not self.store_is_shown
                if self.store_is_shown:
                    self.status_bar_signal.emit("Store")
                    self.pause_game_signal.emit(True)
                else:
                    self.status_bar_signal.emit("")
                    self.pause_game_signal.emit(False)
                self.show_store_signal.emit(self.store_is_shown)
            elif (event.key() == Qt.Key_Up or event.key() == Qt.Key_W) and not self.paused:
                self.move_entity_signal.emit(MovePlayerEvent("Up"))
            elif (event.key() == Qt.Key_Down or event.key() == Qt.Key_S) and not self.paused:
                self.move_entity_signal.emit(MovePlayerEvent("Down"))
            elif (event.key() == Qt.Key_Right or event.key() == Qt.Key_D) and not self.paused:
                self.rotate_entity_signal.emit(RotatePlayerEvent("Right"))
            elif (event.key() == Qt.Key_Left or event.key() == Qt.Key_A) and not self.paused:
                self.rotate_entity_signal.emit(RotatePlayerEvent("Left"))

    def keyReleaseEvent(self, event):
        if self.centralWidget() == self.game_widget and not self.paused:
            if event.key() == Qt.Key_Up or event.key() == Qt.Key_Down \
                    or event.key() == Qt.Key_W or event.key() == Qt.Key_S:
                self.stop_moving_signal.emit()

    def change_store_boolean(self):
        self.store_is_shown = False


class PreGameWidget(QWidget):

    def __init__(self, main_widget_signal, background_signal, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.background_signal = background_signal
        self.main_widget_signal = main_widget_signal
        self.ranking = QWidget(self)
        self.init_GUI()

    def init_GUI(self):
        # Labels
        self.game_title = QLabel("                         DCCELLS", self)
        self.game_title.setStyleSheet("border: 2px solid black; border-radius: 8px; background-color: white")
        self.game_title.setFixedSize(200, 50)
        # Buttons
        self.start_button = QPushButton("Start", self)
        self.start_button.setFixedSize(200, 30)
        self.start_button.setStyleSheet("border: 2px solid black; border-radius: 8px; background-color: white")
        self.start_button.setStatusTip("Press To Start Game")
        self.start_button.clicked.connect(self.start)
        self.ranking_button = QPushButton("Ranking", self)
        self.ranking_button.setFixedSize(200, 30)
        self.ranking_button.setStyleSheet("border: 2px solid black; border-radius: 8px; background-color: white")
        self.ranking_button.setStatusTip("Press To Check High Scores")
        self.ranking_button.clicked.connect(self.show_ranking)
        self.exit_button = QPushButton("Exit", self)
        self.exit_button.setFixedSize(200, 30)
        self.exit_button.setStyleSheet("border: 2px solid black; border-radius: 8px; background-color: white")
        self.exit_button.setStatusTip("Press To Exit Game")
        self.exit_button.clicked.connect(QApplication.quit)

        self.vbox = QVBoxLayout()
        self.vbox.addStretch(2)
        self.vbox.addWidget(self.game_title)
        self.vbox.addStretch(2)
        self.vbox.addWidget(self.start_button)
        self.vbox.addWidget(self.ranking_button)
        self.vbox.addWidget(self.exit_button)
        self.vbox.addStretch(10)

        self.hbox = QHBoxLayout()
        self.hbox.addStretch(1)
        self.hbox.addLayout(self.vbox)
        self.hbox.addStretch(1)

        self.setLayout(self.hbox)

        # Ranking
        self.ranking.setGeometry(300, 300, 100, 400)
        self.ranking.setStyleSheet("border: 2px solid black; border-radius: 8px; background-color: white")
        self.ranking_label = QLabel("", self.ranking)
        font = self.ranking_label.font()
        font.setBold(True)
        self.ranking_label.setFont(font)
        self.ranking.hide()

    # Button Functions
    def start(self):
        self.main_widget_signal.emit("GameWidget")

    def show_ranking(self):
        string = ""
        if path.isfile("ranking.csv"):
            with open("ranking.csv", "r", encoding="utf-8") as ranks:
                for i, row in enumerate(ranks):
                    if i != 0 and i < 11:
                        name_score = row.strip("\n").split(",")
                        string += "{})\t{}:\t{}".format(i, name_score[0], name_score[1])
        self.ranking_label.setText(string)
        self.ranking.show()


class GameWidget(QWidget):

    kill_enemy_signal = pyqtSignal(int)  # index

    def __init__(self, player_image, player_life, main_widget_signal, start_game_signal, background_signal,
                 hide_store_signal, check_store_item_signal, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Signals
        self.start_game_signal = start_game_signal
        self.background_signal = background_signal
        self.hide_store_signal = hide_store_signal
        self.main_widget_signal = main_widget_signal
        self.check_store_item = check_store_item_signal
        # Player
        self.player_label = player_image
        self.player_life = player_life
        self.player_exp = QProgressBar(self)
        self.player_level = QLabel("Level 1", self)
        self.player_score = QLabel("  Score: 0", self)
        self.player_width_scale = 31
        self.player_height_scale = 31
        self.actual_player_rotation = 0
        self.actual_player_sprite = None
        # Enemies
        self.enemies_labels = []
        self.enemies_progress_bars = []
        # Items
        self.lives_labels = []
        self.points_labels = []
        self.bomb = QLabel(self)
        self.bomb.setAlignment(Qt.AlignCenter)
        self.safe_zone = QLabel(self)
        self.safe_zone.setAlignment(Qt.AlignCenter)
        # Pause Buttons
        self.store_button = QPushButton("Store", self)
        self.main_menu_button = QPushButton("Main Menu", self)
        self.exit_button = QPushButton("Exit", self)
        self.inventory = InventoryLabel(self)
        # Store
        self.store = Store(self)
        # GUI
        self.ask_name = QLabel("", self)
        self.count_down = QLabel(self)
        self.input_score = QLineEdit("", self)
        self.boton = QPushButton("Enviar", self)
        self.init_GUI()
        # Variable
        self.high_score = 0

    def init_GUI(self):
        # Pause Buttons
        self.store_button.setFixedSize(200, 30)
        self.store_button.setStyleSheet("border: 2px solid black; border-radius: 8px; background-color: white")
        self.store_button.setStatusTip("Press To Check The Store")
        self.store_button.clicked.connect(self.show_store)
        self.main_menu_button.setFixedSize(200, 30)
        self.main_menu_button.setStyleSheet("border: 2px solid black; border-radius: 8px; background-color: white")
        self.main_menu_button.setStatusTip("Press To End Game")
        self.main_menu_button.clicked.connect(self.go_to_main_menu)
        self.exit_button.setFixedSize(200, 30)
        self.exit_button.setStyleSheet("border: 2px solid black; border-radius: 8px; background-color: white")
        self.exit_button.setStatusTip("Press To Exit Game")
        self.exit_button.clicked.connect(self.exit_game)
        self.store_button.move(575, 200)
        self.main_menu_button.move(575, 250)
        self.exit_button.move(575, 300)
        self.store_button.hide()
        self.main_menu_button.hide()
        self.exit_button.hide()
        # Store
        self.store.setGeometry(450, 200, 500, 300)
        self.store.setStyleSheet("background: white; border-radius: 8px; border: 4px solid black;")
        self.store.hide_all()
        # Inventory
        self.inventory.setPixmap(QPixmap("Assets/Store/inventory").scaled(250, 45))
        self.inventory.move(50, 680)
        self.inventory.show()
        # Player Image
        self.player_label.setPixmap(QPixmap(self.actual_player_sprite))
        self.player_label.show()
        # Player Life
        self.change_player_hp(100)
        self.player_life.show()
        # Player Level
        level_font = self.player_level.font()
        level_font.setBold(True)
        self.player_level.setFont(level_font)
        self.player_level.setStyleSheet("border: 2px solid black; border-radius: 4px; background-color: white")
        self.player_level.setGeometry(1172, 700, 50, 25)
        # Player Exp
        exp_font = self.player_exp.font()
        exp_font.setBold(True)
        self.player_exp.setFont(exp_font)
        self.player_exp.setGeometry(1220, 700, 125, 25)
        self.change_player_exp(0, 1)
        # Player Score
        self.input_score.hide()
        self.ask_name.hide()
        self.boton.hide()
        score_font = self.player_score.font()
        score_font.setBold(True)
        self.player_score.setFont(score_font)
        self.player_score.setGeometry(1220, 10, 100, 30)
        self.player_score.setStyleSheet("border: 2px solid black; border-radius: 4px; background-color: white")

    # Game Functions
    def start_count_down(self, sprite, boolean):
        if boolean:
            self.count_down.hide()
            self.count_down.setPixmap(QPixmap(sprite))
            self.count_down.setGeometry(640, 100, 240, 480)
            self.count_down.show()
        else:
            self.count_down.hide()

    def change_stage(self, number):
        self.background_signal.emit(
            "#MainWidget{" + "background-image: url(Assets/Fondos/Etapa{})".format(number) + "}")

    def win(self):
        pass

    def show_store(self):
        self.show_store_method(True)

    def hide_store(self):
        self.show_store_method(False)
        self.hide_store_signal.emit()

    def show_store_method(self, boolean):
        if boolean:
            self.store.show_all()
        else:
            self.store.hide_all()

    def exit_game(self):
        self.start_game_signal.emit(False)
        QApplication.quit()

    def go_to_main_menu(self):
        self.change_player_hp(100)
        self.store_button.hide()
        self.main_menu_button.hide()
        self.exit_button.hide()
        self.inventory.hide()
        self.player_label.hide()
        self.player_life.hide()
        self.start_game_signal.emit(False)
        self.wait_to_start_again("Wait 30 Seconds to start again...")
        self.main_widget_signal.emit("MainMenuWidget")

    def end_game(self):
        self.change_player_hp(100)
        self.inventory.hide()
        self.player_life.hide()
        self.player_label.hide()
        self.wait_to_start_again("Wait 30 Seconds to start again...")
        self.main_widget_signal.emit("MainMenuWidget")

    def wait_to_start_again(self, string):
        waiting = QLabel(string, self)
        waiting.setGeometry(575, 240, 200, 50)
        waiting.setStyleSheet("border: 2px solid black; border-radius: 8px; background-color: white")
        waiting_font = waiting.font()
        waiting_font.setBold(True)
        waiting.setFont(waiting_font)
        waiting.show()
        QTest.qWait(30000)
        waiting.close()

    def show_paused_buttons(self, boolean):
        if boolean:
            self.store_button.show()
            self.main_menu_button.show()
            self.exit_button.show()
        else:
            self.store_button.hide()
            self.main_menu_button.hide()
            self.exit_button.hide()

    def mouse_released(self, x, y, sprite, name):
        selected_slot = sorted(self.inventory.slots,
                               key=lambda slot: ((slot.pos().x() + self.inventory.pos().x() - x) ** 2 +
                                                 (slot.pos().y() + self.inventory.pos().y() - y) ** 2) ** (1 / 2))
        if ((selected_slot[0].pos().x() + self.inventory.pos().x() - x) ** 2 + (
                        selected_slot[0].pos().y() + self.inventory.pos().y() - y) ** 2) ** (1 / 2) <= 30:
            self.check_store_item.emit(name, sprite, self.inventory.slots.index(selected_slot[0]))

    def change_player_inventory(self, sprite, index):
        self.inventory.slots[index].setPixmap(QPixmap(sprite).scaled(40, 40))

    def ask_for_name(self, score):
        self.player_label.hide()
        self.player_life.hide()
        self.high_score = score
        self.change_stage(7)
        self.ask_name.setText("Incredible! You've Got {} DCCELLS POINTS, Keep On It!\n\t\tInsert Name: ".format(score))
        font = self.ask_name.font()
        font.setBold(True)
        self.ask_name.setFont(font)
        self.ask_name.setStyleSheet("border: 2px solid black; border-radius: 8px; background-color: white")
        self.ask_name.show()
        self.ask_name.move(520, 300)
        self.input_score.setGeometry(600, 340, 100, 25)
        self.input_score.setStyleSheet("border: 2px solid black; border-radius: 8px; background-color: white")
        self.input_score.show()
        self.boton.setGeometry(710, 340, 60, 25)
        self.boton.setFont(font)
        self.boton.setStyleSheet("border: 2px solid black; border-radius: 8px; background-color: white")
        self.boton.clicked.connect(self.save_scores)
        self.boton.show()

    def save_scores(self):
        string = "id,score\n"
        if path.isfile("ranking.csv"):
            with open("ranking.csv", "r", encoding="utf-8") as ranking:
                checked = False
                for row in ranking:
                    if row == "id,score\n":
                        continue
                    if not (self.is_high_score(row) and checked):
                        string += "{},{}\n".format(self.input_score.text(), self.high_score)
                        checked = True
                    string += row
        else:
            string += "{},{}\n".format(self.input_score.text(), self.high_score)
        with open("ranking.csv", "w", encoding="utf-8") as ranking:
            ranking.write(string)
        self.input_score.hide()
        self.ask_name.hide()
        self.boton.hide()
        self.end_game()

    def is_high_score(self, row):
        high_score = row.strip("\n").split(",")[1]
        if float(high_score) >= self.high_score:
            return True
        return False

    # Player Functions
    def hide_sprite(self, boolean):
        if boolean:
            self.player_label.hide()
        else:
            self.player_label.show()

    def change_player_sprite(self, sprite):
        self.actual_player_sprite = sprite
        pixmap = QPixmap(self.actual_player_sprite).scaled(self.player_width_scale, self.player_height_scale)
        transform = QTransform().rotate(self.actual_player_rotation)
        pixmap = pixmap.transformed(transform, Qt.SmoothTransformation)
        self.player_label.setPixmap(pixmap)
        self.player_label.resize(self.player_width_scale, self.player_height_scale)

    def move_player(self, x, y):
        self.player_label.move(x, y)
        self.player_life.move(x + self.player_width_scale / 2 - 46.5, y + self.player_height_scale)

    def rotate_player(self, rot):
        self.actual_player_rotation = rot
        self.change_player_sprite(self.actual_player_sprite)

    def change_player_hp(self, hp_percentage):
        self.player_life.setFormat("%.01f%%" % hp_percentage)
        self.player_life.setValue(hp_percentage)
        if hp_percentage == 0:
            self.player_life.setStyleSheet(
                "QProgressBar{background-color: silver; text-align: center; border: 2px solid black}")
        elif hp_percentage <= 20:
            self.player_life.setStyleSheet(
                "QProgressBar{background-color: orange; text-align: center; border: 2px solid black}"
                "QProgressBar::chunk{background-color: yellow}")
        else:
            self.player_life.setStyleSheet(
                "QProgressBar{background-color: darkred; text-align: center; border: 2px solid black}"
                "QProgressBar::chunk{background-color: red}")

    def change_player_exp(self, exp_percentage, level):
        self.player_exp.setFormat("%.01f%%" % exp_percentage)
        self.player_exp.setValue(exp_percentage)
        if exp_percentage == 0:
            self.player_level.setText("Level {}".format(level))
        self.player_exp.setStyleSheet(
            "QProgressBar{background-color: white; text-align: center; border: 2px solid black; border-radius: 4px}"
            "QProgressBar::chunk{background-color: grey}")

    def change_score(self, score):
        self.player_score.setText("     Score: {}".format(score))

    def change_player_size(self, size):
        if size == 1:
            self.change_player_hp(100)
        self.player_height_scale = 15.5 * size
        self.player_width_scale = 15.5 * size

    def change_player_score(self, score):
        self.player_score.setText("    Score: {}".format(score))

    # Enemy Functions
    def new_enemy(self):
        # Enemy
        enemy = QLabel(self)
        enemy.setAlignment(Qt.AlignCenter)
        enemy.show()
        self.enemies_labels.append(enemy)
        # Enemy's life
        enemy_life = QProgressBar(self)
        enemy_life.setMaximumSize(100, 15)
        enemy_life.setAlignment(Qt.AlignCenter)
        life_font = enemy_life.font()
        life_font.setBold(True)
        enemy_life.setFont(life_font)
        enemy_life.show()
        self.enemies_progress_bars.append(enemy_life)
        self.change_enemy_hp(-1, 100)

    def change_enemy_label(self, index, size, x, y, rot, sprite):
        try:
            enemy = self.enemies_labels[index]
            enemy_life = self.enemies_progress_bars[index]
            pixmap = QPixmap(sprite).scaled(15.5 * size, 15.5 * size)
            transform = QTransform().rotate(rot)
            pixmap = pixmap.transformed(transform, Qt.SmoothTransformation)
            enemy.setPixmap(pixmap)
            enemy.resize(15.5 * size, 15.5 * size)
            enemy.move(x, y)
            enemy_life.move(x + 15.5 * size / 2 - 46.5, y + 15.5 * size)
        except IndexError as err:
            print(err)

    def change_enemy_hp(self, index, hp_percentage):
        try:
            enemy_life = self.enemies_progress_bars[index]
            enemy_life.setFormat("%.01f%%" % hp_percentage)
            enemy_life.setValue(hp_percentage)
            if hp_percentage == 0:
                enemy_life.setStyleSheet(
                    "QProgressBar{background-color: silver; text-align: center; border: 2px solid black}")
                self.kill_enemy(index)
            elif hp_percentage <= 20:
                enemy_life.setStyleSheet(
                    "QProgressBar{background-color: orange; text-align: center; border: 2px solid black}"
                    "QProgressBar::chunk{background-color: yellow}")
            else:
                enemy_life.setStyleSheet(
                    "QProgressBar{background-color: darkred; text-align: center; border: 2px solid black}"
                    "QProgressBar::chunk{background-color: red}")
        except IndexError as err:
            print(err)

    def kill_enemy(self, index):
        try:
            enemy = self.enemies_labels.pop(index)
            enemy_life = self.enemies_progress_bars.pop(index)
            enemy.close()
            enemy_life.close()
        except IndexError as err:
            print(err)

    def kill_all_enemies(self):
        for enemy in self.enemies_labels:
            enemy.close()
        self.enemies_labels = []
        for enemy_life in self.enemies_progress_bars:
            enemy_life.close()
        self.enemies_progress_bars = []
        for life in self.lives_labels:
            life.close()
        self.lives_labels = []
        for point in self.points_labels:
            point.close()
        self.points_labels = []
        self.safe_zone.close()

    # Item Functions
    def new_bomb(self, x, y, sprite):
        self.bomb.setPixmap(QPixmap(sprite))
        self.bomb.resize(62, 62)
        self.bomb.move(x, y)
        self.bomb.show()

    def explode_bomb(self, sprite):
        self.bomb.setPixmap(QPixmap(sprite))
        self.bomb.resize(62, 62)
        QTest.qWait(500)
        self.bomb.close()

    def new_safe_zone(self, x, y):
        self.player_label.show()
        self.safe_zone.setPixmap(QPixmap("Assets/Items/safe_zone.png"))
        self.safe_zone.resize(139.5, 139.5)
        self.safe_zone.move(x, y)
        self.safe_zone.show()

    def new_life(self, x, y):
        new_life = QLabel(self)
        new_life.setPixmap(QPixmap("Assets/Items/vida_extra.png").scaled(31, 31))
        new_life.resize(31, 31)
        new_life.move(x, y)
        new_life.show()
        self.lives_labels.append(new_life)

    def kill_life(self, index):
        try:
            life = self.lives_labels.pop(index)
            life.close()
            self.change_player_hp(100)
        except IndexError as err:
            print(err)

    def new_point(self, x, y):
        new_point = QLabel(self)
        new_point.setPixmap(QPixmap("Assets/Items/puntaje_extra.png").scaled(15.5, 15.5))
        new_point.resize(15.5, 15.5)
        new_point.move(x, y)
        new_point.show()
        self.points_labels.append(new_point)

    def kill_point(self, index):
        try:
            point = self.points_labels.pop(index)
            point.close()
        except IndexError as err:
            print(err)


class InventoryLabel(QLabel):

    def __init__(self, parent=None):
        super().__init__(parent)
        self.slots = [QLabel(self), QLabel(self), QLabel(self), QLabel(self), QLabel(self), QLabel(self)]
        for i, slot in enumerate(self.slots):
            slot.setPixmap(QPixmap("Assets/Store/score_icon.png").scaled(40, 40))
            slot.move(42 * i, self.pos().y() + 2)
            slot.show()


class Store(QLabel):

    def __init__(self, parent=None):
        super().__init__(parent)
        # Exit Store
        self.exit_store = QPushButton("  X  ", parent)
        self.exit_store.move(900, 210)
        self.exit_store.setStyleSheet("border: 2px solid black; border-radius: 8px; background-color: red")
        self.exit_store.clicked.connect(parent.hide_store)
        # Title
        self.title = QLabel("DCCELLS STORE (Coin: Score)", parent)
        font = self.title.font()
        font.setBold(True)
        self.title.setFont(font)
        self.title.setStyleSheet("border: 2px solid black; border-radius: 8px; background-color: white")
        self.title.move(610, 220)
        # Names
        self.name_speed = QLabel("Speed UP\n(250 score points)", parent)
        self.name_speed.setStyleSheet("border: 2px solid black; border-radius: 8px; background-color: white")
        self.name_speed.move(500, 280)
        self.name_attack = QLabel("Attack Speed UP\n(500 score points)", parent)
        self.name_attack.setStyleSheet("border: 2px solid black; border-radius: 8px; background-color: white")
        self.name_attack.move(650, 280)
        self.name_life = QLabel("Life UP\n(750 score points)", parent)
        self.name_life.setStyleSheet("border: 2px solid black; border-radius: 8px; background-color: white")
        self.name_life.move(800, 280)
        font = self.name_speed.font()
        font.setBold(True)
        self.name_speed.setFont(font)
        self.name_attack.setFont(font)
        self.name_life.setFont(font)
        # Images
        self.speed_up = ImageLabel("speed_up", "Assets/Store/store_speed.png", parent)
        self.speed_up.move(520, 320)
        self.speed_attack_up = ImageLabel("speed_attack_up", "Assets/Store/store_attack.png", parent)
        self.speed_attack_up.move(670, 320)
        self.life_up = ImageLabel("life_up", "Assets/Store/store_life.png", parent)
        self.life_up.move(820, 320)
        # Tips
        self.speed_up.setStatusTip("Buy (Drag and Drop To Inventory) For More Speed")
        self.speed_attack_up.setStatusTip("Buy (Drag and Drop To Inventory) For More Attack Speed")
        self.life_up.setStatusTip("Buy (Drag and Drop To Inventory) For More Life")

    def hide_all(self):
        self.hide()
        self.name_attack.hide()
        self.name_life.hide()
        self.name_speed.hide()
        self.title.hide()
        self.speed_attack_up.hide()
        self.speed_up.hide()
        self.life_up.hide()
        self.exit_store.hide()

    def show_all(self):
        self.show()
        self.name_attack.show()
        self.name_life.show()
        self.name_speed.show()
        self.title.show()
        self.speed_attack_up.show()
        self.speed_up.show()
        self.life_up.show()
        self.exit_store.show()


class ImageLabel(QLabel):

    release_mouse_signal = pyqtSignal(float, float, str, str)  # x, y, sprite, item_name

    def __init__(self, name, sprite, parent=None):
        super().__init__(parent)
        self.name = name
        self.sprite = sprite
        self.setPixmap(QPixmap(sprite).scaled(62, 62))
        self.resize(62, 62)
        self.release_mouse_signal.connect(parent.mouse_released)

    def mouseReleaseEvent(self, QMouseEvent):
        self.release_mouse_signal.emit(QMouseEvent.pos().x() + self.pos().x() - 20,
                                       QMouseEvent.pos().y() + self.pos().y() - 20, self.sprite, self.name)


if __name__ == "__main__":
    app = QApplication([])
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
