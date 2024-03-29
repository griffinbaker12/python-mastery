import csv

FILE = "../../Data/ctabus.csv"


def read_file(fn):
    def wrapper(*args, **kwargs):
        with open(FILE) as f:
            f.seek(0)
            rows = csv.reader(f)
            next(rows)  # Skip the header
            return fn(rows, *args, **kwargs)

    return wrapper


@read_file
def get_number_of_rides(rows=[]):
    # Directly operate on rows and return the result
    return len({row[0] for row in rows})


@read_file
def get_bus_rides_on_optional_date(rows, bus_num, date=None):
    # Directly operate on rows and return the result
    # Fixed to filter correctly and sum up the 'rides' as integers
    return sum(
        int(r[-1])
        for r in rows
        if r[0] == str(bus_num) and (date is None or r[1] == date)
    )


if __name__ == "__main__":
    number_of_rides = get_number_of_rides()
    bus_rides = get_bus_rides_on_optional_date("22", "02/02/2011")
    final_str = f"Number of rides: {number_of_rides}\nBus rides on 22: {bus_rides}"
    print(final_str)
