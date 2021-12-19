from __future__ import annotations
from rich import print
from dataclasses import dataclass
from math import sqrt
from itertools import permutations
from functools import cached_property, cache
from itertools import pairwise


@dataclass(frozen=True)
class Point:
    x: int
    y: int
    z: int

    def distance(self, other: "Point"):
        xd = self.x - other.x
        yd = self.y - other.y
        zd = self.z - other.z
        return sqrt(xd * xd + yd * yd + zd * zd)

    @cache
    def neighbour_distances(self, neighbours: list["Point"]) -> set:
        return {int(self.distance(other)) for other in neighbours} - {0}

    def __sub__(self, other):
        return Point(self.x - other.x, self.y - other.y, self.z - other.z)

    def __add__(self, other):
        return Point(self.x + other.x, self.y + other.y, self.z + other.z)

    def matrix(self, other):
        x = [
            1 if self.x == other.x else -1 if self.x == -other.x else 0,
            1 if self.y == other.x else -1 if self.y == -other.x else 0,
            1 if self.z == other.x else -1 if self.z == -other.x else 0,
        ]
        y = [
            1 if self.x == other.y else -1 if self.x == -other.y else 0,
            1 if self.y == other.y else -1 if self.y == -other.y else 0,
            1 if self.z == other.y else -1 if self.z == -other.y else 0,
        ]
        z = [
            1 if self.x == other.z else -1 if self.x == -other.z else 0,
            1 if self.y == other.z else -1 if self.y == -other.z else 0,
            1 if self.z == other.z else -1 if self.z == -other.z else 0,
        ]
        if sum(map(abs, x + y + z)) == 3:
            return [x, y, z]
        return None  # can't tell!

    def rotate(self, matrix: list[list[int]]):
        return Point(
            self.x * matrix[0][0] + self.y * matrix[0][1] + self.z * matrix[0][2],
            self.x * matrix[1][0] + self.y * matrix[1][1] + self.z * matrix[1][2],
            self.x * matrix[2][0] + self.y * matrix[2][1] + self.z * matrix[2][2],
        )


@dataclass
class Scanner:
    name: int
    position: Optional[Point]
    beacons: Set[Point]

    def __repr__(self):
        return "<Scanner %s %s>" % (self.name, self.position)

    @cached_property
    def distances(self) -> set[int]:
        d = set()
        fb = frozenset(self.beacons)
        for b in self.beacons:
            d |= b.neighbour_distances(fb)
        return d

    def overlap(self, other: "Scanner") -> int:
        return len(self.distances & other.distances)

    def shift(self, other: "Scanner") -> "Scanner":
        # find best overlapping point
        fb = frozenset(self.beacons)
        ob = frozenset(other.beacons)
        candidates = sorted(
            [(b, ob) for b in self.beacons for ob in other.beacons],
            key=lambda bob: len(
                bob[0].neighbour_distances(fb) & bob[1].neighbour_distances(ob)
            ),
            reverse=True,
        )
        for p1, p2 in pairwise(candidates):
            matrix = (p1[0] - p2[0]).matrix(p1[1] - p2[1])
            if matrix:
                break
        org = candidates[0][1] - candidates[0][0].rotate(matrix)

        self.position = org
        self.beacons = {b.rotate(matrix) + org for b in self.beacons}


def load(filename):
    scanners = []
    name = 0
    for line in open(filename):
        if line.startswith("---"):
            scanners.append(Scanner(name, None, set()))
            name += 1
        elif line.strip():
            x, y, z = map(int, line.strip().split(","))
            scanners[-1].beacons.add(Point(x, y, z))
    scanners[0].position = Point(0, 0, 0)
    return scanners


def part1(filename):
    raw = load(filename)
    known = [scanner0 := raw.pop(0)]
    while raw:
        best, other = max(
            [(unknown, other) for unknown in raw for other in known],
            key=lambda s: s[0].overlap(s[1]),
        )
        known.append(best)
        best.shift(other)
        raw = [s for s in raw if s is not best]

    beacons = set()
    for scanner in known:
        beacons |= scanner.beacons
    return len(beacons)


assert part1("../input/day19-test.txt") == 79
print(f"Part 1={part1('../input/day19.txt')}")


def manhattan(p1: Point, p2: Point):
    dist = abs(p1.x - p2.x) + abs(p1.y - p2.y) + abs(p1.z - p2.z)
    return dist


assert manhattan(Point(1105, -1205, 1229), Point(-92, -2380, -20)) == 3621


def part2(filename):
    raw = load(filename)
    known = [scanner0 := raw.pop(0)]
    while raw:
        best, other = max(
            [(unknown, other) for unknown in raw for other in known],
            key=lambda s: s[0].overlap(s[1]),
        )
        known.append(best)
        best.shift(other)
        raw = [s for s in raw if s is not best]

    return max(
        manhattan(s1.position, s2.position)
        for s1 in known
        for s2 in known
        if s1 is not s2
    )


assert part2("../input/day19-test.txt") == 3621
print("Part 2", part2("../input/day19.txt"))
