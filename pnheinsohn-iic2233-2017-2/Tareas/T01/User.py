from abc import ABCMeta, abstractmethod
from datetime import datetime, timedelta
import Order
import Market
import Currency


class User(metaclass=ABCMeta):

    list_of_users = []
    list_of_underaged = []
    list_of_traders = []
    list_of_investors = []
    list_of_all_markets = []  # mercados globales compartidos por todos los usuarios

    def __init__(self, username, name, lastname, birthday, orders=''):
        self.order_module = Order
        self.market_module = Market
        self.currency_module = Currency
        self.currency_balances = []  # todas las monedas que posee el usuario
        self.username = username
        self.name = name
        self.last_name = lastname
        self.birth_date = birthday
        self.list_historical_matches = []  # todas las orders concretadas
        self.list_of_my_historical_orders = []
        self.list_of_orders = []  # orders activas del usuario
        self.all_orders_id = ""
        self.commission = 1
        self.orders_id = orders
        self.list_of_markets_registered = []  # mercados en los que el usuario esta registrado
        self.has_priority = False
        self.this_menu = False
        self.showing_markets = False
        self.show_options = {}
        self.list_of_users.append(self)
        User.list_of_users = self.list_of_users

    @abstractmethod
    def display_menu(self):
        pass

    @abstractmethod
    def consultas(self):
        pass

    def run_user(self):
        self._save_all_csv()
        self.this_menu = True
        while self.this_menu:
            self.display_menu()
            choice = input("Ingrese opción: ")
            action = self.show_options.get(choice)
            if action:
                action()
            else:
                print('''"{}" no es una opción válida'''.format(choice))

    def get_age(self):
        birthday = self.birth_date.split("-")
        year = int(datetime.now().strftime("%Y")) - int(birthday[0])
        month = int(datetime.now().strftime("%m"))
        day = int(datetime.now().strftime("%d"))
        if month < int(birthday[1]) or (month == int(birthday[1]) and day > int(birthday[2])):
            year -= 1
        return year

    def mercados_actuales(self):
        print("\nMercados Actuales: ")
        for i in range(len(self.list_of_markets_registered)):
            print(str(i + 1) + ")\t{} ({}), tienes {} orders activas con los siguientes ids: {}"
                  .format(self.list_of_markets_registered[i].name,
                          self.list_of_markets_registered[i].market_id,
                          self.orders_in_market(self.list_of_markets_registered[i].name)[1],
                          self.orders_in_market(self.list_of_markets_registered[i].name)[2]))

    def orders_in_market(self, market_name):  # Útil para cuando el usuario quiera saber sobre sus órdenes en un mercado
        orders_info = []  # Matrix = [0:[orders], 1:Amount of orders, 2:Orders Id]
        list_of_orders = []
        ids = ""
        for order in self.list_of_orders:
            if market_name == order.ticker:
                list_of_orders.append(order)
                ids += str(order.order_id) + ":"
        ids = ids[:-1]
        orders_info.append(list_of_orders)
        orders_info.append(len(list_of_orders))
        orders_info.append(ids)
        return orders_info

    def registrar_mercado(self):
        print('''
            Mercados No Inscritos: ''')
        mercados_no_inscritos = []
        for market in User.list_of_all_markets:
            if market not in self.list_of_markets_registered:
                mercados_no_inscritos.append(market)
                print("             " + str(len(mercados_no_inscritos)) + ": {}".format(market.name))
        print("             0: Ir atrás")
        while True:
            i = input("\nMercado a registrar (N°): ")
            try:
                if i.isdigit():
                    i = int(i)
                    if i == 0:
                        return
                    elif i <= len(mercados_no_inscritos):
                        self.list_of_markets_registered.append(mercados_no_inscritos[i - 1])
                        first_symbol = ""
                        second_symbol = ""
                        for coin in self.currency_balances:
                            if coin.symbol == mercados_no_inscritos[i - 1].name[:3]:
                                coin.amount += 50000
                                first_symbol = coin.symbol
                            elif coin.symbol == mercados_no_inscritos[i - 1].name[3:]:
                                coin.amount += 50000
                                second_symbol = coin.symbol
                        print("\nEl mercado {} ha sido agregado".format(mercados_no_inscritos[i - 1].name))
                        print("¡Además has obtenido 50000 de {} y 50000 de {}!".format(first_symbol, second_symbol))
                        self._save_money_csv()
                        self._save_markets()
                        return
                    else:
                        print("Número inválido, pruebe nuevamente")
                raise ValueError
            except ValueError:
                print("Número inválido, pruebe nuevamente")

    def banco(self):
        print('''
            Banco:
                Esta opción permite enviar criptomonedas a otros usuarios.
                Tan solo debe ingresar el monto, el tipo de moneda, y el 
                destinatario en forma de usuario...
                Actualmente tienes:''')
        for i in range(len(self.currency_balances)):
            print("                " + str(i + 1) + ":", self.currency_balances[i])
        print("                Esto se traduce en {} DCCapital Exchange".format(self._count_money()[0]))
        print("                0: Ir atrás\n")
        while True:
            destinatario = input("Ingrese destinatario (usuario): ")
            entered = False
            if destinatario == "0":
                return
            for user in self.list_of_users:
                if user.username == destinatario and destinatario != self.username:
                    entered = True
                    moneda = input("Ingrese el tipo de moneda (0 para ir atrás): ")
                    try:
                        if moneda.isdigit() and int(moneda) <= len(self.currency_balances):
                            moneda = int(moneda)
                            coin = self.currency_balances[moneda - 1]
                            other_coin = user.currency_balances[moneda - 1]
                            if moneda == 0:
                                return
                            cantidad = input("Ingrese monto: ")
                            try:
                                cantidad = float(cantidad)
                                if cantidad <= coin.amount and not cantidad == 0:
                                    coin.amount -= cantidad * 0.95
                                    other_coin.amount += cantidad * 0.95
                                    print("\n ¡Transacción realizada con éxito!")
                                    self._save_money_csv()
                                    return
                                raise ValueError
                            except ValueError:
                                pass
                        raise ValueError  # when int(moneda.isdigit()) > len(self.currency_balances
                    except ValueError:
                        print("Número inválido, pruebe nuevamente")
                elif destinatario == "0":
                    return
            if not entered:  # When name doest exists
                print("Destinatario inválido, pruebe nuevamente")

    def log_out(self):
        self.this_menu = False
        self._save_all_csv()

    def get_active_orders(self):
        for i in range(len(self.order_module.Order.list_of_orders)):
            print("{})\t {}".format(i + 1, self.order_module.Order.list_of_orders[i]))
        return

    def historical_matches(self):
        for market in self.list_of_all_markets:
            for order in self.order_module.Order.order_history:
                if market.name == order.ticker and order not in market.list_of_matches and order.date_match != "":
                    market.list_of_matches.append(order)
        print('''
            Historial de "Matchs":
            ______________________''')
        print('''Tus matchs:
            ''')
        i = 1
        for match in self.list_historical_matches:
            if i % 2 == 0:
                print(str(int(i / 2)) + ")\tFecha ejecutada: {}, Mercado: {}, Tipo: {},"
                                        " Cantidad: {}, Precio unitario: {}"
                      .format(match.date_match, match.ticker, match.type, match.amount, match.price))
            i += 1
        if len(self.list_historical_matches) == 0:
            print("No has concretado ninguna orden hasta el momento\n")
        print('''Otros matchs:
        ''')
        i = 1
        for market in User.list_of_all_markets:
            for match in market.list_of_matches:
                if match not in self.list_historical_matches:
                    if i % 2 == 0:
                        print(str(int(i / 2)) + ")\tFecha ejecutada: {}, Mercado: {} ({}), "
                                                "Cantidad: {}, Precio unitario: {}"
                              .format(match.date_match, match.ticker, market.market_id, match.amount, match.price))
                    i += 1

    def user_info(self):
        print('''_________________________________
            Usuarios "Underaged":
            ''')
        i = 1
        for user in self.list_of_underaged:
            print(str(i) + ")\tUsuario: {}, \n\tNombre Completo: {} {}"
                  .format(user.username, user.name, user.last_name))
            i += 1
        if len(self.list_of_underaged) == 0:
            print("No hay usuarios 'Underaged' por el momento")
        i = 1
        print('''_______________________________
            Usuarios "Traders":
            ''')
        for user in self.list_of_traders:
            print(str(i) + ")\tUsuario: {}, \n\tNombre Completo: {} {}"
                  .format(user.username, user.name, user.last_name))
            i += 1
        if len(self.list_of_traders) == 0:
            print("No hay usuarios 'Traders' por el momento")
        i = 1
        print('''_________________________________
            Usuarios "Investors":
            ''')
        for user in self.list_of_investors:
            print(str(i) + ")\tUsuario: {},\n\tNombre Completo: {} {}"
                  .format(user.username, user.name, user.last_name))
            i += 1
        if len(self.list_of_investors) == 0:
            print("No hay usuarios 'Investors' por el momento")

    def coin_info(self):
        print('''A continuación se aprecian las siguientes criptomonedas con la que la aplicación trabaja''')
        print('''Para obtener información de una en los respectivos mercados, ingrese su número\n''')
        for i in range(len(self.currency_balances)):
            print("{}.\t{} ({})".format(i + 1, self.currency_balances[i].name, self.currency_balances[i].symbol))
        print("0.\tIr atrás\n")
        while True:
            choice = input("Ingrese número: ")
            try:
                if 0 <= int(choice) <= len(self.currency_balances):
                    coin = self.currency_balances[int(choice) - 1]
                    amount_of_markets = 0
                    print("\nLa moneda {} ({}) está presente en los siguientes mercados:"
                          .format(coin.name, coin.symbol))
                    for market in self.list_of_all_markets:
                        if market.name[:3] == coin.symbol or market.name[3:] == coin.symbol:
                            market.get_orders()
                            market.get_matches()
                            market.actualize_market()
                            for gm in User.list_of_all_markets:
                                if gm.name == market.name:
                                    User.list_of_all_markets[User.list_of_all_markets.index(gm)] = market
                            amount_of_markets += 1
                            print('''{}.{})\t"Orders" activas: {}, Precio actual: {}, Fecha de la última "order": {}'''
                                  .format(amount_of_markets,
                                          market.name,
                                          len(market.list_of_orders),
                                          market.last_price,
                                          market.last_date))
                    return
                else:
                    raise ValueError
            except ValueError:
                print("Opción inválida")

    def info_de_mercados(self):
        print('''A continuación se aprecian los siguientes mercados con la que la aplicación trabaja''')
        print('''Para obtener información de estos ingrese su número\n''')
        for i in range(len(self.list_of_all_markets)):
            print("{}.\t{}, ID: {}".format(i + 1, self.list_of_all_markets[i].name, self.list_of_all_markets[i].market_id))
        print("0.\tIr atrás\n")
        while True:
            choice = input("Ingrese número: ")
            try:
                if 0 <= int(choice) <= len(self.list_of_all_markets):
                    market = self.list_of_all_markets[int(choice) - 1]
                    market.actualize_market()
                    for gm in User.list_of_all_markets:
                        if gm.name == market.name:
                            User.list_of_all_markets[User.list_of_all_markets.index(gm)] = market
                    print('''Mercado {}:\t"Orders" activas: {}, Spread: {}, "Asks": {}, "Bids": {}, '''
                          .format(market.name, len(market.list_of_orders), market.spread,
                                  market.amount_of_asks, market.amount_of_bids), end='')
                    print('''"Best Ask": {}, "Best Bid": {}'''.format(market.best_ask, market.best_bid))
                    return
                else:
                    raise ValueError
            except ValueError:
                print("Opción inválida")

    def get_money(self, list_of_coins):
        if isinstance(list_of_coins[0], Currency.Currency):
            self.currency_balances = list_of_coins
        else:
            for coin in list_of_coins:
                new_coin = self.currency_module.Currency(coin[0], coin[1])
                self.currency_balances.append(new_coin)

    def get_match_money(self, kill_add_list):
        if len(kill_add_list) > 0:
            for ka in kill_add_list:
                kill = ka[0]
                add = ka[1]
                kill_date = datetime.strptime(kill.date_created, "%Y-%m-%d").date()
                add_date = datetime.strptime(add.date_created, "%Y-%m-%d").date()
                new_order = ka[2]
                self.list_of_orders.append(new_order)
                self.list_of_my_historical_orders.append(new_order)
                self.list_historical_matches.append(kill)
                self.list_historical_matches.append(add)
                if new_order != None:
                    if len(self.orders_id) == 0:
                        self.orders_id += new_order.order_id
                        self.all_orders_id += new_order.order_id
                    else:
                        self.orders_id += ":" + new_order.order_id
                        self.all_orders_id += ":" + new_order.order_id
                for user in self.list_of_users:
                    orders_to_delete = []
                    for order in user.list_of_orders:
                        if ((order.order_id == kill.order_id or order.order_id == add.order_id) and
                                        order.type == "ask" and kill_date < add_date) or \
                                ((order.order_id == kill.order_id or order.order_id == add.order_id) and
                                        order.type == "ask" and kill.order_id < add.order_id):
                            for coin in user.currency_balances:
                                if coin.symbol == order.ticker[:3]:
                                    coin.amount += float(kill.amount) * self.commission
                                elif coin.symbol == order.ticker[3:]:
                                    coin.amount -= float(kill.amount) * float(kill.price)
                            orders_to_delete.append(order)
                        elif ((order.order_id == kill.order_id or order.order_id == add.order_id) and
                                        order.type == "ask" and kill_date > add_date) or \
                                ((order.order_id == kill.order_id or order.order_id == add.order_id) and
                                        order.type == "ask" and kill.order_id > add.order_id):
                            for coin in user.currency_balances:
                                if coin.symbol == order.ticker[:3]:
                                    coin.amount += float(kill.amount) * self.commission
                                elif coin.symbol == order.ticker[3:]:
                                    coin.amount -= float(kill.amount) * float(add.price)
                            orders_to_delete.append(order)
                        elif ((order.order_id == kill.order_id or order.order_id == add.order_id) and
                                    order.type == "bid" and kill_date < add_date) or \
                                ((order.order_id == kill.order_id or order.order_id == add.order_id) and
                                         order.type == "bid" and kill.order_id < add.order_id):
                            for coin in user.currency_balances:
                                if coin.symbol == order.ticker[:3]:
                                    coin.amount -= float(kill.amount)
                                elif coin.symbol == order.ticker[3:]:
                                    coin.amount += float(kill.amount) * float(kill.price) * self.commission
                            orders_to_delete.append(order)
                        elif ((order.order_id == kill.order_id or order.order_id == add.order_id) and
                                      order.type == "bid" and kill_date > add_date) or \
                                ((order.order_id == kill.order_id or order.order_id == add.order_id) and
                                         order.type == "bid" and kill.order_id > add.order_id):
                            for coin in user.currency_balances:
                                if coin.symbol == order.ticker[:3]:
                                    coin.amount -= float(kill.amount)
                                elif coin.symbol == order.ticker[3:]:
                                    coin.amount += float(kill.amount) * float(add.price) * self.commission
                            orders_to_delete.append(order)
                    for order in orders_to_delete:
                        user.list_of_orders.pop(user.list_of_orders.index(order))
        self._save_all_csv()
        return

    def _count_money(self):
        my_money = 0
        dcc_money = 0
        for coin in self.currency_balances:
            my_money += coin.amount
        for coin in self.currency_balances:
            if coin.symbol == "DCC":
                dcc_money += coin.amount
        return my_money, dcc_money

    def _save_all_csv(self):
        self._save_users_csv()
        self._save_currency_csv()
        self._save_money_csv()
        self._save_markets()
        for order in self.list_of_orders:
            order._save_orders_csv()
            break
        for order in self.order_module.Order.order_history:
            self.order_module.Order._save_order_history(order)
            break

    def _save_users_csv(self):
        string_of_users = "username: string;name: string;lastname: string;birthday: string;orders: list\n"
        for user in self.list_of_users:
            if not isinstance(user, Investor):
                string_of_users += "{};{};{};{};{}\n".format(user.username,
                                                             user.name,
                                                             user.last_name,
                                                             user.birth_date,
                                                             user.orders_id)
            else:
                string_of_users += "{}INVESTOR;{};{};{};{}\n".format(user.username,
                                                                     user.name,
                                                                     user.last_name,
                                                                     user.birth_date,
                                                                     user.orders_id)
        csv_user_out = open("users.csv", "w", encoding="utf-8")
        csv_user_out.write(string_of_users)
        csv_user_out.close()

    def _save_currency_csv(self):
        string_of_currencies = "symbol: string;name: string\n"
        for currency in self.currency_balances:
            string_of_currencies += "{};{}\n".format(currency.symbol, currency.name)
        csv_currencies_out = open("Currencies.csv", "w", encoding="utf-8")
        csv_currencies_out.write(string_of_currencies)
        csv_currencies_out.close()

    def _save_markets(self):
        string_of_markets = "username: string;name: string\n"
        for user in self.list_of_users:
            if not isinstance(user, Underaged):
                for market in user.list_of_markets_registered:
                    string_of_markets += "{};{}\n".format(user.username, market.name)
        csv_market_out = open("registeredMarkets.csv", "w", encoding="utf-8")
        csv_market_out.write(string_of_markets)
        csv_market_out.close()

    def _save_money_csv(self):
        string_of_money = "username: string;symbol: string;amount: float\n"
        for user in self.list_of_users:
            for coin in user.currency_balances:
                string_of_money += "{};{};{}\n".format(user.username, coin.symbol, coin.amount)
        csv_money_out = open("money.csv", "w", encoding="utf-8")
        csv_money_out.write(string_of_money)
        csv_money_out.close()

    def __repr__(self):
        return "\nUser: " + self.username + " | Orders:" + self.orders_id + " | Priority: " + str(self.has_priority)


