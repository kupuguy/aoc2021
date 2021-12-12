from collections import defaultdict
from rich import print


def find_path(routes, seen, current, required):
    #print("x", current, seen)
    for nxt in routes[current]:
        if nxt.islower():
            if nxt in seen:
                continue  # can't revisit a small room.
            seen.append(nxt)
            if nxt == "end":
                yield seen
                seen.pop(-1)
                continue
        else:
            seen.append(nxt)
        yield from find_path(routes, seen, nxt, required)
        seen.pop(-1)


def part1(filename):
    routes = defaultdict(list)
    for a, b in [line.strip().split("-") for line in open(filename)]:
        routes[a].append(b)
        routes[b].append(a)

    seen = ["start"]
    current = "start"
    required = {cave for cave in routes if cave.islower()}
    return len(list(find_path(routes, seen, current, required)))


assert part1("../input/day12-test.txt") == 19
print("part 1", part1("../input/day12.txt"))

def count_small_bad(seen):
    counter = defaultdict(int)
    for c in seen:
        if c.islower():
            counter[c] += 1
    return any(c > 2 for c in counter.values()) or sum(c > 1 for c in counter.values()) > 1

def find_path2(routes, seen, current, required):
    for nxt in routes[current]:
        if nxt.islower():
            if nxt == 'start': continue
            if nxt == "end":
                yield seen
                continue
            if nxt in seen and count_small_bad(seen + [nxt]):
                continue  # can't revisit another small room.
            seen.append(nxt)
        else:
            seen.append(nxt)
        yield from find_path2(routes, seen, nxt, required)
        seen.pop(-1)


def part2(filename):
    routes = defaultdict(list)
    for a, b in [line.strip().split("-") for line in open(filename)]:
        routes[a].append(b)
        routes[b].append(a)

    seen = ["start"]
    current = "start"
    required = {cave for cave in routes if cave.islower()}
    return len(list(find_path2(routes, seen, current, required)))

assert part2("../input/day12-test.txt") == 103,  part2("../input/day12-test.txt")
print("part 2", part2("../input/day12.txt"))
