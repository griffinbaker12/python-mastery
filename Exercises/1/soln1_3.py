total = 0

with open("../../Data/portfolio.dat", "r") as f:
    for line in f.readlines():
        name, shares, p = line.split()
        total += int(shares) * float(p)

print(total)
