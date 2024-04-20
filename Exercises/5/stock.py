def read_instance_from_row(cls):
    @classmethod
    def from_row(cls, row):
        values = [f(v) for f, v in zip(cls._types, row)]
        return cls(*values)

    cls.from_row = from_row
    return cls


@read_instance_from_row
class Stock:
    _types = [str, int, float]

    def __init__(self, name, price, volume):
        self.name = name
        self.price = price
        self.volume = volume

    def __repr__(self):
        return f"{self.__class__.__name__}(name='{self.name}', price={self.price}, volume={self.volume})"
