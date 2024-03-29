def portfolio_cost(filename):
    total = 0
    with open(filename) as f:
        for line in f.readlines():
            _, shares, p = line.split()
            try:
                total += int(shares) * float(p)
            except ValueError as E:
                print("Couldn't parse", repr(line))
                print("Reason:", E)
    return total


if __name__ == "__main__":
    print("Total cost:", portfolio_cost("../../Data/portfolio2.csv"))
