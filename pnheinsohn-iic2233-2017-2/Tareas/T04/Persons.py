from abc import ABCMeta
from collections import deque
from random import random, randint, uniform, expovariate, normalvariate, choice
from Functions import go_people_kwargs, get_int_list


# Everyone
class Person(metaclass=ABCMeta):

    persons = []

    def __init__(self, name, last_name, age):
        self.name = name
        self.last_name = last_name
        self.age = age
        Person.persons.append(self)

    def __repr__(self):
        return "{} {} {}".format(type(self).__name__, self.name, self.last_name)


# MembersUC
class MemberUC(Person, metaclass=ABCMeta):

    membersUC = []

    def __init__(self, name, last_name, age, best_sellers):
        super().__init__(name, last_name, age)
        self.best_sellers_names = best_sellers.split(" - ")
        self.arrival_time_to_campus = float("Inf")
        self.lunch_distribution = None  # X, Y, Z
        self.movement_in_campus = float("Inf")
        self.decide_lunch_time = float("Inf")
        self.lunch_time = float("Inf")
        self.in_campus = False
        self.in_line = False
        self.snack = [float("Inf"), False]
        self.ate = False
        self.times_left_a_line = 0
        MemberUC.membersUC.append(self)

    @property
    def best_sellers(self):
        return list(filter(lambda persona: "{} {}".format(persona.name, persona.last_name) in self.best_sellers_names,
                           sellers))

    def leave_campus(self):
        self.ate = False
        self.in_line = False
        self.snack = [float("Inf"), False]
        self.in_campus = False

    def set_lunch_time(self):
        member_probability = random() * 100
        if member_probability <= min(self.lunch_distribution):
            first = self.lunch_distribution.index(min(self.lunch_distribution))
            second = self.lunch_distribution[::-1].index(min(self.lunch_distribution))
        elif member_probability <= min(self.lunch_distribution) + sorted(self.lunch_distribution)[1]:
            first = self.lunch_distribution.index(sorted(self.lunch_distribution)[1])
            second = self.lunch_distribution[::-1].index(sorted(self.lunch_distribution)[1])
        else:
            first = self.lunch_distribution.index(max(self.lunch_distribution))
            second = self.lunch_distribution[::-1].index(max(self.lunch_distribution))
        chosen_schedule = choice([first, second])
        if chosen_schedule == 0:
            self.decide_lunch_time = 130  # 13:10
        elif chosen_schedule == 1:
            self.decide_lunch_time = 190  # 14:10
        else:
            self.decide_lunch_time = 70  # 12:10
        going_for_lunch = expovariate(self.movement_in_campus)
        if going_for_lunch > 3 / self.movement_in_campus:
            going_for_lunch = 3 / self.movement_in_campus
        self.lunch_time = going_for_lunch + normalvariate(self.decide_lunch_time, 10)
        if self.lunch_time > self.decide_lunch_time + 120:
            self.lunch_time = self.decide_lunch_time + 120
        elif self.lunch_time < self.decide_lunch_time - 60:
            self.lunch_time = self.decide_lunch_time - 60


class Student(MemberUC):

    def __init__(self, name, last_name, age, best_sellers):
        super().__init__(name, last_name, age, best_sellers)
        self._money = None  # As a reference for daily money
        self.daily_money = None  # Is the only money that variates
        self.patience_limit = None

    def receive_money(self, base_money, monthly=False):  # Every month (30 days)
        if monthly:
            self._money = round(base_money * (1 + random() ** random()) * 20)
        else:
            self.daily_money = self._money / 20

    def set_patience(self, params):
        self.patience_limit = randint(*get_int_list(params))


class Functionary(MemberUC):

    def __init__(self, name, last_name, age, best_sellers):
        super().__init__(name, last_name, age, best_sellers)
        self.daily_money = None
        self.last_seller = None


