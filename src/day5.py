from dataclasses import dataclass
from collections import defaultdict
from rich import print


@dataclass
class Point:
    x: int
    y: int


@dataclass
class Vent:
    start: Point
    end: Point


lines = open("../input/day5-test.txt").readlines()
lines = open("../input/day5.txt").readlines()


def parse(lines):
    for line in lines:
        start, _, end = line.strip().partition("->")
        if not end:
            continue
        startx, starty = start.strip().split(",")
        endx, endy = end.strip().split(",")
        yield Vent(Point(int(startx), int(starty)), Point(int(endx), int(endy)))


data = list(parse(lines))

hv = [p for p in data if p.start.x == p.end.x or p.start.y == p.end.y]
# print(hv)
points = defaultdict(int)

for vent in data:
    if vent.start.x == vent.end.x:
        for i in range(
            min(vent.start.y, vent.end.y), max(vent.start.y, vent.end.y) + 1
        ):
            points[vent.start.x, i] += 1
    elif vent.start.y == vent.end.y:
        for i in range(
            min(vent.start.x, vent.end.x), max(vent.start.x, vent.end.x) + 1
        ):
            points[i, vent.start.y] += 1
    else:
        # print(vent)
        if vent.start.x < vent.end.x:
            xr = range(vent.start.x, vent.end.x + 1)
        else:
            xr = range(vent.start.x, vent.end.x - 1, -1)
        if vent.start.y < vent.end.y:
            yr = range(vent.start.y, vent.end.y + 1)
        else:
            yr = range(vent.start.y, vent.end.y - 1, -1)

        # print(xr, yr)
        for x, y in zip(xr, yr):
            points[x, y] += 1

# print(points)
print(sum(1 for p in points.values() if p > 1))
