from rich import print

scores = {")": 3, "]": 57, "}": 1197, ">": 25137}
closer = {"(": ")", "[": "]", "{": "}", "<": ">"}


def first_illegal(s):
    stack = []
    for c in s:
        if c in closer:
            stack.append(closer[c])
        else:
            if stack[-1] == c:
                stack.pop(-1)
            else:
                print(f"Expected {stack[-1]} but found {c}")
                return scores[c]
    return 0


def part1(filename):
    total = 0
    for line in open(filename):
        line = line.strip()
        total += first_illegal(line)
    print(total)


part1("../input/day10-test.txt")
part1("../input/day10.txt")


def incomplete(s):
    scores = {")": 1, "]": 2, "}": 3, ">": 4}
    stack = []
    for c in s:
        if c in closer:
            stack.append(closer[c])
        else:
            if stack[-1] == c:
                stack.pop(-1)
            else:
                return 0
    score = 0
    for complete in stack[::-1]:
        score = score * 5 + scores[complete]
    return score


def part2(filename):
    scores = []
    for line in open(filename):
        line = line.strip()
        x = incomplete(line)
        if x != 0:
            scores.append(x)
    print(sorted(scores)[len(scores) // 2])


part2("../input/day10-test.txt")
part2("../input/day10.txt")
