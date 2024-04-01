import csv

COL_LEN = 10


class Stock:
    def __init__(self, name, shares, price) -> None:
        self.name = name
        self.shares = shares
        self.price = price

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


def read_portfolio(filename):
    data = []
    with open(filename) as f:
        rows = csv.reader(f)
        next(rows)
        conv = [str, int, float]
        for r in rows:
            data.append(Stock(*[fn(v) for fn, v in zip(conv, r)]))
    return data


def print_headers(p):
    print(" ".join(f"{h:>{COL_LEN}}" for h in vars(p[0]).keys()))


def print_seps(p):
    print(" ".join("-" * COL_LEN for _ in vars(p[0]).keys()))


def _print_portfolio(p):
    for item in p:
        print(
            " ".join(
                f"{getattr(item,header):>{COL_LEN}}" for header in vars(p[0]).keys()
            )
        )


def printer(fns, v):
    for fn in fns:
        fn(v)


def print_portfolio(p):
    fns = [print_headers, print_seps, _print_portfolio]
    printer(fns, p)
