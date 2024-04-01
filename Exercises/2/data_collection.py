import csv
from collections.abc import Sequence


class DataCollection(Sequence):
    def __init__(self, columns):
        self.columns = columns

    def __getitem__(self, index):  # type: ignore
        if isinstance(index, slice):
            sliced_data = {key: value[index] for key, value in self.columns.items()}
            return DataCollection(sliced_data)
        elif isinstance(index, int):
            if index < 0 or index >= len(self):
                raise IndexError("Index out of range")
            return {key: value[index] for key, value in self.columns.items()}
        else:
            raise TypeError("Invalid argument type.")

    def __len__(self):
        if self.columns:
            return len(next(iter(self.columns.values())))
        return 0


def read_csv_as_columns(filename, types):
    with open(filename, "r") as file:
        reader = csv.reader(file)
        headers = next(reader)  # Read the first row to use as column headers
