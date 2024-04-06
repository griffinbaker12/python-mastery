import csv
from abc import ABC, abstractmethod

from soln3_1 import TableFormatter, str_to_formatter_map


def read_instance_from_row(cls):
    @classmethod
    def from_row(cls, row):
        # say class and not the instance, between types is on the class itself
        # and not an instance
        values = [f(v) for f, v in zip(cls._types, row)]
        return cls(*values)

    cls.from_row = from_row
    return cls


def print_table_with_formats(records, fields, formats, formatter):
    # no guarantee this works even if it inherits from the proper base blass
    if not issubclass(type(formatter), TableFormatter):
        raise TypeError("Expected a table formatter")

    formatter.headings(fields)
    for r in records:
        rowdata = [f % getattr(r, fieldname) for f, fieldname in zip(formats, fields)]
        formatter.row(rowdata)


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


class CSVParser(ABC):
    def parse(self, filename):
        records = []
        with open(filename) as f:
            rows = csv.reader(f)
            headers = next(rows)
            for row in rows:
                record = self.make_record(headers, row)
                records.append(record)
        return records

    @abstractmethod
    def make_record(self, headers, row):
        pass


class DictCSVParser(CSVParser):
    def __init__(self, types):
        self.types = types

    def make_record(self, headers, row):  # type: ignore
        return {name: func(val) for name, func, val in zip(headers, self.types, row)}


class InstanceCSVParser(CSVParser):
    def __init__(self, cls):
        self.cls = cls

    def make_record(self, headers, row):
        return self.cls.from_row(row)


def read_csv_as_instances(file, instance):
    parser = InstanceCSVParser(instance)
    return parser.parse(file)


def read_csv_as_dicts(file, types):
    parser = DictCSVParser(types)
    return parser.parse(file)


# meant to be mixed with a class that provides the required row method
class ColumnFormatMixin:
    formats = []

    def row(self, rowdata):
        rowdata = [(fmt % d) for fmt, d in zip(self.formats, rowdata)]
        super().row(rowdata)  # type: ignore


class UpperHeadersMixin:
    def headings(self, headers):
        super().headings([h.upper() for h in headers])  # type: ignore


def create_formatter_with_mixins(type, column_formats=None, upper_headers=False):
    if type not in str_to_formatter_map:
        RuntimeError("Please provide a valid key: 'html', 'csv', or 'html'")
    formatter_cls = str_to_formatter_map[type]

    if column_formats:

        class formatter_cls(ColumnFormatMixin, formatter_cls):
            formats = column_formats

    if upper_headers:

        class formatter_cls(UpperHeadersMixin, formatter_cls):
            pass

    return formatter_cls()
