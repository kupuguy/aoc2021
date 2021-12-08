from rich import print


def part1(filename):
    lines = [line.strip() for line in open(filename) if line.strip()]
    parts = [line.partition(" | ") for line in lines]
    # print(parts)
    data = [part.split() for _, _, part in parts]

    count = sum(sum(len(d) in (2, 3, 4, 7) for d in row) for row in data)
    print(filename, count)


part1("../input/day8-test.txt")
part1("../input/day8.txt")

digits = {
    1: "cf",
    7: "acf",
    4: "bcdf",
    2: "acdeg",
    3: "acdfg",
    5: "abdfg",
    6: "abdefg",
    9: "abcdfg",
    0: "abcefg",
    8: "abcdefg",
}


def decode(patterns, values):
    known = {}
    for p in patterns:
        if len(p) == 2:
            known[1] = set(p)
        if len(p) == 3:
            known[7] = set(p)
        if len(p) == 4:
            known[4] = set(p)
        if len(p) == 7:
            known[8] = set(p)
    for p in patterns:
        if len(p) == 6:
            if len(set(p).intersection(known[1])) == 1:
                known[6] = set(p)
            elif len(set(p).intersection(known[4])) == 4:
                known[9] = set(p)
            else:
                known[0] = set(p)
    for p in patterns:
        if len(p) == 5:
            if len(set(p).intersection(known[1])) == 2:
                known[3] = set(p)
            elif len(set(p).intersection(known[6])) == 5:
                known[5] = set(p)
            else:
                known[2] = set(p)
    # print(known)
    decoded = []
    for v in values:
        for k in known:
            if known[k] == set(v):
                decoded.append(k)
    # print(decoded)
    assert len(decoded) == 4
    return decoded[0] * 1000 + decoded[1] * 100 + decoded[2] * 10 + decoded[3]


def part2(filename):
    lines = [line.strip() for line in open(filename) if line.strip()]
    parts = [line.partition(" | ") for line in lines]
    # print(parts)
    data = [(patterns.split(), values.split()) for patterns, _, values in parts]

    real = [decode(p, v) for p, v in data]
    print(filename, sum(real))


print(
    decode(
        "acedgfb cdfbe gcdfa fbcad dab cefabd cdfgeb eafb cagedb ab".split(),
        "cdfeb fcadb cdfeb cdbaf".split(),
    )
)
part2("../input/day8-test.txt")
part2("../input/day8.txt")
