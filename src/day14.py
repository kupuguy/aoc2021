from itertools import pairwise
from rich import print
from collections import Counter, defaultdict


def load(filename):
    with open(filename) as f:
        template = f.readline().strip()
        rules = {}
        for line in f:
            pair, _, insert = line.strip().partition(" -> ")
            if insert:
                rules[pair[0], pair[1]] = pair[0] + insert
    return template, rules


test_data = load("../input/day14-test.txt")
real_data = load("../input/day14.txt")


def part1(data):
    template, rules = data
    for step in range(10):
        template = "".join(
            [rules.get(pair, pair[0]) for pair in pairwise(template)] + [template[-1]]
        )

    count = Counter(template).most_common()
    return count[0][1] - count[-1][1]


assert part1(test_data) == 1588
print(part1(real_data))


def part2(data):
    template, rules = data
    rules = {k: v[1] for k, v in rules.items()}

    pair_count = Counter(pairwise(template))
    for step in range(40):
        new_count = Counter()
        for a, b in pair_count:
            if (a, b) in rules:
                c = rules[a, b]
                new_count.update({(a, c): pair_count[a, b], (c, b): pair_count[a, b]})
            else:
                new_count[a, b] += pair_count[a, b]
        pair_count = new_count

    count = defaultdict(int)
    for pair in pair_count:
        count[pair[0]] += pair_count[pair]
    count[template[-1]] += 1
    counts = sorted(count.items(), key=lambda p: p[1], reverse=True)
    return counts[0][1] - counts[-1][1]


assert part2(test_data) == 2188189693529
print(part2(real_data))
