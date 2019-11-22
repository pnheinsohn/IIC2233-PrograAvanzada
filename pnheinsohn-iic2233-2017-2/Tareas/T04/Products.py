from abc import ABCMeta
import math
from Functions import go_product_kwargs


class Product(metaclass=ABCMeta):

    products = []

    def __init__(self, product_name, price, calories, putrefaction_rate, sold_in):
        self.product_name = product_name
        self.initial_price = float(price)
        self.price = self.initial_price
        self.calories = float(calories)
        self.putrefaction_rate = float(putrefaction_rate)
        self.putrafaction_intensification = 1
        self.quality_reduction = 1
        self.sold_in = sold_in
        self.amount_sold = 0
        self.min_amount = float("Inf")
        self.max_amount = 0
        self.total_sold = 0
        self.daily_sold = 0
        self.monthly_non_sold_times = 0
        self.times_decomposed = 0
        Product.products.append(self)

    def quality(self, actual_time):
        asd = (self.calories * (1 - self.putrefaction(actual_time)) ** 4) \
               / ((self.price ** (4 / 5)) * self.quality_reduction)
        return asd

    def putrefaction(self, actual_time):
        rotten = (1 - math.exp(-(actual_time + 180) / self.putrefaction_rate)) * self.putrafaction_intensification
        if rotten >= 1:
            self.times_decomposed += 1
            return 1
        return rotten

    def __repr__(self):
        return "'{}'".format(self.product_name)


class Food(Product):

    def __init__(self, product_name, price, calories, putrefaction_rate, sold_in):
        super().__init__(product_name, price, calories, putrefaction_rate, sold_in)


class Snack(Product):
    def __init__(self, product_name, price, calories, putrefaction_rate, sold_in):
        super().__init__(product_name, price, calories, putrefaction_rate, sold_in)


with open("productos.csv", "r", encoding="utf-8") as products_csv:
    first_filter = list(map(lambda row: row.strip("\n").split("; "), products_csv))
    foods = list(map(lambda row: Food(**go_product_kwargs(row, first_filter)), filter(lambda row: "Fondo" in row,
                                                                                      first_filter)))
    snacks = list(map(lambda row: Snack(**go_product_kwargs(row, first_filter)), filter(lambda row: "Snack" in row,
                                                                                        first_filter)))
