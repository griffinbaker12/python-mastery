import collections
import csv


# abstract class vs. protocol, requires us to implement the len and getitem methods
class RideData(collections.abc.Sequence):  # type: ignore
    def __init__(self, routes=[], dates=[], daytypes=[], numrides=[]):
        self.routes = routes
        self.dates = dates
        self.daytypes = daytypes
        self.numrides = numrides

    # assuming they are all of the same length
    def __len__(self):
        return len(self.routes)

    # prior to implementing a proper slice, the index itself is a slice
    # object that gets passed into each column
    # should support ints and slices
    def __getitem__(self, i):
        if isinstance(i, int):
            if i < 0 or i > len(self):
                raise IndexError("Invalid index provided")
            return {
                "route": self.routes[i],
                "date": self.dates[i],
                "daytype": self.daytypes[i],
                "rides": self.numrides[i],
            }
        # should return a new RidesData object that can then be indexed
        elif isinstance(i, slice):
            return RideData(
                routes=self.routes[i],
                dates=self.dates[i],
                daytypes=self.daytypes[i],
                numrides=self.numrides[i],
            )
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
    records = RideData()  # <--- CHANGE THIS
    with open(filename) as f:
        rows = csv.reader(f)
        _ = next(rows)  # Skip headers
        for row in rows:
            route = row[0]
            date = row[1]
            daytype = row[2]
            rides = int(row[3])
            # this dict is only temporary, and gets cleaned up on the next
            # iteration of the loop (what would that look like in C)
            # how would we manage that allocation? I guess one benefit
            # of using that language is that you have to be aware of the memory
            # you are allocating with having to clear it yourself and stuff
            record = {
                "route": route,
                "date": date,
                "daytype": daytype,
                "rides": rides,
            }
            records.append(record)
    return records
