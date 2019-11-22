import User
import Order
import Market
import Currency
import datetime


class MainMenu:
    def __init__(self):
        self.user = User
        self.order = Order
        self.market = Market
        self.currency = Currency
        self.list_of_coins = [["DCC", "DCCapital Exchange"]]
        self.deleted_orders = []
        self.pre_orders_review = []
        self.list_of_trader = []
        self.list_of_matches = []
        self.running = bool
        self.show_options = {
                            "1": self.log_in,
                            "2": self.create_new_user,
                            "3": self.exit
                            }

    def display_menu(self):
        print('''
            Menu:
                1: Ingresar
                2: Crear cuenta
                3: Salir        
            ''')

    def run_main_menu(self):
        self.running = True
        while self.running:
            self.display_menu()
            choice = input("Ingrese opción: ")
            action = self.show_options.get(choice)
            if action:
                action()
            else:
                print("{} no es una opción válida".format(choice))

    def log_in(self):
        username = input("Ingresar nombre de usuario: ")
        for user in self.user.User.list_of_users:
            if username == user.username:
                self.user.User.this_menu = True
                while self.user.User.this_menu:
                    if user.get_age() < 18:
                        self.user.Underaged.run_user(user)
                    elif user.has_priority:
                        self.user.Investor.run_user(user)
                    else:
                        self.user.Trader.run_user(user)
                    return
        print("Nombre de usuario inválido, pruebe nuevamente")
        return

    def create_new_user(self):
        username = input("Ingrese nombre de usuario: ")
        for user in self.user.User.list_of_users:
            if username in user.username:
                print("Nombre de usuario ya existe, pruebe nuevamente")
                return
        name = input("Ingrese su nombre: ")
        lastname = input("Ingrese su apellido: ")
        birthday = input("Ingrese su fecha de nacimiento de la siguiente forma -> YYYY-MM-DD: ")
        birth_list = birthday.split("-")
        try:
            if birthday != str(datetime.datetime.strptime(birthday, "%Y-%m-%d").date()):
                raise ValueError
            elif int(birth_list[0]) < 1900 or int(birth_list[0]) > 2017:
                raise ValueError
            else:
                self.user_assignment(username, name, lastname, birthday)
                for user in self.user.User.list_of_traders:
                    if user.username == username:
                        for coin in user.currency_balances:
                            if coin.symbol == "DCC":
                                coin.amount += 100000
                        user._save_users_csv()
                        user._save_money_csv()
                print("\n¡Usuario creado exitosamente! Por favor inicie sesión")
                return
        except ValueError:
            print("Fecha inválida, pruebe nuevamente")
            return

    def exit(self):
        self.running = False
        for user in self.user.User.list_of_users:
            user._save_all_csv()
            break
        print("Gracias por usar nuestra aplicación ¡Esperamos verte pronto!")

    def instantiate_users(self):  # Abre el archivo 'users.csv' y
        users = [line.split(';') for line in open('users.csv', 'r', encoding='UTF-8').read().split('\n')]
        list_of_kwargs = self._kwargs_master(users)
        for kwarg in list_of_kwargs:
            self.user_assignment(**kwarg)
        self._destroy_underaged_pair_orders()

    def instantiate_orders(self):  # creo las orders anteriores
        orders = [line.split(';') for line in open('orders.csv', 'r', encoding='UTF-8').read().split('\n')]
        list_of_kwargs = self._kwargs_master(orders)
        for kwarg in list_of_kwargs:
            self.order.Order(**kwarg)
        self.order.Order.list_of_orders.sort(key=lambda x: x.date_created)

    def instantiate_currencies(self):  # creo las currencies anteriores
        currencies = [line.split(';') for line in open('Currencies.csv', 'r', encoding='UTF-8').read().split('\n')]
        list_of_kwargs = self._kwargs_master(currencies)
        for kwarg in list_of_kwargs:
            values = kwarg.values()
            values_to_append = []
            short_value = ""
            long_value = ""
            for value in values:
                if len(value) == 3:
                    short_value = value
                else:
                    long_value = value
                if len(short_value) != 0 and short_value != "DCC" and len(long_value) != 0:
                    values_to_append.append(short_value)
                    values_to_append.append(long_value)
                    self.list_of_coins.append(values_to_append)
                    short_value = ""
                    long_value = ""

        for i in range(len(self.list_of_coins)):
            for j in range(len(self.list_of_coins)):
                if self.list_of_coins[i] != self.list_of_coins[j]:
                    self.market.Market(self.list_of_coins[i][0] + self.list_of_coins[j][0])

    def instantiate_money(self):
        try:
            money = [line.split(';') for line in open('money.csv', 'r', encoding='UTF-8').read().split('\n')]
            list_of_kwargs = self._kwargs_master(money)
            for kwarg in list_of_kwargs:
                for user in self.user.User.list_of_users:
                    if kwarg["username"] == user.username:
                        for coin in user.currency_balances:
                            if kwarg["symbol"] == coin.symbol:
                                coin.amount = float(kwarg["amount"])
        except:
            return

    def instantiate_historical_orders(self):
        try:
            orders = [line.split(';') for line in open('orderHistory.csv', 'r', encoding='UTF-8').read().split('\n')]
            list_of_kwargs = self._kwargs_master(orders)
            new_order = NotImplemented
            for kwarg in list_of_kwargs:
                new_order = self.order.Order(**kwarg)
                self.order.Order.list_of_orders.pop(self.order.Order.list_of_orders.index(new_order))
            orders_to_del = []
            self.order.Order.order_history.sort(key=lambda x: (x.order_id, x.date_created))
            for i in range(len(self.order.Order.order_history) - 1):
                o = self.order.Order.order_history[i]
                oo = self.order.Order.order_history[i + 1]
                if o.order_id == oo.order_id and o.ticker == oo.ticker and o.price == oo.price and \
                                o.date_created == oo.date_created and o.amount == o.amount and o.type == oo.type and \
                                o.date_match == oo.date_match and o not in orders_to_del:
                    orders_to_del.append(o)
            for order in orders_to_del:
                if order in self.order.Order.order_history:
                    self.order.Order.order_history.pop(self.order.Order.order_history.index(order))
            self.order.Order.order_history.sort(key=lambda x: x.date_created)
            self.order.Order._save_order_history(new_order)
            for user in self.user.User.list_of_users:
                list_of_orders = user.all_orders_id.split(":")
                if list_of_orders[0] == "":
                    return
                for i in range(len(list_of_orders)):
                    for order in self.order.Order.order_history:
                        if order.order_id == list_of_orders[i]:
                            user.list_of_my_historical_orders.append(order)
        except:
            return

    def instantiate_registered_markets(self):
        try:
            markets = [line.split(';') for line in open('registeredMarkets.csv', 'r', encoding="utf-8").read().split('\n')]
            list_of_kwargs = self._kwargs_master(markets)
            for user in self.user.User.list_of_users:
                user_markets = []
                user_markets_to_add = []
                for market in user.list_of_markets_registered:
                    user_markets.append(market.name)
                for kwarg in list_of_kwargs:
                    if kwarg["username"] == user.username:
                        if kwarg["name"] not in user_markets:
                            user_markets_to_add.append(kwarg["name"])
                for market in user.list_of_all_markets:
                    if market.name in user_markets_to_add:
                        user.list_of_markets_registered.append(market)
        except:
            return

    def user_assignment(self, username, name, lastname, birthday, orders=''):  # creo los users anteriores
        birth_date = birthday.split("-")
        year = int(datetime.datetime.now().strftime("%Y")) - int(birth_date[0])
        month = int(datetime.datetime.now().strftime("%m"))
        day = int(datetime.datetime.now().strftime("%d"))
        if month < int(birth_date[1]) or (month == int(birth_date[1]) and day > int(birth_date[2])):
            year -= 1
        if year < 18:
            new_user = self.user.Underaged(username, name, lastname, birthday, orders)
            self.destroy_underaged_orders(new_user)
        elif username[-8:] == "INVESTOR":
            investor_username = username[:-8]
            new_user = self.user.Investor(investor_username, name, lastname, birthday, orders)
            new_user.has_priority = True
        else:
            new_user = self.user.Trader(username, name, lastname, birthday, orders)
            self.go_to_order_preview(new_user)
        self.user.User.get_money(new_user, self.list_of_coins)
        return type(self.user)

    def destroy_underaged_orders(self, underaged):  # aca destruyo todas las orders de los usuarios underaged
        if len(underaged.orders_id) != 0:
            list_of_orders = underaged.orders_id.split(":")
            for i in range(len(list_of_orders)):
                for order in self.order.Order.list_of_orders:
                    if order.order_id == list_of_orders[i]:
                        self.deleted_orders.append(order)
                        self.order.Order.list_of_orders.pop(self.order.Order.list_of_orders.index(order))
            underaged.orders_id = ""

    def go_to_order_preview(self, trader):  # add orders from traders and investors for being checked
        list_of_orders = trader.orders_id.split(":")
        if list_of_orders[0] == "":
            return
        for i in range(len(list_of_orders)):
            for order in self.order.Order.list_of_orders:
                if order.order_id == list_of_orders[i] and order.order_id not in self.pre_orders_review:
                    self.pre_orders_review.append(order)

    def _destroy_underaged_pair_orders(self):  # checks the matches between wrong orders, taking them out
        for i in range(len(self.pre_orders_review)):
            order = self.pre_orders_review[i]
            for j in range(len(self.deleted_orders)):
                del_order = self.deleted_orders[j]
                if order.price == del_order.price and order.amount == del_order.amount and order != del_order:
                    self.order.Order.list_of_orders.pop(self.order.Order.list_of_orders.index(order))
        self._add_trader_orders_and_markets_to_user()

    def _add_trader_orders_and_markets_to_user(self):  # add orders and markets to user
        for market in self.market.Market.list_of_markets:
            self.user.User.list_of_all_markets.append(market)
        for user in self.user.User.list_of_users:
            if len(user.orders_id) > 0:
                list_of_orders = user.orders_id.split(":")
                for order in self.order.Order.list_of_orders:
                    if order.order_id in list_of_orders and order.order_id not in user.list_of_orders:
                        user.list_of_orders.append(order)
                        for market in self.market.Market.list_of_markets:
                            if market.name == order.ticker and market not in user.list_of_markets_registered:
                                user.list_of_markets_registered.append(market)
        self._get_matches()

    def _get_matches(self):  # Agarra las orders que ya se ejecutaron, las guarda y elimina
        for order in self.order.Order.list_of_orders:
            if order.date_match != "":
                for user in self.user.User.list_of_users:
                    if order in user.list_of_orders and order.type == "bid":
                        for user_coin in user.currency_balances:
                            if order.ticker[:3] == user_coin.symbol:
                                user_coin.amount -= float(order.amount)
                            elif order.ticker[3:] == user_coin.symbol:
                                user_coin.amount += float(order.price)
                        user.list_historical_matches.append(order)
                        user.list_historical_matches.sort(key=lambda x: x.date_match)
                        user.list_of_orders.pop(user.list_of_orders.index(order))
                        break
                    elif order in user.list_of_orders and order.type == "ask":
                        for user_coin in user.currency_balances:
                            if order.ticker[:3] == user_coin.symbol:
                                user_coin.amount += float(order.amount)
                            elif order.ticker[3:] == user_coin.symbol:
                                user_coin.amount -= float(order.price)
                        user.list_historical_matches.append(order)
                        user.list_historical_matches.sort(key=lambda x: x.date_match)
                        user.list_of_orders.pop(user.list_of_orders.index(order))
                        break
                self.list_of_matches.append(order)
        self._add_matches_to_respective_places()

    def _add_matches_to_respective_places(self):
        for order in self.list_of_matches:
            self.order.Order.list_of_orders.pop(self.order.Order.list_of_orders.index(order))
        if len(self.list_of_matches) > 0:  # en caso de que no haya ningun match en el csv
            self.list_of_matches.sort(key=lambda x: x.date_match)
            for user in self.user.User.list_of_users:
                for market in user.list_of_all_markets:
                    for i in range(len(user.list_of_markets_registered)):
                        if market.name == user.list_of_markets_registered[i].name:
                            user.list_of_markets_registered[i] = market
            for user in self.user.User.list_of_users:
                user._save_markets()
                break
        self._get_order_ids_right()

    def _get_order_ids_right(self):
        for user in self.user.User.list_of_users:
            actual_ids = []
            user.orders_id = ""
            for user_order in user.list_of_orders:
                actual_ids.append(user_order.order_id)
            for i in range(len(actual_ids)):
                user.orders_id += str(actual_ids[i]) + ":"
            user.orders_id = user.orders_id[:-1]
            user.all_orders_id = user.orders_id[:-1]
        for order in self.order.Order.order_history:
            order._save_orders_csv()
            break

    def _kwargs_master(self, list_to_turn):  # obtiene los kwargs para ser entregados
        list_of_headers = []
        list_of_kwargs = []
        for i in range(len(list_to_turn)):
            if i == 0:
                for j in range(len(list_to_turn[0])):
                    header = ""
                    for string in list_to_turn[0][j]:
                        if string != ":":
                            header += string
                        else:
                            list_of_headers.append(header)
                            break
            elif i < len(list_to_turn) - 1:
                kwargs = {}
                for j in range(len(list_to_turn[i])):
                    kwarg1 = {list_of_headers[j]: list_to_turn[i][j]}
                    kwargs.update(kwarg1)
                list_of_kwargs.append(kwargs)
        return list_of_kwargs

menu = MainMenu()
MainMenu.instantiate_orders(menu)
MainMenu.instantiate_currencies(menu)
MainMenu.instantiate_users(menu)
MainMenu.instantiate_money(menu)
MainMenu.instantiate_historical_orders(menu)
MainMenu.instantiate_registered_markets(menu)
menu.run_main_menu()
