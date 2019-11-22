import Order
from datetime import datetime as dt


class Market:

    list_of_markets = []
    market_id = 0

    def __init__(self, name):
        self.order_module = Order
        self.list_of_orders = []
        self.match_params = []
        self.name = name
        self.amount_of_bids = 0
        self.amount_of_asks = 0
        self.amount_of_money = 0
        self.last_price = 0
        self.last_date = ""
        self.best_bid = 0
        self.best_ask = 0
        self.lowest_bid_price = 0
        self.highest_ask_price = 0
        self.spread = 0
        self.list_of_matches = []
        self.get_orders()
        self.list_of_markets.append(self)
        self.market_id = Market.market_id
        Market.market_id += 1
        Market.list_of_markets = self.list_of_markets

    def get_orders(self):
        for order in self.order_module.Order.list_of_orders:
            if order.ticker == self.name and order not in self.list_of_orders:
                self.list_of_orders.append(order)
                self.last_price = float(order.price)
                self.last_date = order.date_created
                if order.type == "ask":
                    self.amount_of_asks += 1
                elif order.type == "bid":
                    self.amount_of_bids += 1

    def actualize_market(self):
        self.list_of_orders.sort(key=lambda x: x.date_created)
        if len(self.list_of_orders) > 0:
            last_order = self.list_of_orders[len(self.list_of_orders) - 1]
            self.last_price = float(last_order.price)
            self.last_date = last_order.date_created
        if self.best_bid == "" or self.best_ask == "" or self.spread == "" or self.lowest_bid_price == "" or self.highest_ask_price == "":
            self.best_bid = 0
            self.best_ask = 0
            self.spread = 0
            self.lowest_bid_price = 0
            self.highest_ask_price = 0
        self.amount_of_asks = 0
        self.amount_of_bids = 0
        for order in self.list_of_orders:
            if order.type == "ask" and float(order.price) > self.best_bid:
                self.best_bid = float(order.price)
                self.amount_of_asks += 1
                if float(order.price) > self.highest_ask_price:
                    self.highest_ask_price = float(order.price)
            elif order.type == "bid" and (float(order.price) < self.best_ask or self.best_ask == 0):
                self.best_ask = float(order.price)
                self.amount_of_bids += 1
                if float(order.price) < self.lowest_bid_price or self.lowest_bid_price == 0:
                    self.lowest_bid_price = float(order.price)
            elif order.type == "ask":
                self.amount_of_asks += 1
            elif order.type == "bid":
                self.amount_of_bids += 1
        self.spread = self.lowest_bid_price - self.highest_ask_price
        if self.best_bid == 0:
            self.best_bid = ""
        if self.best_ask == 0:
            self.best_ask = ""
        if self.spread == 0:
            self.spread = ""
        if self.lowest_bid_price == 0:
            self.lowest_bid_price = ""
        if self.highest_ask_price == 0:
            self.highest_ask_price = ""
        self.get_matches()

    def get_matches(self):
        f = "%Y-%m-%d"
        already_checked = []
        kill_add = []
        self.match_params = []
        for o in self.list_of_orders:
            for oo in self.list_of_orders:
                if o.type != oo.type and float(o.amount) <= float(oo.amount) and not oo in already_checked and \
                        ((o.type == "ask" and float(o.price) >= float(oo.price)) or
                             (o.type == "bid" and float(o.price) <= float(oo.price))):
                    kill_add.append([o, oo])
                elif o.type != oo.type and float(o.amount) > float(oo.amount) and not oo in already_checked and \
                        ((o.type == "ask" and float(o.price) >= float(oo.price)) or
                             (o.type == "bid" and float(o.price) <= float(oo.price))):
                    kill_add.append([oo, o])
            already_checked.append(o)
        self.actualize_orders_from_market_and_orders(kill_add)

    def actualize_orders_from_market_and_orders(self, killaddlist):
        for ka in killaddlist:
            kill = ka[0]
            add = ka[1]
            kill.date_match = dt.now().date().strftime("%Y-%m-%d")
            add.date_match = dt.now().date().strftime("%Y-%m-%d")
            self.list_of_matches.append(kill)
            self.list_of_matches.append(add)
            new_order = None
            if float(add.amount) - float(kill.amount) != 0:
                amount = float(add.amount) - float(kill.amount)
                order_id = 0
                for order in self.order_module.Order.list_of_orders:
                    if int(order.order_id) >= order_id:
                        order_id = int(order.order_id) + 1
                new_order = self.order_module.Order(add.ticker, str(order_id), add.type,
                                                    amount, add.price, add.date_created)
                self.list_of_orders.append(new_order)
            self.list_of_orders.pop(self.list_of_orders.index(kill))
            self.list_of_orders.pop(self.list_of_orders.index(add))
            for i in range(len(Market.list_of_markets)):
                if Market.list_of_markets[i].name == self.name:
                    Market.list_of_markets[i] = self
            for order in self.order_module.Order.list_of_orders:
                if order.order_id == kill.order_id or order.order_id == add.order_id:
                    self.order_module.Order.list_of_orders.pop(self.order_module.Order.list_of_orders.index(order))
            for order in self.order_module.Order.order_history:
                if order.order_id == kill.order_id or order.order_id == add.order_id:
                    order.date_match = dt.now().date().strftime("%Y-%m-%d")
            self.match_params.append([kill, add, new_order])

    def __repr__(self):
        return "Name: " + self.name + " Market ID: " + str(self.market_id)
