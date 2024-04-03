import csv
import sys
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

    # @shares.deleter
    # def shares(self):
    #     # delete
    #     del self._shares

    @property
    def price(self):
        return self._price

    @price.setter
    def price(self, value):
        if not isinstance(value, self._types[2]):
            raise TypeError(f"Expected a {self._types[2].__name__}")
        if value < 0:
            raise ValueError("Price must be >= 0")
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

    def __repr__(self):
        return f"{self.__class__.__name__}('{self.name}', {self.shares}, {self.price})"

    def __eq__(self, other):
        return isinstance(other, Stock) and (self.name, self.shares, self.price) == (
            other.name,
            other.shares,
            other.price,
        )


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


def print_table(records, fields, formatter):
    formatter.headings(fields)
    for r in records:
        rowdata = [getattr(r, fieldname) for fieldname in fields]
        formatter.row(rowdata)


# would be really cool to allow for writing to a different output file


class TableFormatter:
    def headings(self, headers):
        raise NotImplementedError()

    def row(self, rowdata):
        raise NotImplementedError()


class TextTableFormatter(TableFormatter):
    def headings(self, headers):
        print(" ".join("%10s" % h for h in headers))
        print(("-" * 10 + " ") * len(headers))

    def row(self, rowdata):
        print(" ".join("%10s" % d for d in rowdata))


class CSVTableFormatter(TableFormatter):
    def headings(self, headers):
        print(",".join("%s" % h for h in headers))

    def row(self, rowdata):
        print(",".join("%s" % d for d in rowdata))


class HTMLTableFormatter(TableFormatter):
    def headings(self, headers):
        print(
            "<tr>" + " " + " ".join("<th>%s</th>" % h for h in headers) + " " + "</tr>"
        )

    def row(self, rowdata):
        print(
            "<tr>" + " " + " ".join("<td>%s</td>" % d for d in rowdata) + " " + "</tr>"
        )


str_to_formatter_map = {
    "text": TextTableFormatter,
    "csv": CSVTableFormatter,
    "html": HTMLTableFormatter,
}


def create_formatter(type):
    if type in str_to_formatter_map:
        AttributeError("Please provide a valid key: 'html', 'csv', or 'html'")

    return str_to_formatter_map[type]()


# makes a temporary patch to sys.stdout to cause all output to redirect to a different file
class redirect_stdout:
    # accepts a file object
    def __init__(self, out_file):
        self.out_file = out_file

    def __enter__(self):
        # save the sys.stdout prior to over writing it
        self.stdout = sys.stdout
        sys.stdout = self.out_file
        return self.out_file

    def __exit__(self, ty, val, tb):
        sys.stdout = self.stdout
