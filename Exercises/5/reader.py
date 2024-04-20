# the csv class can take any iterable, not just files
import csv


def convert_csv(lines, converter, *, headers):
    """
    Takes lines and converts them in some way the user specifies
    """
    rows = csv.reader(lines)
    headers = next(rows)
    return list(map(lambda row: converter(headers, row), rows))


def csv_as_dicts(lines, types, *, headers=None):
    """
    Takes lines and reads them as dicts
    """
    return convert_csv(
        lines,
        lambda headers, row: {h: f(v) for h, f, v in zip(headers, types, row)},
        headers=headers,
    )


def csv_as_instances(lines, cls, *, headers=None):
    """
    Takes lines and returns them as instances
    """
    return convert_csv(
        lines,
        lambda _, row: cls.from_row(row),
        headers=headers,
    )


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