class Underaged(User):

    def __init__(self, username, name, lastname, birthday, orders):
        super().__init__(username, name, lastname, birthday, orders)
        self.show_options = {"1": self.mercados_actuales,
                             "2": self.registrar_mercado,
                             "3": self.banco,
                             "4": self.consultas,
                             "5": self.log_out}
        self.list_of_underaged.append(self)
        User.list_of_underaged = self.list_of_underaged

    def display_menu(self):
        print('''
            "Underaged Menu:"
                1: Mercados actuales
                2: Registrar nuevo mercado
                3: Ingresar al banco
                4: Consultas
                5: Regresar al menu principal
            ''')
        return

    def consultas(self):
        print('''
            Consultas:
            1. Ver todas las "orders" activas
            2. Ver el historial de todos los "matchs"
            3. Información sobre usuarios
            4. Información sobre mercados
            5. Información sobre monedas
            6. Atrás
            ''')
        opciones = {"1": self.get_active_orders,
                    "2": self.historical_matches,
                    "3": self.user_info,
                    "4": self.info_de_mercados,
                    "5": self.coin_info}
        choice = input("Ingrese opción: ")
        if choice == "6":
            return
        accion = opciones.get(choice)
        if accion:
            accion()
        else:
            print('''"{}" no es una opción válida'''.format(choice))
            return

    def get_match_money(self, kill_add_list):
        pass

    def registrar_mercado(self):
        print('''
            Mercados No Inscritos: ''')
        mercados_no_inscritos = []
        for market in User.list_of_all_markets:
            if market not in self.list_of_markets_registered:
                mercados_no_inscritos.append(market)
                print("             " + str(len(mercados_no_inscritos)) + ":\t{}".format(market.name))
        print("             0:\tIr atrás")
        while True:
            i = input("\nMercado a registrar (N°): ")
            try:
                if i.isdigit():
                    i = int(i)
                    if i == 0:
                        return
                    elif i <= len(mercados_no_inscritos):
                        self.list_of_markets_registered.append(mercados_no_inscritos[i - 1])
                        print("\nEl mercado {} ha sido agregado".format(mercados_no_inscritos[i - 1].name))
                        self._save_money_csv()
                        self._save_markets()
                        return
                    else:
                        print("Número inválido, pruebe nuevamente")
                raise ValueError
            except ValueError:
                print("Número inválido, pruebe nuevamente")


