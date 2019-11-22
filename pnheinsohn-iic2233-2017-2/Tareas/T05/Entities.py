from abc import ABCMeta
from random import uniform, randint


class Entity(metaclass=ABCMeta):

    entities = []
    playing = True
    id_ = 0

    def __init__(self, hp, sprites, hp_signal, die_signal):
        self._radius = self.radius
        self._stage = 1
        self._x = randint(-5, round(1330 - self._radius))
        self._y = randint(62, round(670 - self._radius))
        self._hp = hp
        self.attack_cd = 1
        self._rotation = 0
        self.sprite_index = 0
        self.sprites = sprites
        self.hp_signal = hp_signal
        self.die_signal = die_signal
        self.sprite_speed = 125
        Entity.id_ += 1
        Entity.entities.append(self)

    @property
    def x(self):
        return self._x

    @x.setter
    def x(self, value):
        if value < -5:
            self._x = -5
        elif value + self.radius > 1330:
            self._x = 1330 - self.radius
        else:
            self._x = value

    @property
    def y(self):
        return self._y

    @y.setter
    def y(self, value):
        if value < 62:
            self._y = 62
        elif value + self.radius > 670:
            self._y = 670 - self.radius
        else:
            self._y = value

    @property
    def radius(self):
        return 15.5 * self.size / 2

    @property
    def speed(self):
        return 10 / self.size + round(self.size ** (1 / 3))

    @property
    def hp(self):
        return self._hp

    @hp.setter
    def hp(self, value):
        if value <= 0:
            self._hp = 0
            self.sprite_index = -1
        elif value >= self.max_hp:
            self._hp = self.max_hp
            self.sprite_index = 0
        elif value / self.max_hp <= 0.8:
            self.sprite_index = 1
            self._hp = value
        else:
            self.sprite_index = 0
            self._hp = value

    @property
    def rotation(self):
        return self._rotation

    @rotation.setter
    def rotation(self, value):
        if value >= 360:
            self._rotation = 0
        elif value < 0:
            self._rotation = 359
        else:
            self._rotation = value

    def receive_damage(self, damage):
        self.hp -= damage
        if isinstance(self, Player):
            self.hp_signal.emit(round(self.hp / self.max_hp * 100, 1))
            if self.hp == 0:
                Entity.entities.pop(Entity.entities.index(self))
                Entity.playing = False
                self.die_signal.emit(False)
        else:
            self.hp_signal.emit(Enemy.enemies.index(self), round(self.hp / self.max_hp * 100, 1))
            if self.hp == 0:
                Entity.entities.pop(Entity.entities.index(self))
                enemy_dead = Enemy.enemies.pop(Enemy.enemies.index(self))
                self.exp_signal.emit(enemy_dead)