# Externals
class Seller(Person):

    def __init__(self, name, last_name, age, food_type):
        super().__init__(name, last_name, age)
        self.can_sell = True
        self.food_type = food_type
        self.next_attending = float("Inf")
        self._arrival_time = float("Inf")
        self.fear_days_limit = None
        self._fear_days = 0  # To simulate the days a seller is gone. When it's 0 seller goes to work.
        self.selling_speed = None
        self._daily_stock = None
        self.stockless = False
        self._work_place = None
        self.attending = None
        self.products = set()
        self.line = deque()
        self.permit = None
        self.amount_of_toxic_members = 0
        self.quality_prom = None
        self.amount_of_stock_out = 0
        self.did_not_sold = 0
        self.sold_today = False

    @property
    def work_place(self):
        return self._work_place and self.daily_stock != 0

    @work_place.setter
    def work_place(self, value):
        self._work_place = value

    @property
    def waiting_time(self):
        return len(self.line) * self.selling_speed

    @property
    def fear_days(self):
        return self._fear_days == 0

    @fear_days.setter
    def fear_days(self, value):
        if value <= 0:
            self._fear_days = 0
        else:
            self._fear_days = value

    @property
    def arrival_time(self):
        return self._arrival_time

    @arrival_time.setter
    def arrival_time(self, value):
        if value < 0:
            self._arrival_time = 0
        else:
            self._arrival_time = value

    @property
    def daily_stock(self):
        return self._daily_stock

    @daily_stock.setter
    def daily_stock(self, value):
        if value <= 0:
            self._daily_stock = 0
            self.stockless = True
        else:
            self._daily_stock = value

    def receive_stock(self, params):
        self._daily_stock = int(uniform(*get_int_list(params)))

    def attend_member(self, actual_time):
        self.sold_today = True
        member = self.line.popleft()
        member.in_line = False
        if isinstance(member, Student):
            product = choice(list(filter(lambda prod: prod.price <= member.daily_money, self.products)))
        else:
            product = sorted(filter(lambda prod: prod.price <= member.daily_money, self.products),
                             key=lambda prod: prod.quality(actual_time))[-1]
        product.amount_sold += 1
        product.daily_sold += 1
        member.daily_money -= product.price
        #self.daily_stock -= 1
        return member, product

    def reset_day(self, day, month):
        if not self.sold_today:
            self.did_not_sold += 1
            if self.did_not_sold >= 20:
                print("(11:00 | {}/{})\t[BANCARROTA]:\t'{}' se ha quedado en bancarrota! Nunca más lo veran"
                      .format(day, month, self))
                self.can_sell = False
        else:
            self.did_not_sold = 0
            self.sold_today = False
        self.line = deque()
        self.attending = None
        self.work_place = None
        self.stockless = False
        self.next_attending = 0
        self.arrival_time = normalvariate(0, 30)
        for product in self.products:
            if product.amount_sold > product.max_amount:
                product.max_amount = product.amount_sold
            elif product.amount_sold < product.min_amount:
                product.min_amount = product.amount_sold
            product.total_sold += product.amount_sold
            product.amount_sold = 0


class Cop(Person):

    def __init__(self, name, last_name, age, personality):
        super().__init__(name, last_name, age)
        self.personality = personality
        self.products_to_check_rate = 0
        self.cheat_prob = 0


with open("personas.csv", "r", encoding="utf-8") as persons_csv:
    first_filter = list(map(lambda row: row.strip("\n").split("; "), persons_csv))

    sellers = list(map(lambda row: Seller(**go_people_kwargs(row, "Vendedor", first_filter)),
                       filter(lambda row: "Vendedor" in row, first_filter)))

    students = list(map(lambda row: Student(**go_people_kwargs(row, "Alumno", first_filter)),
                        filter(lambda row: "Alumno" in row, first_filter)))

    functionaries = list(map(lambda row: Functionary(**go_people_kwargs(row, "Funcionario", first_filter)),
                             filter(lambda row: "Funcionario" in row, first_filter)))

    cops = list(map(lambda row: Cop(**go_people_kwargs(row, "Carabinero", first_filter)),
                    filter(lambda row: "Carabinero" in row, first_filter)))
