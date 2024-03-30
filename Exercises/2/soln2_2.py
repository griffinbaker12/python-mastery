import csv
from collections import Counter, defaultdict

FILE = "../../Data/ctabus.csv"
GREATEST_INC_SELECTION = 5


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


@read_file
def total_num_of_rides(rows=[]):
    num_rides = defaultdict(int)
    for r in rows:
        num_rides[r[0]] += int(r[3])
    return dict(num_rides)


yr_set = {"2001", "2011"}


# could probably do something where one direction is positive and the other is negative
@read_file
def get_greatest_ten_yr_increase(rows=[], selections=5):
    total_diff = Counter()

    # two_one = Counter()
    # two_elevent = Counter()

    for row in rows:
        year = row[1].split("/")[-1]
        if year in yr_set:
            # if year == "2001":
            #     total_one[row[0]] += int(row[-1])
            # else:
            #     two_eleven[row[0]] += int(row[-1])

            # alternative way to calculate
            if year == "2001":
                total_diff[row[0]] -= int(row[-1])
            else:
                total_diff[row[0]] += int(row[-1])

    # print(total_diff, two_eleven)
    # diff = two_eleven - total_diff

    return total_diff.most_common(selections)


if __name__ == "__main__":
    number_of_rides = get_number_of_rides()
    bus_rides = get_bus_rides_on_optional_date("22", "02/02/2011")
    total_rides_per = total_num_of_rides()
    greatest_ten_yr_increase = get_greatest_ten_yr_increase(GREATEST_INC_SELECTION)

    final_str = f"Total number of rides: {number_of_rides}\n\
        Bus rides on 22: {bus_rides}\n\
        Total rides per route: {total_rides_per}\n\
        Greatest increase for {GREATEST_INC_SELECTION} selections: {greatest_ten_yr_increase}\n\
        "
    print(final_str)
