import csv
import functools
import tracemalloc as tm
from collections import namedtuple

import matplotlib.pyplot as plt


# these need to return all of the data in the given representation
def read_as_tuple(route, date, daytype, rides):
    return route, date, daytype, rides


def read_as_dict(route, date, daytype, rides):
    return {
        "route": route,
        "date": date,
        "daytype": daytype,
        "rides": rides,
    }


class Row:
    def __init__(self, route, date, daytype, rides) -> None:
        self.route = route
        self.date = date
        self.daytype = daytype
        self.rides = rides


def read_as_class(route, date, daytype, rides):
    return Row(route, date, daytype, rides)


# Define the namedtuple type outside of the function
RowNamedTuple = namedtuple("Row", ["route", "date", "daytype", "rides"])


def read_as_named_tuple(route, date, daytype, rides):
    return RowNamedTuple(route, date, daytype, rides)


class RowWithSlots:
    __slots__ = ["route", "date", "daytype", "rides"]

    def __init__(self, route, date, daytype, rides) -> None:
        self.route = route
        self.date = date
        self.daytype = daytype
        self.rides = rides


def read_as_slots(route, date, daytype, rides):
    return RowWithSlots(route, date, daytype, rides)


data_reps = {
    "tuple": {"fn": read_as_tuple, "memory": 0},
    "dict": {"fn": read_as_dict, "memory": 0},
    "class": {"fn": read_as_class, "memory": 0},
    "named_tuple": {"fn": read_as_named_tuple, "memory": 0},
    "slots": {"fn": read_as_slots, "memory": 0},
}


def track_memory(fn):
    @functools.wraps(fn)
    def wrapper(*args, **kwargs):
        tm.start()  # Start tracking memory
        result = fn(*args, **kwargs)  # Call the original function
        _, peak = tm.get_traced_memory()  # Get the memory usage
        tm.stop()  # Stop tracking memory
        tm.clear_traces()  # Clear traces to reset memory tracking
        return (
            result,
            peak,
        )

    return wrapper


@track_memory
def process_rows(rows, fn):
    items = []
    _ = next(rows)
    for row in rows:
        item = fn(*row)
        items.append(item)
    return items


# read in the file, process according to each rep, and then reset the file
# pointer until the end of the file is reached and all representations are read


def read_all_reps(filename):
    with open(filename) as f:
        for rep in data_reps:
            f.seek(0)
            rows = csv.reader(f)
            # process rows and get memory usage
            _, p = process_rows(rows, data_reps[rep]["fn"])
            data_reps[rep]["memory"] = p


def draw_results(sorted_rep):
    # Extract data types and memory usage from sorted_rep
    data_types = [rep for rep, _ in sorted_rep]
    memory_usage = [data["memory"] / 1000000 for _, data in sorted_rep]  # Convert to MB

    # Creating the bar chart
    plt.figure(figsize=(10, 6))  # Set the figure size
    plt.bar(data_types, memory_usage, color="skyblue")  # Create a bar chart

    plt.title("Memory Usage by Data Representation")  # Title of the chart
    labelpad = 10  # Set the padding for the labels
    plt.xlabel("Data Representation", labelpad=labelpad)  # X-axis label
    plt.ylabel("Memory Usage (MB)", labelpad=labelpad)  # Y-axis label
    # plt.xticks(rotation=30)  # Rotate the x-axis labels
    upper_limit = max(memory_usage) + 50  # Set the upper limit of the y-axis
    plt.ylim(0, upper_limit)  # Set the y-axis limits

    # Optionally, add the exact memory usage above each bar for clarity
    spacing = 5  # Set the spacing between the bar and the text
    for i, usage in enumerate(memory_usage):
        plt.text(i, usage + spacing, f"{usage:.2f} MB", ha="center")

    # Display the plot
    plt.tight_layout()  # Adjust the layout
    plt.show()


if __name__ == "__main__":
    read_all_reps("../../Data/ctabus.csv")
    sorted_rep = sorted(data_reps.items(), key=lambda x: x[1]["memory"])
    for rep, data in sorted_rep:
        print(f"{rep}: {data['memory']/1000000:.2f} MB")
    print("\nDrawing graph...\n")
    draw_results(sorted_rep)
    # for rep, data in sorted_rep:
    #     print(f"{rep}: {data['memory']/1000000:.2f} MB")
