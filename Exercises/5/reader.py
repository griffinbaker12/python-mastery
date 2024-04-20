import csv

# the csv class can take any iterable, not just files


def csv_as_dicts(lines, types, *, headers=None):
    """
    Takes lines and reads them as dicts
    """
    records = []
    print(headers)
    rows = csv.reader(lines)
    if headers is None:
        headers = next(rows)
    for row in rows:
        records.append({name: fn(val) for name, fn, val in zip(headers, types, row)})
    return records


def csv_as_instances(lines, cls, *, headers=None):
    """
    Takes lines and returns them as instances
    """
    records = []
    rows = csv.reader(lines)
    if headers is None:
        headers = next(rows)
    for row in rows:
        records.append(cls.from_row(row))
    return records


def read_csv_as_dicts(filename, types, *, headers=None):
    """
    Read CSV data into a list of dictionaries with type conversion
    """
    with open(filename) as f:
        return csv_as_dicts(f, types, headers=headers)


def read_csv_as_instances(filename, cls, *, headers=None):
    """
    Read csv data into a list of instances
    """
    with open(filename) as f:
        return csv_as_instances(f, cls, headers=headers)
