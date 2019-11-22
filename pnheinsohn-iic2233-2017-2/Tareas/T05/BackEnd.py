from Entities import Player, Enemy, Entity, Item
from PyQt5.QtCore import pyqtSignal, QObject
from PyQt5.Qt import QTest
from math import cos, sin, radians
from random import triangular, random, randint, expovariate, uniform
from threading import Thread
from constantes import *
from time import time


class GameManager(QObject):
    # Game Signals
    update_win = pyqtSignal()
    update_stage = pyqtSignal(int)  # stage_number
    ask_for_name = pyqtSignal(float)  # score
    update_start_again = pyqtSignal(str)  # String to show
    show_paused_buttons = pyqtSignal(bool)  # True to show
    start_count_down = pyqtSignal(str, bool)  # sprite, true to show
    # Player FrontEnd Signals
    update_player_hp = pyqtSignal(float)  # hp_percentage
    update_player_size = pyqtSignal(int)  # size
    update_hide_sprite = pyqtSignal(bool)  # hide
    update_player_sprite = pyqtSignal(str)  # sprite
    update_player_score = pyqtSignal(float)  # score
    update_player_rotation = pyqtSignal(int)  # rot
    update_player_exp = pyqtSignal(float, int)  # exp_percentage, level
    update_player_inventory = pyqtSignal(str, int)  # sprite, index
    update_player_position = pyqtSignal(float, float)  # x, y
    # Player BackEnd Signals
    die_signal = pyqtSignal(bool)
    update_stage_level = pyqtSignal(int)  # stage_number
    update_player_experience = pyqtSignal(Enemy)  # enemy
    # Enemy Signals
    update_new_enemy = pyqtSignal()
    update_kill_enemy = pyqtSignal(int)  # index
    update_kill_all_enemies = pyqtSignal()
    update_enemy_hp = pyqtSignal(int, float)  # index, hp_percentage
    update_enemy_label = pyqtSignal(int, int, float, float, int, str)  # index, size, x, y, rot, sprite
    # Item Signals
    update_explosion = pyqtSignal(str)  # sprite
    update_safe_zone = pyqtSignal(int, int)  # x, y
    update_kill_extra_life = pyqtSignal(int)  # index
    update_kill_extra_point = pyqtSignal(int)  # index
    update_new_bomb = pyqtSignal(int, int, str)  # x, y, sprite
    update_new_extra_life = pyqtSignal(int, int)  # x, y
    update_new_extra_point = pyqtSignal(int, int)  # x, y

    def __init__(self, game_widget, check_store_item_signal):
        super().__init__()
        # Game
        self.level = 1
        self.in_count_down = False
        self.extra_lives = []
        self.extra_points = []
        self.score = 0
        self.update_win.connect(game_widget.win)
        self.update_stage.connect(game_widget.change_stage)
        self.start_count_down.connect(game_widget.start_count_down)
        self.update_start_again.connect(game_widget.wait_to_start_again)
        self.show_paused_buttons.connect(game_widget.show_paused_buttons)
        # Player FrontEnd
        self.ask_for_name.connect(game_widget.ask_for_name)
        self.update_hide_sprite.connect(game_widget.hide_sprite)
        self.update_player_hp.connect(game_widget.change_player_hp)
        self.update_player_position.connect(game_widget.move_player)
        self.update_player_exp.connect(game_widget.change_player_exp)
        self.update_player_rotation.connect(game_widget.rotate_player)
        self.update_player_size.connect(game_widget.change_player_size)
        self.update_player_score.connect(game_widget.change_player_score)
        self.update_player_sprite.connect(game_widget.change_player_sprite)
        self.update_player_inventory.connect(game_widget.change_player_inventory)
        # Player BackEnd
        self.die_signal.connect(self.start)
        self.update_stage_level.connect(self.change_stage)
        self.update_player_experience.connect(self.player_receives_exp)
        check_store_item_signal.connect(self.check_store_item)
        # Enemies
        self.enemy_rate_helper = self.enemy_gen()
        self.update_new_enemy.connect(game_widget.new_enemy)
        self.update_kill_enemy.connect(game_widget.kill_enemy)
        self.update_enemy_hp.connect(game_widget.change_enemy_hp)
        self.update_enemy_label.connect(game_widget.change_enemy_label)
        self.update_kill_all_enemies.connect(game_widget.kill_all_enemies)
        # Items
        self.update_new_bomb.connect(game_widget.new_bomb)
        self.update_safe_zone.connect(game_widget.new_safe_zone)
        self.update_explosion.connect(game_widget.explode_bomb)
        self.update_new_extra_life.connect(game_widget.new_life)
        self.update_kill_extra_life.connect(game_widget.kill_life)
        self.update_new_extra_point.connect(game_widget.new_point)
        self.update_kill_extra_point.connect(game_widget.kill_point)

    # Game
    @property
    def level_values(self):
        if self.level == 1:
            return 1, 5, 1
        elif self.level == 2:
            return 1, 6, 3
        elif self.level == 3:
            return 3, 7, 5
        elif self.level == 4:
            return 5, 9, 7
        else:
            return 7, 10, 9

    def alive_score(self):
        try:
            while Entity.playing:
                QTest.qWait(1000)
                self.main_player.score += float(PUNTAJE_TIEMPO)
                self.update_player_score.emit(self.main_player.score)
        except ValueError as err:
            print(err)

    def start(self, start):
        if start:  # Main Way to kill all entities Threads
            self.safe_zone = Item(8)
            self.main_player = Player(self.update_player_hp, self.update_player_size, self.update_stage_level,
                                      self.update_win, self.update_player_score, self.safe_zone, PUNTAJE_NIVEL,
                                      self.die_signal)
            if isinstance(PUNTAJE_INICIO, float) or isinstance(PUNTAJE_INICIO, int):
                self.main_player.score = float(PUNTAJE_INICIO)
            self.update_player_score.emit(self.main_player.score)
            self.update_player_position.emit(self.main_player.x, self.main_player.y)

            bombs = Thread(target=self.send_bombs, daemon=True)
            enemies = Thread(target=self.send_enemies, daemon=True)
            alive_score = Thread(target=self.alive_score, daemon=True)
            safe_zones = Thread(target=self.send_safe_zones, daemon=True)
            extra_lives = Thread(target=self.send_extra_life, daemon=True)
            extra_points = Thread(target=self.send_extra_points, daemon=True)
            player_sprites = Thread(target=self.send_player_sprites, daemon=True)

            bombs.start()
            enemies.start()
            alive_score.start()
            safe_zones.start()
            extra_lives.start()
            extra_points.start()
            player_sprites.start()
        else:
            Entity.playing = False
            self.update_kill_all_enemies.emit()
            self.ask_for_name.emit(self.main_player.score)

    def pause(self, pause):
        if not self.in_count_down:
            if pause:
                Entity.playing = False
                self.show_paused_buttons.emit(True)
            else:
                self.in_count_down = True
                self.show_paused_buttons.emit(False)
                self.start_count_down.emit("Assets/Countdowns/3.png", True)
                QTest.qWait(1000)
                self.start_count_down.emit("Assets/Countdowns/2.png", True)
                QTest.qWait(1000)
                self.start_count_down.emit("Assets/Countdowns/1.png", True)
                QTest.qWait(1000)
                self.start_count_down.emit("", False)
                Entity.playing = True

                for enemy in Enemy.enemies:
                    make_it_intelligent = Thread(target=self.start_intelligence, args=(enemy,), daemon=True)
                    make_it_intelligent.start()

                bombs = Thread(target=self.send_bombs, daemon=True)
                enemies = Thread(target=self.send_enemies, daemon=True)
                alive_score = Thread(target=self.alive_score, daemon=True)
                safe_zones = Thread(target=self.send_safe_zones, daemon=True)
                extra_lives = Thread(target=self.send_extra_life, daemon=True)
                extra_points = Thread(target=self.send_extra_points, daemon=True)
                player_sprites = Thread(target=self.send_player_sprites, daemon=True)

                bombs.start()
                enemies.start()
                alive_score.start()
                safe_zones.start()
                extra_lives.start()
                extra_points.start()
                player_sprites.start()
                self.in_count_down = False

    def change_stage(self, stage_number):
        Entity.playing = False
        self.level += 1
        self.update_kill_all_enemies.emit()
        self.main_player.size = 2
        self.main_player.level = 1
        self.update_stage.emit(stage_number)
        Entity.entities = []
        Enemy.enemies = []
        self.extra_lives = []
        self.extra_points = []

        self.update_start_again.emit("Wait 30 Seconds to load next level")

        Entity.playing = True

        bombs = Thread(target=self.send_bombs, daemon=True)
        enemies = Thread(target=self.send_enemies, daemon=True)
        alive_score = Thread(target=self.alive_score, daemon=True)
        safe_zones = Thread(target=self.send_safe_zones, daemon=True)
        extra_lives = Thread(target=self.send_extra_life, daemon=True)
        extra_points = Thread(target=self.send_extra_points, daemon=True)
        player_sprites = Thread(target=self.send_player_sprites, daemon=True)

        bombs.start()
        enemies.start()
        alive_score.start()
        safe_zones.start()
        extra_lives.start()
        extra_points.start()
        player_sprites.start()

    def check_store_item(self, item_name, sprite, index):
        if item_name == "speed_up" and self.main_player.score >= 250:
            self.main_player.score -= 250
            self.main_player.speed_bonus = self.main_player.speed * 0.1
            self.update_player_inventory.emit(sprite, index)
        elif item_name == "speed_attack_up" and self.main_player.score >= 500:
            self.main_player.score -= 500
            self.main_player.attack_cd *= 0.85
            self.update_player_inventory.emit(sprite, index)
        elif item_name == "life_up" and self.main_player.score >= 750:
            self.main_player.score -= 750
            self.main_player.bonus = self.max_hp * 0.2
            self.update_player_inventory.emit(sprite, index)
        self.update_player_score.emit(self.main_player.score)

    # Player
    def send_player_sprites(self):
        while Entity.playing:
            self.main_player.sprites[
                self.main_player.sprite_index] = self.main_player.sprites[self.main_player.sprite_index][1:] \
                                                 + [self.main_player.sprites[self.main_player.sprite_index][0]]
            self.update_player_sprite.emit(self.main_player.sprites[self.main_player.sprite_index][0])
            QTest.qWait(self.main_player.sprite_speed)

    def move_entity(self, event):
        if Entity.playing:
            self.main_player.sprite_speed /= 2
            if self.main_player.rotation == 0:
                self.main_player.y += self.main_player.speed * -event.factor
            elif self.main_player.rotation == 180:
                self.main_player.y += self.main_player.speed * event.factor
            elif self.main_player.rotation == 90:
                self.main_player.x += self.main_player.speed * event.factor
            elif self.main_player.rotation == 270:
                self.main_player.x += self.main_player.speed * -event.factor
            else:
                self.main_player.x += self.main_player.speed * sin(radians(self.main_player.rotation)) * event.factor
                self.main_player.y += self.main_player.speed * cos(radians(self.main_player.rotation)) * -event.factor
            self.update_player_position.emit(self.main_player.x, self.main_player.y)
            if self.main_player.in_safe_zone:
                self.update_hide_sprite.emit(True)
            else:
                self.update_hide_sprite.emit(False)
            points_to_kill = []
            lives_to_kill = []
            for point in self.extra_points:
                if ((self.main_player.x - (point.x)) ** 2 + (self.main_player.y - (point.y)) ** 2) ** (1 / 2) \
                        <= point.radius + 20:
                    self.main_player.score += 1000
                    self.update_kill_extra_point.emit(self.extra_points.index(point))
                    self.update_player_score.emit(self.main_player.score)
                    points_to_kill.append(point)
            for life in self.extra_lives:
                if ((self.main_player.x - (life.x)) ** 2 + (self.main_player.y - (life.y)) ** 2) ** (1 / 2) \
                        <= life.radius + 20:
                    self.main_player.hp += 10000
                    self.update_kill_extra_life.emit(self.extra_lives.index(life))
                    lives_to_kill.append(life)
            for point in points_to_kill:
                del self.extra_points[self.extra_points.index(point)]
            for life in lives_to_kill:
                del self.extra_lives[self.extra_lives.index(life)]

    def stop_entity(self):
        self.main_player.sprite_speed *= 2

    def rotate_entity(self, event):
        self.main_player.rotation += event.rotation
        self.update_player_rotation.emit(self.main_player.rotation)

    def player_makes_damage(self, enemy):
        while ((enemy.x - self.main_player.x) ** 2 + (enemy.y - self.main_player.y) ** 2) \
                ** (1 / 2) <= self.main_player.radius and enemy.hp > 0 and Entity.playing:
            enemy.receive_damage(self.main_player.damage)
            QTest.qWait(self.main_player.attack_cd * 1000)

    def player_receives_exp(self, enemy):
        self.main_player.experience += 100 * max(enemy.size - self.main_player.size + 3, 1)
        self.update_player_exp.emit(self.main_player.experience / 10, self.main_player.level)
        try:
            self.main_player.score += 1000 + PUNTAJE_ENEMIGO * (enemy.size - self.main_player.size)
            self.update_player_score.emit(self.main_player.score)
        except Exception as err:
            print(err)

    # Enemies
    def send_enemies(self):  # Enemies Main thread
        rate = next(self.enemy_rate_helper)
        while Entity.playing:
            new_enemy = Enemy(triangular(*self.level_values), self.update_enemy_hp, self.update_kill_enemy,
                              self.update_player_experience, self.die_signal)
            self.update_new_enemy.emit()
            make_it_intelligent = Thread(target=self.start_intelligence, args=(new_enemy,), daemon=True)
            make_it_intelligent.start()
            QTest.qWait(expovariate(rate) * 1000)  # cambiar

    def start_intelligence(self, enemy):
        while Entity.playing and enemy.hp > 0:
            if self.player_is_near(enemy) and (enemy.size < self.main_player.size or (
                            enemy.size == self.main_player.size and random() <= 0.5)):
                QTest.qWait(enemy.reaction_time)
                while enemy.hp > 0 and self.player_is_noticed(enemy) and Entity.playing:
                    self.player_is_near_actions(enemy, "Scape")
            elif self.player_is_near(enemy) and (enemy.size > self.main_player.size
                                                 or enemy.size == self.main_player.size):
                QTest.qWait(enemy.reaction_time)
                while enemy.hp > 0 and self.player_is_noticed(enemy) and Entity.playing:
                    self.player_is_near_actions(enemy, "Attack")
            else:
                if random() <= 0.25:
                    enemy.rotation = randint(0, 359)
                before = time()
                while enemy.hp > 0 and time() - before < 1 and Entity.playing:
                    self.move_enemy(enemy)

    def player_is_near(self, enemy):
        if ((enemy.x - self.main_player.x) ** 2 + (enemy.y - self.main_player.y) ** 2) \
                ** (1 / 2) <= self.main_player.size * 30 and not self.main_player.in_safe_zone:
            return True
        return False

    def player_is_noticed(self, enemy):
        if ((enemy.x - self.main_player.x) ** 2 + (enemy.y - self.main_player.y) ** 2) \
                ** (1 / 2) <= enemy.scape_range(self.main_player.size * 30) and not self.main_player.in_safe_zone:
            return True
        return False

    def player_is_near_actions(self, enemy, key):
        if key == "Scape":
            self.set_enemy_scape_rot(enemy)
        else:
            self.set_enemy_attack_rot(enemy)
        self.move_enemy(enemy)
        attack_enemy = Thread(target=self.player_makes_damage, daemon=True, args=(enemy,))
        attack_player = Thread(target=self.enemy_makes_damage, daemon=True, args=(enemy,))
        attack_enemy.start()
        attack_player.start()
        if enemy.attack_cd > self.main_player.attack_cd:
            attack_enemy.join()
        else:
            attack_player.join()

    def set_enemy_scape_rot(self, enemy):
        if enemy.x - self.main_player.x > 0 and enemy.y - self.main_player.y > 0:
            enemy.rotation = randint(0, 90)
        elif enemy.x - self.main_player.x > 0:
            enemy.rotation = randint(90, 180)
        elif enemy.x - self.main_player.x < 0 and enemy.y - self.main_player.y < 0:
            enemy.rotation = randint(180, 270)
        else:
            enemy.rotation = randint(270, 360)

    def set_enemy_attack_rot(self, enemy):
        if enemy.x - self.main_player.x > 0 and enemy.y - self.main_player.y > 0:
            enemy.rotation = randint(180, 270)
        elif enemy.x - self.main_player.x > 0:
            enemy.rotation = randint(270, 360)
        elif enemy.x - self.main_player.x < 0 and enemy.y - self.main_player.y < 0:
            enemy.rotation = randint(0, 90)
        else:
            enemy.rotation = randint(90, 180)

    def move_enemy(self, enemy):
        enemy.x += enemy.speed * sin(radians(enemy.rotation))
        enemy.y += enemy.speed * cos(radians(enemy.rotation))
        try:
            self.update_enemy_label.emit(Enemy.enemies.index(enemy), enemy.size, enemy.x, enemy.y,
                                         enemy.rotation, enemy.sprites[enemy.sprite_index][0])
        except ValueError as err:
            print(err)
        else:
            enemy.sprites[enemy.sprite_index] = enemy.sprites[enemy.sprite_index][1:] \
                                                + [enemy.sprites[enemy.sprite_index][0]]
            QTest.qWait(enemy.sprite_speed)

    def enemy_makes_damage(self, enemy):
        while ((enemy.x - self.main_player.x) ** 2 + (enemy.y - self.main_player.y) ** 2) \
                ** (1 / 2) <= self.main_player.radius and enemy.hp > 0 and Entity.playing:
            self.main_player.receive_damage(enemy.damage)
            QTest.qWait(enemy.attack_cd * 1000)

    def enemy_gen(self):
        id_ = 0
        while True:
            yield 1 / (11 - self.level - id_)
            id_ += 1

    # Items
    def send_bombs(self):
        QTest.qWait(uniform(1000, 30000))
        while Entity.playing:
            new_bomb = Item(4)
            self.update_new_bomb.emit(new_bomb.x, new_bomb.y, "Assets/Items/bomba.png")
            QTest.qWait(3000)
            explosion = Thread(target=self.update_explosion.emit, args=("Assets/Items/explosion.png",), daemon=True)
            explosion.start()
            self.explode(new_bomb)
            QTest.qWait(uniform(1000, 27000))  # minus 3 cos' the waiting time to explode

    def explode(self, bomb):
        for entity in Entity.entities:
            if ((isinstance(entity, Player) and not entity.in_safe_zone) or isinstance(entity, Enemy)) and \
                                    ((entity.x - bomb.x) ** 2 + (entity.y - bomb.y) ** 2) ** (1 / 2) \
                            <= ((10 + bomb.radius) ** 2 + (10 + bomb.radius) ** 2) ** (1 / 2):
                entity.receive_damage(10000)  # 10000 it's enough to kill anyone

    def send_safe_zones(self):
        QTest.qWait(uniform(1000, 30000))
        while Entity.playing:
            self.safe_zone = Item(9)
            self.main_player.safe_zone = self.safe_zone
            self.update_safe_zone.emit(self.safe_zone.x, self.safe_zone.y)
            QTest.qWait(uniform(1000, 30000))

    def send_extra_points(self):
        QTest.qWait(uniform(1000, 30000))
        while Entity.playing:
            point = Item(2)
            self.extra_points.append(point)
            self.update_new_extra_point.emit(point.x, point.y)
            QTest.qWait(uniform(1000, 30000))

    def send_extra_life(self):
        QTest.qWait(uniform(1000, 30000))
        while Entity.playing:
            life = Item(4)
            self.extra_lives.append(life)
            self.update_new_extra_life.emit(life.x, life.y)
            QTest.qWait(uniform(1000, 30000))