class Trader(User):

    def __init__(self, username, name, lastname, birthday, orders):
        super().__init__(username, name, lastname, birthday, orders)
        self.daily_orders_left = 15
        self.commission = 0.9
        self.show_options = {"1": self.mercados_actuales,
                             "2": self.registrar_mercado,
                             "3": self.get_my_active_orders,
                             "4": self.registrar_order,
                             "5": self.banco,
                             "6": self.consultas,
                             "7": self.become_investor,
                             "8": self.log_out}
        self.list_of_traders.append(self)
        User.list_of_traders = self.list_of_traders

    def display_menu(self):
        print('''
            "Trader Menu:"
                1: Mercados actuales
                2: Registrar nuevo mercado
                3: Ver/eliminar tus "orders" activas
                4: Agregar una "order" a un mercado inscrito
                5: Ingresar al banco
                6: Consultas
                7: Suscripción premium (convertirse en 'Investor')
                8: Regresar al menu principal
            ''')
        return

    def get_my_active_orders(self):
        print('''
            Tus "Orders" Activas:
            ''')
        for i in range(len(self.list_of_orders)):
            print("{})\t {}".format(i + 1, self.list_of_orders[i]))
        print('''
            Acciones a realizar:
                1. Eliminar una order
                2. Ir atrás
            ''')
        while True:
            choice = input("Opción elegida: ")
            if choice == "1" and len(self.list_of_orders) > 0:
                choice2 = input("¿Cuál desea eliminar? (N°): ")
                try:
                    if 0 < int(choice2) <= len(self.list_of_orders):
                        choice2 = int(choice2)
                        order = self.list_of_orders[choice2 - 1]
                        order_module = self.order_module.Order.list_of_orders
                        if order in order_module:
                            order_module.pop(order_module.index(order))
                        self.list_of_orders.pop(choice2 - 1)
                        for market in self.list_of_all_markets:
                            if order in market.list_of_orders:
                                market.list_of_orders.pop(market.list_of_orders.index(order))
                        num = 0
                        orders_id = self.orders_id.split(":")
                        for i in range(len(orders_id)):
                            if order.order_id == orders_id[i]:
                                num = i
                                break
                        orders_id.pop(num)
                        self.orders_id = ""
                        for id in orders_id:
                            self.orders_id += id + ":"
                        self.orders_id = self.orders_id[:-1]
                        self._save_users_csv()
                        self.order_module.Order._save_orders_csv(order)
                        print("La 'order' con el ID: {} ha sido eliminada".format(order.order_id))
                        return
                    else:
                        raise ValueError
                except ValueError:
                    print("Opción inválida, pruebe nuevamente")

            elif choice == "2":
                return
            else:
                print("Opción inválida, pruebe nuevamente")

    def become_investor(self):
        eligiendo = True
        while eligiendo:
            choice = input("Debes gastar 300.000 DCC ¿Estás seguro que deseas ser un 'Investor'? (si/no): ")
            if choice.lower() == "no":
                return
            elif choice.lower() != "si":
                print("Respuesta inválida, pruebe nuevamente")
            else:
                eligiendo = False
        for coin in self.currency_balances:
            if coin.symbol == "DCC" and coin.amount >= 300000:
                coin.amount -= 300000
                self.list_of_traders.pop(Trader.list_of_traders.index(self))
                self.list_of_users.pop(User.list_of_users.index(self))
                Trader.list_of_traders = self.list_of_traders
                User.list_of_users = self.list_of_users
                self.this_menu = False
                new_investor = Investor(self.username, self.name, self.last_name, self.birth_date, self.orders_id)
                new_investor.get_money(self.currency_balances)
                new_investor.list_of_orders = self.list_of_orders
                new_investor.list_of_markets_registered = self.list_of_markets_registered
                self._save_all_csv()
                new_investor.run_user()
                return
        print("\nNo tienes suficiente dinero para obtener la suscripción premium. "
              "Se necesitan 300.000 DCC, y tu tienes: {}".format(self._count_money()[1]))

    def registrar_order(self):
        self.list_of_markets_registered.sort(key=lambda x: x.market_id)
        print('''\nPara agregar una "order" debe estar inscrito en un mercado, actualmente usted está inscrito en:''')
        for i in range(len(self.list_of_markets_registered)):
            print(str(i + 1) + ")\t {} ({}), en el cual tienes {} orders activas con los siguientes ids: {}"
                  .format(self.list_of_markets_registered[i].name,
                          self.list_of_markets_registered[i].market_id,
                          self.orders_in_market(self.list_of_markets_registered[i].name)[1],
                          self.orders_in_market(self.list_of_markets_registered[i].name)[2]))
        print('''0)\t Ir Atrás\n''')
        daily_orders = 0
        for historical_order in self.list_of_my_historical_orders:
            if historical_order.date_created == str(datetime.now().strftime("%Y-%m-%d")):
                daily_orders += 1
        eligiendo = len(self.list_of_orders) < 5 and daily_orders < 15
        while eligiendo:
            choice = input('''Mercado elegido para registrar una "order": ''')
            try:
                if choice == "0":
                    return
                elif 0 < int(choice) <= len(self.list_of_markets_registered):
                    market = self.list_of_markets_registered[int(choice) - 1]
                    order_type = input('''"Order" type (bid/ask): ''')
                    if order_type != "ask" and order_type != "bid":
                        raise ValueError
                    elif order_type == "ask":
                        buysell = "comprar"
                    else:
                        buysell = "vender"
                    order_amount = input("Ingrese cantidad de {} a {}: ".format(market.name[:3], buysell))
                    order_price = input("Ingrese precio de {} en {} por unidad: ".format(market.name[:3],
                                                                                         market.name[3:]))
                    if order_price.isnumeric() and float(order_price) > 0 and \
                            order_amount.isnumeric() and float(order_amount) > 0:
                        for coin in self.currency_balances:
                            if buysell == "comprar" and market.name[3:] == coin.symbol and \
                                                    float(order_amount) * float(order_price) > coin.amount:
                                print("No tienes suficiente dinero para comprar {} de {}"
                                      .format(order_amount, market.name[:3]))
                                return
                            elif buysell == "vender" and market.name[:3] == coin.symbol and \
                                            float(order_amount) > coin.amount:
                                print("No tienes suficiente dinero para vender {} de {}"
                                      .format(order_amount, market.name[3:]))
                                return
                        self.order_module.Order.order_history.sort(key=lambda x: (x.order_id, x.date_created))
                        order_history = self.order_module.Order.order_history
                        id = 0
                        for i in range(len(order_history)):
                            if int(order_history[i].order_id) >= id:
                                id = int(order_history[i].order_id) + 1
                        new_order = self.order_module.Order(market.name, str(id), order_type, order_amount,
                                                            order_price, datetime.now().strftime("%Y-%m-%d"))
                        self.list_of_orders.append(new_order)
                        self.list_of_my_historical_orders.append(new_order)
                        if len(self.orders_id) == 0:
                            self.orders_id += str(id)
                            self.all_orders_id += str(id)
                        else:
                            self.orders_id += ":" + str(id)
                            self.all_orders_id += ":" + str(id)
                        market.list_of_orders.append(new_order)
                        market.get_orders()
                        market.get_matches()
                        self.get_match_money(market.match_params)
                        for i in range(len(User.list_of_all_markets)):
                            if market.name == User.list_of_all_markets[i].name:
                                User.list_of_all_markets[i] = market
                                print('''\nLa "order" con ID: {} ha sido registrada en el mercado {} exitosamente'''
                                      .format(id, market.name))
                                self._save_users_csv()
                                self.order_module.Order._save_orders_csv(new_order)
                                self.order_module.Order._save_order_history(new_order)
                                return
                raise ValueError
            except ValueError:
                print("Opción inválida, pruebe nuevamente")
        print('''No puedes registrar una nueva "order", ya tienes 5 "orders" activas''', end='')
        print(''', o bien, ya registraste 15 "orders" hoy''')

    def consultas(self):
        print('''
            Consultas:
            1. Ver todas las "orders" activas
            2. Ver el historial de todas las "orders" de la última semana
            3. Ver el historial de todos los "matchs"
            4. Información sobre usuarios
            5. Información sobre mercados
            6. Información sobre monedas
            7. Atrás
            ''')
        opciones = {"1": self.get_active_orders,
                    "2": self.get_order_history,
                    "3": self.historical_matches,
                    "4": self.user_info,
                    "5": self.info_de_mercados,
                    "6": self.coin_info}
        choice = input("Ingrese opción: ")
        if choice == "7":
            return
        accion = opciones.get(choice)
        if accion:
            accion()
        else:
            print('''"{}" no es una opción válida'''.format(choice))
            return

    def get_order_history(self):
        self.order_module.Order.order_history.sort(key=lambda x: x.date_created)
        print('''
            Formatos disponibles para ver las "orders" de los últimos 7 días:

                1. Ver todas las del día
                2. Ver todas en una fecha específica
                3. Ver todas entre dos fechas
                4. Ver todas de un mercado en particular 
                5. Ir atrás
            ''')
        while True:
            choice = input("Opción a elegir: ")
            if choice == "1":
                print('''"\nOrders" del día ({}):'''.format(datetime.now().date()))
                i = 1
                for order in self.order_module.Order.order_history:
                    if order.date_created == str(datetime.now().date()):
                        print("{})\t {}".format(i + 1, order))
                        i += 1
                if i == 1:
                    print('''No se han realizado "orders" hoy, por el momento''')
                return
            elif choice == "2":
                past_date = input("Fecha a elegir (YYYY-MM-DD): ")
                try:
                    past_date = datetime.strptime(past_date, "%Y-%m-%d").date()
                    day1 = (datetime.now().date() - timedelta(days=datetime.now().date().weekday()))
                    day2 = (past_date - timedelta(days=past_date.weekday()))
                    if past_date <= datetime.now().date() and (day1 - day2).days <= 7:
                        print('''\n"Orders" de la fecha {}:'''.format(past_date))
                        i = 1
                        for order in self.order_module.Order.order_history:
                            if order.date_created == str(past_date):
                                print("{})\t {}".format(i, order))
                                i += 1
                        if i == 1:
                            print('''No se realizaron "orders" durante la fecha {}'''.format(past_date))
                        return
                    else:
                        raise ValueError
                except ValueError:
                    print("Fecha inválida, pruebe nuevamente")
            elif choice == "3":
                dates = input("Fechas a elegir (YYYY-MM-DD/YYYY-MM-DD): ")
                try:
                    dates = dates.split("/")
                    if datetime.strptime(dates[0], "%Y-%m-%d").date() <= \
                            datetime.strptime(dates[1], "%Y-%m-%d").date():
                        past_date = datetime.strptime(dates[0], "%Y-%m-%d").date()
                        other_date = datetime.strptime(dates[1], "%Y-%m-%d").date()
                    else:
                        past_date = datetime.strptime(dates[1], "%Y-%m-%d").date()
                        other_date = datetime.strptime(dates[0], "%Y-%m-%d").date()
                    day1 = (datetime.now().date() - timedelta(days=datetime.now().date().weekday()))
                    day2 = (past_date - timedelta(days=past_date.weekday()))
                    if other_date <= datetime.now().date() and (day1 - day2).days <= 7:
                        print('''\n"Orders" entre {} y {}:\n'''.format(past_date, other_date))
                        i = 1
                        for order in self.order_module.Order.order_history:
                            if past_date <= datetime.strptime(order.date_created, "%Y-%m-%d").date() <= other_date:
                                print("{})\t {}".format(i, order))
                                i += 1
                        if i == 1:
                            print('''No se realizaron "orders" entre {} y {}'''.format(past_date, other_date))
                        return
                    else:
                        raise ValueError
                except ValueError:
                    print("Fecha inválida, pruebe nuevamente")
            elif choice == "4":
                market_name = input("Ingrese nombre del mercado: ")
                for market in self.list_of_all_markets:
                    if market.name == market_name:
                        print('''\n"Orders" del mercado {}'''.format(market_name))
                        i = 1
                        for j in range(len(self.order_module.Order.order_history)):
                            order = self.order_module.Order.order_history[j]
                            past_date = datetime.strptime(order.date_created, "%Y-%m-%d").date()
                            day1 = (datetime.now().date() - timedelta(days=datetime.now().date().weekday()))
                            day2 = (past_date - timedelta(days=past_date.weekday()))
                            if order.ticker == market_name and (day1 - day2).days <= 7:
                                print("{})\t {}".format(i, order))
                                i += 1
                        if i == 1:
                            print('''No se encontraron "orders" en el mercado {} durante los últimos 7 días'''
                                  .format(market_name))
                        return
                print("Nombre del mercado no válido, pruebe nuevamente")
            elif choice == "5":
                return
            else:
                print('''"{}" no es una opción válida, pruebe nuevamente'''.format(choice))


