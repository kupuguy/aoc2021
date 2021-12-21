from functools import reduce

from rich import print


def first_illegal(s):
    scores = {")": 3, "]": 57, "}": 1197, ">": 25137}
    for _ in s:
        s = s.replace("()", "").replace("[]", "").replace("{}", "").replace("<>", "")
    if first_bad := next((c for c in s if c not in "([{<"), None):
        return scores[first_bad]
    return 0


def part1(filename):
    print(sum(first_illegal(line.strip()) for line in open(filename)))


part1("../input/day10-test.txt")
part1("../input/day10.txt")


def incomplete(s):
    scores = {"(": 1, "[": 2, "{": 3, "<": 4}
    for _ in s:
        s = s.replace("()", "").replace("[]", "").replace("{}", "").replace("<>", "")

    if next((c for c in s if c not in "([{<"), None):
        return 0

    return reduce(lambda a, b: a * 5 + b, (scores[c] for c in s[::-1]), 0)


def part2(filename):
    scores = sorted(
        score for line in open(filename) if (score := incomplete(line.strip()))
    )
    print(scores[len(scores) // 2])


part2("../input/day10-test.txt")
part2("../input/day10.txt")
