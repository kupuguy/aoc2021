from collections import defaultdict
from rich import print


def find_path(routes: dict[str, set], seen: set, current: str, small_caves: set[str], small_cave_count: int=0):
    for nxt in routes[current]:
        if nxt in small_caves:
            if nxt == "end":
                yield seen
            elif len(seen | {nxt}) < small_cave_count+1:
                continue  # can't revisit a small room.
            else:
                yield from find_path(routes, seen | {nxt}, nxt, small_caves, small_cave_count+1)
        else:
            yield from find_path(routes, seen, nxt, small_caves, small_cave_count)

def load(filename: str) -> dict[str, set]:
    routes = defaultdict(set)
    for a, b in [line.strip().split("-") for line in open(filename)]:
        # avoid adding any routes back to start
        if b != 'start':
            routes[a].add(b)
        if a != 'start':
            routes[b].add(a)
    # and no routes away from end
    routes['end'] = set()
    return routes

def part1(filename):
    routes = load(filename)
    
    small_caves = {cave for cave in routes if cave.islower()}
    return len(list(find_path(routes, seen=set(), current='start', small_caves=small_caves, small_cave_count=0)))


assert part1("../input/day12-test.txt") == 19
print("part 1", part1("../input/day12.txt"))

def part2(filename):
    routes = load(filename)
    
    small_caves = {cave for cave in routes if cave.islower()}
    return len(list(find_path(routes, seen=set(), current='start', small_caves=small_caves, small_cave_count=-1)))

assert part2("../input/day12-test.txt") == 103
print("part 2", part2("../input/day12.txt"))
