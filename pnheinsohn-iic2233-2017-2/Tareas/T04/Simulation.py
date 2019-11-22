from random import randint, triangular, random, choice, uniform, expovariate
from Functions import get_list, get_float_list, get_int_list
from Persons import students, sellers, cops, MemberUC, Student, Functionary
from Products import foods, snacks, Product, Snack, Food
from QuickDevil import QuikDevil


class Simulation:

    def __init__(self, dias_susto, personalidad_jekyll, llamado_policial, concha_estereo, moda_llegada_campus,
                 limite_paciencia, rapidez_vendedores, traslado_campus, probabilidad_permiso, distribucion_almuerzo,
                 base_mesada, personalidad_hide, dinero_funcionarios, stock_vendedores):
        # QuikDevil:
        self.quik_devil = QuikDevil()
        for snack in snacks:
            self.quik_devil.snacks.add(snack)
        for food in foods:
            self.quik_devil.foods.add(food)
        # Students:
        self.patience = limite_paciencia
        self.student_base_income = float(base_mesada)
        # Functionaries:
        self.functionary_daily_income = float(dinero_funcionarios)
        # Sellers:
        self.stock_vendedores = stock_vendedores
        # Simulation it self:
        self._next_member_arrives = None
        self._next_seller_arrives = None
        self._next_seller_to_attend = None
        self._next_seller_attending_finishes = None
        self._next_choose_lunch_line = None
        self._next_choose_snack_line = None
        self.campus_arrival_trend = int(moda_llegada_campus)
        self.call_cops_rate = float(llamado_policial)
        self.party_prob = float(concha_estereo)
        self.next_extreme_temperatures = round(uniform(2, 20))
        self.next_burger_rain = round(expovariate(1 / 21))
        while self.next_burger_rain > 30:
            self.next_burger_rain = round(expovariate(1 / 21))
        self.sickness_ratio = 0.35
        self._actual_time = 0
        self._actual_day = 0
        self.month = 0
        self.prices_changed = False
        self.quality_changed = False
        self.putrefaction_changed = False
        self.temperature_adviced = False
        self.burger_adviced = False
        self.stereo_adviced = False
        self.stereo_party_register = []
        self.extreme_temperatures_register = []
        # Set params:
        for seller in sellers:
            seller.fear_days_limit = dias_susto  # Set at init.
            seller.permit = float(probabilidad_permiso)  # Set at init.
            seller.selling_speed = randint(*get_float_list(rapidez_vendedores))  # Set at init.
            if "Snack" == seller.food_type:
                for snack in snacks:
                    seller.products.add(Snack(snack.product_name, snack.price, snack.calories, snack.putrefaction_rate,
                                              snack.sold_in))
            else:
                for food in foods:
                    seller.products.add(Food(food.product_name, food.price, food.calories, food.putrefaction_rate,
                                             food.sold_in))
        for cop in cops:
            if cop.personality == "Dr. Jekyll":  # Set at init.
                cop.cheat_prob(get_list(personalidad_jekyll)[1])
                cop.products_to_check_rate(get_list(personalidad_jekyll)[0])
            elif cop.personality == "Mr. Hyde":  # Set at init.
                cop.cheat_prob(get_list(personalidad_hide)[1])
                cop.products_to_check_rate(get_list(personalidad_hide)[0])
        for member in MemberUC.membersUC:
            member.movement_in_campus = float(traslado_campus)
            member.lunch_distribution = get_int_list(distribucion_almuerzo)
            member.lunch_distribution.append(100 - member.lunch_distribution[0] - member.lunch_distribution[1])
        # Statistical Purposes
        self.final_lunch_distribution = [0, 0, 0]
        self.amount_students_did_not_lunched = [0, 0, 0, 0]
        self.cops_incoming_amount = 0
        self.burger_rain_register = []
        self.amount_of_stock_out = 0

    # Time management
    @property
    def actual_time(self):
        return self._actual_time

    @actual_time.setter
    def actual_time(self, value):
        if value >= 240:
            self._actual_time = 0
            self.actual_day += 1
        else:
            self._actual_time = value

    @property
    def actual_day(self):
        return self._actual_day

    @actual_day.setter
    def actual_day(self, value):
        if value > 30:
            self.new_month()
        else:
            self.new_day(value)

    def new_month(self):
        self.month += 1
        for student in students:
            student.receive_money(self.student_base_income, True)
        for seller in sellers:
            if seller.stockless:
                seller.stockless = False
            for product in seller.products:
                if seller.amount_of_stock_out != 0:
                    product.initial_price += product.initial_price * seller.amount_of_stock_out * 0.06
                    seller.amount_of_stock_out = 0
                if product.monthly_non_sold_times != 0:
                    product.initial_price -= product.initial_price * product.monthly_non_sold_times * 0.05
                    product.monthly_non_sold_times = 0
        self.new_day(1)

    def new_day(self, value):
        if self.actual_day == 0 and self.month == 1:
            print("(11:00 | {}/{})\t[INICIO SIMULACIÓN]".format(self._actual_day + 1, self.month))
        elif self.actual_day != 0 and self.month != 0 and self.actual_day != 6 and self.actual_day != 7 \
                and self.actual_day != 13 and self.actual_day != 14 and self.actual_day != 20 \
                and self.actual_day != 21 and self.actual_day != 27 and self.actual_day != 28:
            print("(15:00 | {}/{})\t[END DAY]:\tTodos han abandonado el campus".format(self._actual_day, self.month))
        elif self.actual_day == 6 or self.actual_day == 7 or self.actual_day == 13 or self.actual_day == 14 \
                or self.actual_day == 20 or self.actual_day == 21 or self.actual_day == 27 or self.actual_day == 28:
            print("(11:00 | {}/{})\t[WEEKEND]:\tNo hay eventos durante los fines de semana".format(self.actual_day,
                                                                                                   self.month))
        self._actual_day = value
        self.sickness_ratio = 0.35
        self.temperature_adviced = False
        self.stereo_adviced = False
        self.burger_adviced = False

        if self.month <= 4 and self.actual_day != 6 and self.actual_day != 7 and self.actual_day != 13 \
                and self.actual_day != 14 and self.actual_day != 20 and self.actual_day != 21 \
                and self.actual_day != 27 and self.actual_day != 28:
            print("({})\t[NEW DAY]:\tHa iniciado un nuevo dia!".format(self.time()))
            for memberUC in MemberUC.membersUC:
                if isinstance(memberUC, Functionary):
                    memberUC.daily_money = self.functionary_daily_income
                else:
                    if not memberUC.ate:
                        self.amount_students_did_not_lunched[self.month - 1] += 1
                    memberUC.set_patience(self.patience)
                    memberUC.receive_money(self.student_base_income)
                memberUC.leave_campus()
                memberUC.arrival_time_to_campus = triangular(0, 240, self.campus_arrival_trend)
                memberUC.set_lunch_time()
            for seller in sellers:
                if seller.stockless:
                    seller.amount_of_stock_out += 1
                seller.reset_day(self.actual_day, self.month)
                seller.receive_stock(self.stock_vendedores)
            if self.quality_changed or self.putrefaction_changed or self.prices_changed:
                self.quality_changed = False
                self.putrefaction_changed = False
                self.prices_changed = False
                for product in Product.products:
                    if product.daily_sold == 0:
                        product.monthly_non_sold_times += 1
                        product.daily_sold = 0
                    product.quality_reduction = 1
                    product.putrafaction_intensification = 1
                    product.price = product.initial_price

    def time(self):
        _time = str(self.actual_time - int(self.actual_time / 60) * 60)
        if len(_time) == 1:
            _time = "0" + _time
        if self._actual_day == 6 or self._actual_day == 7 or self.actual_day == 13 or self.actual_day == 14 \
                or self.actual_day == 20 or self.actual_day == 21 or self.actual_day == 27 or self.actual_day == 28:
            return "{}/{}".format(self.actual_day, self.month)
        elif self.actual_time // 60 == 0:
            return "11:{} | {}/{}".format(_time, self.actual_day, self.month)
        elif self.actual_time // 60 == 1:
            return "12:{} | {}/{}".format(_time, self.actual_day, self.month)
        elif self.actual_time // 60 == 2:
            return "13:{} | {}/{}".format(_time, self.actual_day, self.month)
        elif self.actual_time // 60 == 3:
            return "14:{} | {}/{}".format(_time, self.actual_day, self.month)
        else:
            return "15:{} | {}/{}".format(_time, self.actual_day, self.month)

    def day_difference(self, last_date):
        if len(last_date) == 0:
            return 0
        return abs((self.actual_day + (self.month - 1) * 30) - (last_date[-1][0] + (last_date[-1][1] - 1) * 30))

    # Possible Programmed Events
    @property
    def next_member_arrives(self):
        members_out_of_campus = list(filter(lambda member: not member.in_campus, MemberUC.membersUC))
        if len(members_out_of_campus) == 0:
            return float("Inf")
        self._next_member_arrives = sorted(members_out_of_campus, key=lambda member: member.arrival_time_to_campus)[0]
        return self._next_member_arrives.arrival_time_to_campus

    @property
    def next_seller_arrives(self):
        sellers_out_of_campus = list(filter(lambda seller: not seller.work_place and seller.can_sell, sellers))
        if len(sellers_out_of_campus) == 0:
            return float("Inf")
        self._next_seller_arrives = sorted(sellers_out_of_campus, key=lambda seller: seller.arrival_time)[0]
        return self._next_seller_arrives.arrival_time

    @property
    def next_choose_snack_line(self):
        av_members = sorted(list(filter(lambda member: member.in_campus and not member.in_line and not member.snack[1],
                                        MemberUC.membersUC)), key=lambda member: member.snack[0])
        if len(av_members) == 0:
            return float("Inf")
        self._next_choose_snack_line = av_members[0]
        return av_members[0].snack[0]

    @property
    def next_choose_lunch_line(self):
        av_members = sorted(list(filter(lambda member: member.in_campus and not member.in_line and not member.ate,
                                        MemberUC.membersUC)), key=lambda member: member.lunch_time)
        if len(av_members) == 0:
            return float("Inf")
        self._next_choose_lunch_line = av_members[0]
        return av_members[0].lunch_time

    @property
    def next_seller_to_attend(self):
        av_sellers = sorted(filter(lambda seller: seller.work_place and not seller.attending and len(seller.line) > 0,
                                   filter(lambda seller: seller.can_sell, sellers)),
                            key=lambda seller: seller.next_attending)
        if len(av_sellers) == 0:
            return float("Inf")
        self._next_seller_to_attend = av_sellers[0]
        return self.actual_time

    @property
    def next_seller_finishes_attendance(self):
        av_sellers = sorted(filter(lambda seller: seller.work_place and seller.attending,
                                   filter(lambda seller: seller.can_sell, sellers)),
                            key=lambda seller: seller.next_attending)
        if len(av_sellers) == 0:
            return float("Inf")
        self._next_seller_attending_finishes = av_sellers[0]
        return self._next_seller_attending_finishes.next_attending

    def get_next_event(self):
        times = [self.next_member_arrives, self.next_seller_arrives, self.next_choose_snack_line,
                 self.next_choose_lunch_line, self.next_seller_finishes_attendance, self.next_seller_to_attend]
        time_next_event = min(times)
        if self.month == 4 and self.actual_day == 30 and time_next_event + self.actual_time > 240:
            return "end"
        elif time_next_event >= 240:
            return "new_day"
        events = ["member_arrives", "seller_arrives", "choose_snack_line", "choose_lunch_line",
                  "seller_finishes_attendance", "seller_attends"]
        return events[times.index(time_next_event)]

    # Running
    def run(self):
        self.new_month()
        while self.month <= 4:
            while self.actual_day == 6 or self.actual_day == 7 or self.actual_day == 13 or self.actual_day == 14 \
                    or self.actual_day == 20 or self.actual_day == 21 or self.actual_day == 27 or self.actual_day == 28:
                if self.next_extreme_temperatures == self.actual_day:
                    self.get_next_extreme_temperatures()
                if self.next_burger_rain == self.actual_day:
                    self.get_next_burger_rain()
                self.actual_day += 1
            if not self.temperature_adviced and self.next_extreme_temperatures == self.actual_day:
                self.extreme_temperatures()
            if not self.stereo_adviced and self.actual_day % 5 == 0 and \
                    (self.stereo_day_difference() >= 28 or random() <= self.party_prob):
                self.stereo_party()
            if not self.burger_adviced and self.next_burger_rain <= self.actual_day:
                self.burger_rain()
            self.stereo_adviced = True
            self.temperature_adviced = True
            self.burger_adviced = True
            event = self.get_next_event()
            if event == "member_arrives":
                self.member_arrives()
            elif event == "seller_arrives":
                self.seller_arrives()
            elif event == "choose_snack_line":
                self.choose_snack_line()
            elif event == "choose_lunch_line":
                self.choose_lunch_line()
            elif event == "seller_finishes_attendance":
                self.sellers_finishes_attendance()
            elif event == "seller_attends":
                self.seller_attends()
            elif event == "new_day":
                self.actual_time = 240
            elif event == "end":
                print("({})\t[END SIMULATION]:\tNo Habrán más eventos este mes".format(self.time()))
                break

    # Programmed Event Manager
    def member_arrives(self):
        member = self._next_member_arrives
        self.actual_time = round(member.arrival_time_to_campus)
        member.in_campus = True
        print("({})\t[LLEGADA]:\t'{}' ha llegado al campus!".format(self.time(), member))
        if self.actual_time > member.lunch_time:
            member.lunch_time = float("Inf")
        if random() <= 0.5:
            member.snack[0] = randint(self.actual_time, 240)
        else:
            member.snack[1] = True

    def seller_arrives(self):
        seller = self._next_seller_arrives
        self.actual_time = round(self.next_seller_arrives)
        seller.work_place = True
        if self.actual_time == 0:
            print("({})\t[PUESTO]:\t'{}' está instalado en un puesto!".format(self.time(), seller))
        else:
            print("({})\t[PUESTO]:\t'{}' ha instalado un puesto!".format(self.time(), seller))

    def choose_snack_line(self):
        member = self._next_choose_snack_line
        self.actual_time = round(self.next_choose_snack_line)
        first_filter_snack_sellers = filter(lambda seller: seller.food_type == "Snack",
                                            filter(lambda seller: seller.work_place,
                                                   filter(lambda seller: seller.can_sell, member.best_sellers)))
        if isinstance(member, Student):  # Checks conditions for getting into line
            available_snack_sellers = filter(lambda seller: seller.daily_stock >= len(seller.line) + 1,
                                             first_filter_snack_sellers)
            for av_seller in available_snack_sellers:
                if av_seller.waiting_time < member.patience_limit:
                    amount_available_products = len(list(filter(lambda product: product.price <= member.daily_money,
                                                                av_seller.products)))
                    if amount_available_products > 0:
                        av_seller.line.append(member)
                        member.in_line = True
                        print("({})\t[COLA]:\t\t'{}' ha ingresado en la cola de '{}'"
                              .format(self.time(), member, av_seller))
                        return

        else:  # Checks conditions for getting into line
            av_snack_s = list(filter(lambda seller: seller.daily_stock >= len(list(
                filter(lambda memb: isinstance(memb, Functionary), seller.line))) + 1, first_filter_snack_sellers))
            for av_seller in av_snack_s:
                amount_available_products = len(list(filter(lambda product: product.price <= member.daily_money,
                                                            av_seller.products)))
                functionaries_in_line = [elem for elem in av_seller.line if isinstance(elem, Functionary)]
                if amount_available_products > 0 and len(functionaries_in_line) == 0:
                    av_seller.line.insert(0, member)
                    member.in_line = True
                    print("({})\t[COLA]:\t\t'{}' ha ingresado en la cola de {} para comprar un snack"
                          .format(self.time(), member, av_seller))
                    self.check_waiting_times(av_seller)
                    return
                elif amount_available_products > 0:
                    av_seller.line.insert(av_seller.line.index(functionaries_in_line[-1]) + 1, member)
                    member.in_line = True
                    print("({})\t[COLA]:\t\t'{}' ha ingresado en la cola de {} para comprar un snack"
                          .format(self.time(), member, av_seller))
                    self.check_waiting_times(av_seller)
                    return

        self.buy_in_quik_devil("Snack", member)

    def choose_lunch_line(self):
        member = self._next_choose_lunch_line
        self.actual_time = round(self.next_choose_lunch_line)
        first_filter_lunch_sellers = list(
            filter(lambda seller: seller.food_type == "China" or seller.food_type == "Mexicana",
                   filter(lambda seller: seller.work_place,
                          filter(lambda seller: seller.can_sell, member.best_sellers))))

        if isinstance(member, Student):  # Checks conditions for getting into line
            available_lunch_sellers = filter(lambda seller: seller.daily_stock >= len(first_filter_lunch_sellers) + 1,
                                             first_filter_lunch_sellers)
            for av_seller in available_lunch_sellers:
                if av_seller.waiting_time < member.patience_limit:
                    amount_available_products = len(list(filter(lambda product: product.price <= member.daily_money,
                                                                av_seller.products)))
                    if amount_available_products > 0:
                        av_seller.line.append(member)
                        member.in_line = True
                        print("({})\t[COLA]:\t\t'{}' ha ingresado en la cola de '{}' para comprar un almuerzo"
                              .format(self.time(), member, av_seller))
                        return

        else:  # Checks conditions for getting into line
            av_lunch_s = filter(
                lambda s: "{} {}".format(s.name, s.last_name) != member.last_seller and s.daily_stock >= len(list(
                    filter(lambda memb: isinstance(memb, Functionary), s.line))) + 1, first_filter_lunch_sellers)
            for av_seller in av_lunch_s:
                amount_available_products = len(list(filter(lambda product: product.price <= member.daily_money,
                                                            av_seller.products)))
                functionaries_in_line = [elem for elem in av_seller.line if isinstance(elem, Functionary)]
                if amount_available_products > 0 and len(functionaries_in_line) == 0:
                    av_seller.line.insert(0, member)
                    member.in_line = True
                    print("({})\t[COLA]:\t\t'{}' ha ingresado en la cola de '{}' para comprar un almuerzo"
                          .format(self.time(), member, av_seller))
                    self.check_waiting_times(av_seller)
                    return
                elif amount_available_products > 0:
                    av_seller.line.insert(av_seller.line.index(functionaries_in_line[-1]) + 1, member)
                    member.in_line = True
                    print("({})\t[COLA]:\t'{}' ha ingresado en la cola de '{}' para comprar un almuerzo"
                          .format(self.time(), member, av_seller))
                    self.check_waiting_times(av_seller)
                    return

        self.buy_in_quik_devil("Lunch", member)

    def check_waiting_times(self, seller):
        members_to_delete = []
        for i, member in enumerate(seller.line):
            if isinstance(member, Student) and (member.patience_limit <= seller.selling_speed * (i + 1)
                                                or seller.line.index(member) > seller.daily_stock):
                members_to_delete.append(member)
                av_sellers = list(filter(lambda sel: sel.daily_stock >= len(sel.line) + 1,
                                         filter(lambda sel: sel.waiting_time < member.patience_limit,
                                                filter(lambda sel: sel.food_type == sel.food_type,
                                                       filter(lambda sel: sel.work_place,
                                                              filter(lambda sel: sel.can_sell, member.best_sellers))))))
                if len(av_sellers) == 0:
                    member.in_line = False
                    self.buy_in_quik_devil(seller.food_type, member)
                else:
                    for av_seller in av_sellers:
                        amount_available_products = len(list(filter(lambda product: product.price <= member.daily_money,
                                                        av_seller.products)))
                        if amount_available_products > 0:
                            av_seller.line.append(member)
                            member.in_line = True
                            print("({})\t[COLA]:\t\t'{}' ha cambiado de cola: '{}' -> '{}'"
                                  .format(self.time(), member, seller, av_seller))
                            break
        for member in members_to_delete:
            member.times_left_a_line += 1
            del seller.line[seller.line.index(member)]

    def buy_in_quik_devil(self, product_type, member):
        if product_type == "Snack":
            product = choice(list(filter(lambda s: s.price <= member.daily_money, self.quik_devil.snacks)))
            member.snack[1] = True
        else:
            product = choice(list(filter(lambda food: food.price <= member.daily_money, self.quik_devil.foods)))
            member.ate = True
            if random() <= self.sickness_ratio and product.quality(self.actual_time) < 0.2:
                print("({})\t[ENFERMO]:\t'Quik Devil' ha enfermado a '{}'! u.u".format(self.time(), product))
            if 60 <= self.actual_time < 119:
                self.final_lunch_distribution[0] += 1
            elif 120 <= self.actual_time < 179:
                self.final_lunch_distribution[1] += 1
            else:
                self.final_lunch_distribution[2] += 1
        member.daily_money -= product.price
        product_class = type(product).__name__.upper()
        if product_class == "FOOD":
            product_class = "ALMUERZO"
        print("({})\t[{}]:\t'{}' ha comprado un {} en el QuikDevil u.u"
              .format(self.time(), product_class, member, product))

    def seller_attends(self):
        seller = self._next_seller_to_attend
        seller.attending = True
        seller.next_attending = seller.selling_speed + self.actual_time

    def sellers_finishes_attendance(self):
        seller = self._next_seller_attending_finishes
        member_product = seller.attend_member(self.actual_time)
        seller.attending = False
        self.actual_time = seller.next_attending
        if seller.food_type == "China" or seller.food_type == "Mexicana":
            member_product[0].ate = True
            if 60 <= self.actual_time < 119:
                self.final_lunch_distribution[0] += 1
            elif 120 <= self.actual_time < 179:
                self.final_lunch_distribution[1] += 1
            else:
                self.final_lunch_distribution[2] += 1
        else:
            member_product[0].snack[1] = True
        product_type = type(member_product[1]).__name__.upper()
        if product_type == "FOOD":
            product_type = "ALMUERZO"
        print("({})\t[{}]:\t'{}' vendió un {} al '{}'"
              .format(self.time(), product_type, seller, member_product[1],
                      member_product[0]))
        if random() <= self.sickness_ratio and member_product[1].quality(self.actual_time) < 0.2:
            seller.amount_of_toxic_members += 1
            member_product[0].best_sellers_names.pop(member_product[0].best_sellers_names
                                                     .index("{} {}".format(seller.name, seller.last_name)))
            print("({})\t[ENFERMO]:\t'{}' se ha enfermado! u.u... '{}' ha recibido 'la mirada de Lily' (HIMYM)"
                  .format(self.time(), member_product[0], seller))

    # Non-Programmed Event Manager
    def stereo_day_difference(self):
        if len(self.stereo_party_register) == 0:
            return 0
        return self.day_difference(self.stereo_party_register)

    def stereo_party(self):
        print("({})\t[PARTY HARD]:\t ¡CONCHA ESTEREO! PARTY HARD. YOUNG, WILD & FREE lol xd".format(self.time()))
        self.stereo_party_register.append([self.actual_day, self.month])
        self.prices_changed = True
        for product in Product.products:
            product.price *= 1.25

    def extreme_temperatures(self):
        day = choice(["extreme_cold", "extreme_heat"])
        self.get_next_extreme_temperatures()
        if day == "extreme_cold":
            self.lower_products_quality()
        else:
            self.increase_products_putrefaction()

    def get_next_extreme_temperatures(self):
        self.extreme_temperatures_register.append([self.actual_day, self.month])
        if self.actual_day + 18 > 30:
            self.next_extreme_temperatures = round(choice([uniform(1, self.actual_day - 12),
                                                           uniform(self.actual_day + 1, 30)]))
        else:
            self.next_extreme_temperatures = round(uniform(self.actual_day + 1, self.actual_day + 19))
        pass

    def lower_products_quality(self):
        print("({})\t[TEMPERATURA]:\tHOLY F**K TEMPERATURE HAS GONE WILD... "
              "PRODUCTS QUALITY HAVE DECREASED. WATCH OUT".format(self.time()))
        for product in Product.products:
            product.quality_reduction *= 2

    def increase_products_putrefaction(self):
        print("({})\t[TEMPERATURA]:\tHOLY F**K TEMPERATURE HAS GONE WILD... "
              "PRODUCTS HAVE INCREASED THEIR PUTREFACTION RATE. WATCH OUT!".format(self.time()))
        for product in Product.products:
            product.putrafaction_intensification *= 2

    def get_next_burger_rain(self):
        if [self.actual_day, self.month] not in self.burger_rain_register:
            self.burger_rain_register.append([self.actual_day, self.month])
        if len(self.burger_rain_register) != 0:
            self.next_burger_rain = round(expovariate(
                1 / (21 - self.day_difference(self.extreme_temperatures_register))))
        else:
            self.next_burger_rain = round(expovariate(1 / 21))
        if self.next_burger_rain + self.actual_day >= 60:
            self.get_next_burger_rain()
        elif self.next_burger_rain + self.actual_day > 30:
            self.next_burger_rain += self.actual_day - 30
        else:
            self.next_burger_rain += self.actual_day

    def burger_rain(self):
        print("({})\t[BURGER RAIN]:\t¡LLUVIA DE HAMBURGUESAS! COMIDA GRATIS PARA LOS MIEMBROSUC"
              .format(self.time()))
        self.get_next_burger_rain()
        self.sickness_ratio = 0.7
        for member in MemberUC.membersUC:
            member.ate = True
            member.snack[1] = True

    # Statistical Information
    def get_statistical_information(self):
        products_names = []
        amounts_of_products = []
        min_of_products = [None, float("Inf")]
        max_of_products = [None, 0]
        averages = []
        for seller in sellers:
            prom = sum([product.quality(120) for product in seller.products]) / len(seller.products)
            averages.append(prom)
            for product in seller.products:
                if product.product_name not in products_names:
                    products_names.append(product.product_name)
                    amounts_of_products.append(product.total_sold)
                else:
                    amounts_of_products[products_names.index(product.product_name)] += product.total_sold
                if min_of_products[1] > product.min_amount:
                    min_of_products = product.product_name, product.min_amount
                if max_of_products[1] < product.max_amount:
                    max_of_products = product.product_name, product.max_amount
        for snack in self.quik_devil.snacks:
            amounts_of_products[products_names.index(snack.product_name)] += snack.total_sold
            if min_of_products[1] > snack.min_amount:
                min_of_products = snack.product_name, snack.min_amount
            if max_of_products[1] < snack.max_amount:
                max_of_products = snack.product_name, snack.max_amount

        string = str(min_of_products[0]) + ";" + str(min_of_products[1])
        string += ";" + str(max_of_products[0]) + ";" + str(max_of_products[1])
        string += ";" + str(round(sum(amounts_of_products) / len(amounts_of_products)))
        string += ";" + str(len(self.stereo_party_register))
        string += ";" + str(len(self.extreme_temperatures_register)) + ";" + str(len(self.burger_rain_register))
        string += ";" + str(round(self.final_lunch_distribution[0] / (22 * (self.month - 1))))
        string += ";" + str(round(self.final_lunch_distribution[1] / (22 * (self.month - 1))))
        string += ";" + str(round(self.final_lunch_distribution[2] / (22 * (self.month - 1))))
        string += ";" + str(self.amount_students_did_not_lunched[0])
        string += ";" + str(self.amount_students_did_not_lunched[1])
        string += ";" + str(self.amount_students_did_not_lunched[2])
        string += ";" + str(self.amount_students_did_not_lunched[3])
        string += ";" + str(sum(averages) / len(averages))
        string += ";" + str(round(sum([seller.amount_of_toxic_members for seller in sellers]) / len(sellers)))
        string += ";" + str(sum([product.times_decomposed for seller in sellers for product in seller.products]))
        string += ";" + str(sum(map(lambda person: person.times_left_a_line, MemberUC.membersUC))
                            / (22 * (self.month - 1)))
        string += ";" + str(self.amount_of_stock_out / (22 * (self.month - 1)))
        return string