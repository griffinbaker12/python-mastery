# import collections
import csv
from collections.abc import Sequence

from soln2_1 import read_as_dict


class RideData(Sequence):
    def __init__(
        self,
        routes=None,
        dates=None,
        daytypes=None,
        numrides=None,
    ) -> None:
        self.routes = routes if routes is not None else []
        self.dates = dates if dates is not None else []
        self.daytypes = daytypes if daytypes is not None else []
        self.numrides = numrides if numrides is not None else []

    def __len__(self) -> int:
        return len(self.routes)

    def __getitem__(self, index):  # type: ignore
        if isinstance(index, slice):
            print("The index and slice are:", index, slice)
            # Handle slice case: return a new RideData object with sliced data
            return RideData(
                routes=self.routes[index],
                dates=self.dates[index],
                daytypes=self.daytypes[index],
                numrides=self.numrides[index],
            )
        elif isinstance(index, int):
            # Handle single item access: return a dictionary for the row
            if index < 0 or index >= len(self):  # Bounds checking
                raise IndexError("Index out of range")
            return {
                "route": self.routes[index],
                "date": self.dates[index],
                "daytype": self.daytypes[index],
                "rides": self.numrides[index],
            }
        else:
            raise TypeError("Invalid argument type.")

    def append(self, d):
        self.routes.append(d["route"])
        self.dates.append(d["date"])
        self.daytypes.append(d["daytype"])
        self.numrides.append(d["rides"])


def read_rides_as_dicts(filename):
    """
    Read the bus ride data as a list of dicts
    """
    records = RideData()
    with open(filename) as f:
        rows = csv.reader(f)
        next(rows)  # Skip headers
        for row in rows:
            route = row[0]
            date = row[1]
            daytype = row[2]
            rides = int(row[3])
            record = {
                "route": route,
                "date": date,
                "daytype": daytype,
                "rides": rides,
            }
            records.append(record)
    return records


def process_rows(rows, fn):
    next(rows)
    items = []
    for row in rows:
        items.append(fn(*row))
    return items


# 18482016 (column method)
# 287158823 (rows as dicts)
# 96207950 (as custom container)
def read_rides_as_columns(filename):
    """
    Read the bus ride data into 4 lists, representing columns
    """
    routes = []
    dates = []
    daytypes = []
    numrides = []
    with open(filename) as f:
        rows = csv.reader(f)
        next(rows)  # Skip headers
        for row in rows:
            routes.append(row[0])
            dates.append(row[1])
            daytypes.append(row[2])
            numrides.append(int(row[3]))
    return dict(
        routes=routes,
        dates=dates,
        daytypes=daytypes,
        numrides=numrides,
    )


def read():
    return read_rides_as_dicts("../../Data/ctabus.csv")
    # return read_rides_as_columns("../../Data/ctabus.csv")
    # with open("../../Data/ctabus.csv") as f:
    #     return process_rows(csv.reader(f), read_rides_as_dicts)


if __name__ == "__main__":
    read()
