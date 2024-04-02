import csv
from decimal import Decimal

COL_LEN = 10


# wrap and return new version / instance of class
# and all we need to do is just add this decorator to a diff class that
# we want to provide this interface to create new instances
def read_instance_from_row(cls):
    @classmethod
    def from_row(cls, row):
        # say class and not the instance, between types is on the class itself
        # and not an instance
        values = [f(v) for f, v in zip(cls._types, row)]
        return cls(*values)

    cls.from_row = from_row
    return cls


@read_instance_from_row
class Stock:
    __slots__ = ("name", "_shares", "_price")
    # Class variables such as this are sometimes used as a customization
    # mechanism when inheritance is used
    _types = (str, int, float)

    def __init__(self, name, shares, price) -> None:
        self.name = name
        self.shares = shares
        self.price = price

    # turn this to an attribute
    # def cost(self):
    #     return round(self.shares * self.price, 2)

    @property
    def shares(self):
        return self._shares

    @shares.setter
    def shares(self, value):
        if not isinstance(value, self._types[1]):
            raise TypeError(f"Expected an {self._types[1].__name__}")
        if value < 0:
            raise ValueError("shares must be >= 0")
        self._shares = value

    @property
    def price(self):
        return self._price

    @price.setter
    def price(self, value):
        if not isinstance(value, self._types[2]):
            raise TypeError(f"Expected a {self._types[2].__name__}")
        if value < 0:
            raise ValueError("price must be >= 0")
        self._price = value

    @property
    def cost(self):
        return round(self.shares * self.price, 2)

    def sell(self, vol):
        if self.shares == 0:
            return "No shares to sell"
        elif vol > self.shares:
            sold = self.shares
            self.shares = 0
            return f"Sold all {sold} shares"
        else:
            self.shares -= vol
            return f"Sold {vol} shares"


# types can easily be changed in a subclass
class DStock(Stock):
    types = (str, int, Decimal)


# we can use these class methods to put a highly uniform instance creation interface
# on a wide variety of classes (even better with decorators) and write
# general purpose utility functions that use them


def read_portfolio(filename):
    data = []
    with open(filename) as f:
        rows = csv.reader(f)
        next(rows)

        # was doing it here before creating the instance, but now can do
        # this data should probably be related to the instances we are creating
        # but they only need to exist on the class and not the instances
        # conv = [str, int, float]
        # for r in rows:
        #     data.append(Stock(*[fn(v) for fn, v in zip(conv, r)]))

        for r in rows:
            data.append(Stock.from_row(r))  # type: ignore

    return data


def preprocess_headers(func):
    def wrapper(p, headers=None):
        filtered_headers = headers if headers else vars(p[0]).keys()
        return func(p, filtered_headers)

    return wrapper


@preprocess_headers
def _print_headers(_, headers):
    print(" ".join(f"{h:>{COL_LEN}}" for h in headers))


@preprocess_headers
def _print_seps(_, headers):
    print(" ".join("-" * COL_LEN for _ in headers))


@preprocess_headers
def _print_portfolio(p, headers):
    for item in p:
        print(" ".join(f"{getattr(item,header):>{COL_LEN}}" for header in headers))


def printer(fns, v, headers):
    for fn in fns:
        fn(v, headers)


def print_portfolio(p, headers=None):
    fns = [_print_headers, _print_seps, _print_portfolio]
    printer(fns, p, headers)
