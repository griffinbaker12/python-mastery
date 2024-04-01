import collections
import csv


# Cool exercise as it shows the difference between the interal representation of data, and how it is
# presented to its consumer / user
# rely on the magic methods to present the data to use in a useful way
class DataCollection(collections.abc.Sequence):  # type: ignore
    def __init__(self, headers, data=None):
        self.headers = headers
        if data is None:
            for h in headers:
                setattr(self, h, [])
        # elif len(data.values()) != len(headers):
        #     raise TypeError("You must pass initial data for each header")
        else:
            print(len(data), len(headers))
            for h, v in zip(headers, data):
                setattr(self, h, v)

    def get_attributes(self):
        return

    def __getitem__(self, i):
        if isinstance(i, int):
            # need to dynamically get the headers, and then for the headers, use those to build a
            # new object to return
            return {h: getattr(self, h)[i] for h in self.headers}
        elif isinstance(i, slice):
            x = [[d] for h in self.headers for d in getattr(self, h)[i]]
            print(x, "the x is")
            return DataCollection(self.headers, x)
        else:
            raise TypeError("Invalid argument type.")

    def __len__(self):
        for h in self.headers:
            return len(getattr(self, h, []))

    def append(self, d):
        for col in d.keys():
            getattr(self, col).append(d[col])


def read_rides_as_columns(filename, types):
    """
    Read the bus ride data as a list of dicts
    """
    with open(filename) as f:
        rows = csv.reader(f)
        headers = next(rows)  # Skip headers

        if len(headers) != len(types):
            raise ValueError("These type conversions do not properly map to the data")

        records = DataCollection(headers)
        for row in rows:
            record = {h: fn(val) for val, fn, h in zip(row, types, headers)}
            records.append(record)

    return records