class Player(Entity):

    def __init__(self, hp_signal, size_signal, stage_signal, win_signal, score_signal, safe_zone, puntaje_nivel,
                 die_signal):
        Entity.playing = True
        self.bonus = 0
        self._size = 2
        self._level = 1
        self.score = 0
        self._experience = 0
        self._damage = self.damage
        self.speed_bonus = 0
        self.safe_zone = safe_zone
        self.win_signal = win_signal
        self.size_signal = size_signal
        self.stage_signal = stage_signal
        self.score_signal = score_signal
        self.level_score = puntaje_nivel
        self.next_increase_size = [500, 1000]
        self.sprites = [["Assets\JugadorPrincipal/jugador00.png", "Assets/JugadorPrincipal/jugador01.png",
                         "Assets/JugadorPrincipal/jugador02.png", "Assets/JugadorPrincipal/jugador03.png",
                         "Assets/JugadorPrincipal/jugador04.png", "Assets/JugadorPrincipal/jugador05.png",
                         "Assets/JugadorPrincipal/jugador06.png", "Assets/JugadorPrincipal/jugador07.png"],
                        ["Assets\JugadorPrincipal/jugador11.png", "Assets/JugadorPrincipal/jugador11.png",
                         "Assets/JugadorPrincipal/jugador12.png", "Assets/JugadorPrincipal/jugador13.png",
                         "Assets/JugadorPrincipal/jugador14.png", "Assets/JugadorPrincipal/jugador15.png",
                         "Assets/JugadorPrincipal/jugador16.png", "Assets/JugadorPrincipal/jugador17.png"],
                        ["Assets/JugadorPrincipal/jugador20.png"]]
        super(Player, self).__init__(hp=self.max_hp, sprites=self.sprites, hp_signal=hp_signal, die_signal=die_signal)

    @property
    def in_safe_zone(self):
        return ((self.x - (self.safe_zone.x + 2 * self.safe_zone.radius / 3)) ** 2 +
                (self.y - (self.safe_zone.y + self.safe_zone.radius)) ** 2) ** (1 / 2) <= self.safe_zone.radius

    @property
    def max_hp(self):
        return self.size * 20 + 100 + self.bonus

    @property
    def size(self):
        return self._size

    @size.setter
    def size(self, value):
        if value > 10:
            self._size = 10
        else:
            self._size = value
            self.size_signal.emit(self._size)

    @property
    def level(self):
        return self._level

    @level.setter
    def level(self, value):
        self._experience = 0
        self._level = value
        self.hp = self.max_hp
        if self._level == 5:
            self.stage += 1
        try:
            self.score += 1500 + self.level_score * value
            self.score_signal.emit(self.score)
        except Exception as err:
            print(err)

    @property
    def stage(self):
        return self._stage

    @stage.setter
    def stage(self, value):
        if self._stage == 5:
            self.win_signal.emit()
        else:
            self._stage = value
            if isinstance(self, Player):
                self.stage_signal.emit(value)

    @property
    def experience(self):
        return self._experience

    @experience.setter
    def experience(self, value):
        self._experience = value
        if self._experience >= self.next_increase_size[0]:
            if self.next_increase_size[0] == 1000:
                self.level += 1
            self.next_increase_size = [self.next_increase_size[1], self.next_increase_size[0]]
            self.size += 1
            self.size_signal.emit(self.size)

    @property
    def damage(self):
        return round(self.size * self.max_hp / 10)

    @property
    def speed(self):
        return 10 / self.size + round(self.size ** (1 / 3)) + self.speed_bonus


class Enemy(Entity):

    enemies = []

    def __init__(self, size, hp_signal, kill_signal, exp_signal, die_signal):
        self.size = int(size)
        self._damage = self.damage
        self._max_hp = self.max_hp
        self.exp_signal = exp_signal
        self.kill_signal = kill_signal
        self.sprites = [["Assets\Enemigos/enemigo00.png", "Assets/Enemigos/enemigo01.png",
                         "Assets/Enemigos/enemigo02.png", "Assets/Enemigos/enemigo03.png",
                         "Assets/Enemigos/enemigo04.png", "Assets/Enemigos/enemigo05.png",
                         "Assets/Enemigos/enemigo06.png", "Assets/Enemigos/enemigo07.png"],
                        ["Assets\Enemigos/enemigo11.png", "Assets/Enemigos/enemigo11.png",
                         "Assets/Enemigos/enemigo12.png", "Assets/Enemigos/enemigo13.png",
                         "Assets/Enemigos/enemigo14.png", "Assets/Enemigos/enemigo15.png",
                         "Assets/Enemigos/enemigo16.png", "Assets/Enemigos/enemigo17.png"],
                        ["Assets/Enemigos/enemigo20.png"]]
        super().__init__(hp=self._max_hp, sprites=self.sprites, hp_signal=hp_signal, die_signal=die_signal)
        Enemy.enemies.append(self)

    @property
    def max_hp(self):
        return self.size * 20 + 100

    @property
    def damage(self):
        return round(self.size * self.max_hp / 10)

    @staticmethod
    def scape_range(vision_range):
        return vision_range * 1.5

    @property
    def reaction_time(self):
        return uniform(0, 1)


class Item:

    items = []

    def __init__(self, size):
        self.size = size
        self._radius = self.radius
        self.x = randint(-5, round(1330 - self._radius))
        self.y = randint(62, round(670 - self._radius))
        Item.items.append(self)

    @property
    def radius(self):
        return 15.5 * self.size / 2