class Investor(User):

    def __init__(self, username, name, last_name, birth_date, orders):
        super().__init__(username, name, last_name, birth_date, orders)
        self.has_priority = True
        self.commission = 0.95
        self.show_options = {
                            "1": self.mercados_actuales,
                            "2": self.registrar_mercado,
                            "3": self.get_my_active_orders,
                            "4": self.registrar_order,
                            "5": self.banco,
                            "6": self.consultas,
                            "7": self.log_out
                            }
        self.list_of_investors.append(self)
        User.list_of_investors = self.list_of_investors

    def display_menu(self):
        print('''
            "Investor Menu:"
                1: Mercados actuales
                2: Registrar nuevo mercado
                3: Ver/elminar tus "orders" activas
                4: Agregar una "order" a un mercado inscrito
                5: Ingresar al banco
                6: Consultas
                7: Regresar al menu principal
            ''')
        return

    def get_my_active_orders(self):
        print('''
            Tus "Orders" Activas:
            ''')
        for i in range(len(self.list_of_orders)):
            print("{})\t {}".format(i + 1, self.list_of_orders[i]))
        print('''
            Acciones a realizar:
                1. Eliminar una order
                2. Ir atrás
            ''')
        while True:
            choice = input("Opción elegida: ")
            if choice == "1" and len(self.list_of_orders) > 0:
                choice2 = input("¿Cuál desea eliminar? (N°): ")
                try:
                    if 0 < int(choice2) <= len(self.list_of_orders):
                        choice2 = int(choice2)
                        order = self.list_of_orders[choice2 - 1]
                        order_module = self.order_module.Order.list_of_orders
                        if order in order_module:
                            order_module.pop(order_module.index(order))
                        self.list_of_orders.pop(choice2 - 1)
                        for market in self.list_of_all_markets:
                            if order in market:
                                market.list_of_orders.pop(market.list_of_orders.index(order))
                        num = 0
                        orders_id = self.orders_id.split(":")
                        for i in range(len(orders_id)):
                            if order.order_id == orders_id[i]:
                                num = i
                                break
                        orders_id.pop(num)
                        self.orders_id = ""
                        for id in orders_id:
                            self.orders_id += id + ":"
                        self.orders_id = self.orders_id[:-1]
                        self._save_users_csv()
                        self.order_module.Order._save_orders_csv(order)
                        print("La 'order' con el ID: {} ha sido eliminada".format(order.order_id))
                        return
                    else:
                        raise ValueError
                except ValueError:
                    print("Opción inválida, pruebe nuevamente")

            elif choice == "2":
                return
            else:
                print("Opción inválida, pruebe nuevamente")

    def registrar_order(self):
        self.list_of_markets_registered.sort(key=lambda x: x.market_id)
        print('''\nPara agregar una "order" debe estar inscrito en un mercado, actualmente usted está inscrito en:''')
        for i in range(len(self.list_of_markets_registered)):
            print(str(i + 1) + ")\t {} ({}), en el cual tienes {} orders activas con los siguientes ids: {}"
                  .format(self.list_of_markets_registered[i].name,
                          self.list_of_markets_registered[i].market_id,
                          self.orders_in_market(self.list_of_markets_registered[i].name)[1],
                          self.orders_in_market(self.list_of_markets_registered[i].name)[2]))
        print('''0)\t Ir Atrás\n''')
        daily_orders = 0
        for historical_order in self.list_of_my_historical_orders:
            if historical_order.date_created == str(datetime.now().strftime("%Y-%m-%d")):
                daily_orders += 1
        while True:
            choice = input('''Mercado elegido para registrar una "order": ''')
            try:
                if choice == "0":
                    return
                elif 0 < int(choice) <= len(self.list_of_markets_registered):
                    market = self.list_of_markets_registered[int(choice) - 1]
                    order_type = input('''"Order" type (bid/ask): ''')
                    if order_type != "ask" and order_type != "bid":
                        raise ValueError
                    elif order_type == "ask":
                        buysell = "comprar"
                    else:
                        buysell = "vender"
                    order_amount = input("Ingrese cantidad de {} a {}: ".format(market.name[:3], buysell))
                    order_price = input("Ingrese precio de {} en {} por unidad: ".format(market.name[:3],
                                                                                         market.name[3:]))
                    if order_price.isnumeric() and float(order_price) > 0 and \
                            order_amount.isnumeric() and float(order_amount) > 0:
                        for coin in self.currency_balances:
                            if buysell == "comprar" and market.name[3:] == coin.symbol and \
                                                    float(order_amount) * float(order_price) > coin.amount:
                                print("No tienes suficiente dinero para comprar {} de {}"
                                      .format(order_amount, market.name[:3]))
                                return
                            elif buysell == "vender" and market.name[:3] == coin.symbol and \
                                            float(order_amount) > coin.amount:
                                print("No tienes suficiente dinero para vender {} de {}"
                                      .format(order_amount, market.name[3:]))
                                return
                        self.order_module.Order.order_history.sort(key=lambda x: (x.order_id, x.date_created))
                        order_history = self.order_module.Order.order_history
                        id = 0
                        for i in range(len(order_history)):
                            if int(order_history[i].order_id) >= id:
                                id = int(order_history[i].order_id) + 1
                        new_order = self.order_module.Order(market.name, str(id), order_type, order_amount,
                                                            order_price, datetime.now().strftime("%Y-%m-%d"))
                        self.list_of_orders.append(new_order)
                        self.list_of_my_historical_orders.append(new_order)
                        if len(self.orders_id) == 0:
                            self.orders_id += str(id)
                            self.all_orders_id += str(id)
                        else:
                            self.orders_id += ":" + str(id)
                            self.all_orders_id += ":" + str(id)
                        market.list_of_orders.append(new_order)
                        market.get_orders()
                        market.get_matches()
                        self.get_match_money(market.match_params)
                        for i in range(len(User.list_of_all_markets)):
                            if market.name == User.list_of_all_markets[i].name:
                                User.list_of_all_markets[i] = market
                                print('''\nLa "order" con ID: {} ha sido registrada en el mercado {} exitosamente'''
                                      .format(id, market.name))
                                self._save_users_csv()
                                self.order_module.Order._save_orders_csv(new_order)
                                self.order_module.Order._save_order_history(new_order)
                                return
                raise ValueError
            except ValueError:
                print("Opción inválida, pruebe nuevamente")

    def consultas(self):
        print('''
            Consultas:
            1. Ver todas las "orders" activas
            2. Ver el historial de todas las "orders"
            3. Ver el historial de todos los "matchs"
            4. Información sobre usuarios
            5. Información sobre un mercado
            6. Información sobre monedas
            7. Atrás
            ''')
        opciones = {"1": self.get_active_orders,
                    "2": self.get_order_history,
                    "3": self.historical_matches,
                    "4": self.user_info,
                    "5": self.info_de_mercados,
                    "6": self.coin_info}
        choice = input("Ingrese opción: ")
        if choice == "7":
            return
        accion = opciones.get(choice)
        if accion:
            accion()
        else:
            print('''"{}" no es una opción válida'''.format(choice))
            return

    def get_order_history(self):
        self.order_module.Order.order_history.sort(key=lambda x: x.date_created)
        print('''
            Formatos disponibles para ver las "orders":
                
                1. Ver todas las del día
                2. Ver todas en una fecha específica
                3. Ver todas entre dos fechas
                4. Ver todas de un mercado en particular 
                5. Ir atrás
            ''')
        while True:
            choice = input("Opción a elegir: ")
            if choice == "1":
                print('''\n"Orders" del día ({}):'''.format(datetime.now().date()))
                i = 1
                for order in self.order_module.Order.order_history:
                    if order.date_created == str(datetime.now().date()):
                        print("{})\t {}".format(i + 1, order))
                        i += 1
                if i == 1:
                    print('''No se han realizado "orders" hoy, por el momento''')
                return
            elif choice == "2":
                past_date = input("Fecha a elegir (YYYY-MM-DD): ")
                try:
                    past_date = datetime.strptime(past_date, "%Y-%m-%d").date()
                    print('''\n"Orders" de la fecha {}:'''.format(past_date))
                    i = 1
                    for order in self.order_module.Order.order_history:
                        if order.date_created == str(past_date):
                            print("{})\t {}".format(i, order))
                            i += 1
                    if i == 1:
                        print('''No se realizaron "orders" durante la fecha {}'''.format(past_date))
                    return
                except:
                    print("Fecha inválida, pruebe nuevamente")
            elif choice == "3":
                dates = input("Fechas a elegir (YYYY-MM-DD/YYYY-MM-DD): ")
                try:
                    dates = dates.split("/")
                    if datetime.strptime(dates[0], "%Y-%m-%d").date() <= \
                            datetime.strptime(dates[1], "%Y-%m-%d").date():
                        past_date = datetime.strptime(dates[0], "%Y-%m-%d").date()
                        other_date = datetime.strptime(dates[1], "%Y-%m-%d").date()
                    else:
                        past_date = datetime.strptime(dates[1], "%Y-%m-%d").date()
                        other_date = datetime.strptime(dates[0], "%Y-%m-%d").date()
                    if other_date < datetime.now().date() and \
                            past_date > datetime.strptime("1900-01-01", "%Y-%m-%d").date():
                        print('''\n"Orders" entre {} y {}:\n'''.format(past_date, other_date))
                        i = 1
                        for order in self.order_module.Order.order_history:
                            if past_date <= datetime.strptime(order.date_created, "%Y-%m-%d").date() <= other_date:
                                print("{})\t {}".format(i, order))
                                i += 1
                        if i == 1:
                            print('''No se realizaron "orders" entre {} y {}'''.format(past_date, other_date))
                        return
                    else:
                        raise ValueError
                except ValueError:
                    print("Fecha inválida, pruebe nuevamente")
            elif choice == "4":
                market_name = input("Ingrese nombre del mercado: ")
                for market in self.list_of_all_markets:
                    if market.name == market_name:
                        print('''\n"Orders" del mercado {}'''.format(market_name))
                        i = 1
                        for j in range(len(self.order_module.Order.order_history)):
                            order = self.order_module.Order.order_history[j]
                            if order.ticker == market_name:
                                print("{})\t {}".format(i, order))
                                i += 1
                        if i == 1:
                            print('''No se encontraron "orders" en el mercado {}'''.format(market_name))
                        return
                print("Nombre del mercado no válido, pruebe nuevamente")
            elif choice == "5":
                return
            else:
                print('''"{}" no es una opción válida, pruebe nuevamente'''.format(choice))
