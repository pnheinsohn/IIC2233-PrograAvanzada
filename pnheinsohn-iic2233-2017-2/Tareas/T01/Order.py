class Order:

    list_of_orders = []
    order_history = []

    def __init__(self, ticker, order_id, type, amount, price, date_created, date_match=''):
        self.ticker = ticker
        self.order_id = order_id
        self.type = type
        self.amount = amount
        self.price = price
        self.date_created = date_created
        self.date_match = date_match
        self.list_of_orders.append(self)
        self.order_history.append(self)
        self.list_of_orders.sort(key=lambda x: x.date_created)
        self.order_history.sort(key=lambda  x:x.date_created)
        Order.order_history = self.order_history
        Order.list_of_orders = self.list_of_orders

    def _save_orders_csv(self):
        string_of_orders = "ticker: string;order_id: int;type: string;amount: float;" \
                                "price: float;date_created: string;date_match: string\n"
        for order in self.list_of_orders:
            string_of_orders += "{};{};{};{};{};{};{}\n".format(order.ticker,
                                                                order.order_id,
                                                                order.type,
                                                                order.amount,
                                                                order.price,
                                                                order.date_created,
                                                                order.date_match)
        Order.string_of_orders = string_of_orders
        csv_orders_out = open("orders.csv", "w", encoding="utf-8")
        csv_orders_out.write(string_of_orders)
        csv_orders_out.close()

    def _save_order_history(self):
        string_of_order_history = "ticker: string;order_id: int;type: string;amount: float;" \
                                       "price: float;date_created: string;date_match: string\n"
        for order in self.order_history:
            string_of_order_history += "{};{};{};{};{};{};{}\n".format(order.ticker,
                                                                       order.order_id,
                                                                       order.type,
                                                                       order.amount,
                                                                       order.price,
                                                                       order.date_created,
                                                                       order.date_match)
        csv_other_order_out = open("orderHistory.csv", "w", encoding="utf-8")
        csv_other_order_out.write(string_of_order_history)
        csv_other_order_out.close()

    def __repr__(self):
        return "ID: {}, Mercado: {}, Tipo: {}, Precio: {}, Cantidad: {}, Fecha de Creación: {}"\
            .format(self.order_id, self.ticker, self.type, self.price, self.amount, self.date_created)
