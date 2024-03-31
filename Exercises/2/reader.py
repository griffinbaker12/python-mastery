import csv


def read_csv_as_dicts(filename, conv):
    with open(filename) as f:
        rows = csv.reader(f)
        headers = next(rows)

        if len(headers) != len(conv):
            raise ValueError(
                f"Expected {len(headers)} conversion functions, got {len(conv)}"
            )

        return [
            {name: func(val) for name, func, val in zip(headers, conv, row)}
            for row in rows
        ]
