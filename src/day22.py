from __future__ import annotations
import re
from dataclasses import dataclass
from rich import print
from collections import defaultdict


def segments(
    amin: int, amax: int, bmin: int, bmax: int
) -> tuple[list[tuple[int, int]], list[tuple[int, int]], list[tuple[int, int]]]:
    """Split 2 line segments into parts a-only, b-only, and intersection"""
    a_only, b_only, intersection = [], [], []
    if amin < bmin:
        a_only += [(amin, min(amax, bmin - 1))]
        amin = bmin
    if bmax < amax:
        a_only += [(max(bmax + 1, amin), amax)]
        amax = bmax
    if bmin < amin:
        b_only += [(bmin, min(bmax, amin - 1))]
        bmin = amin
    if amax < bmax:
        b_only += [(max(amax + 1, bmin), bmax)]
    intersection = [(amin, amax)] if amin <= amax else []
    return a_only, b_only, intersection


@dataclass
class Cuboid:
    state: bool
    xmin: int
    xmax: int
    ymin: int
    ymax: int
    zmin: int
    zmax: int

    def in_region(self) -> bool:
        return all(
            -50 <= p <= 50
            for p in (self.xmin, self.xmax, self.ymin, self.ymax, self.zmin, self.zmax)
        )

    def intersects(self, other: Cuboid) -> bool:
        return (
            other.xmax >= self.xmin
            and other.xmin <= self.xmax
            and other.ymax >= self.ymin
            and other.ymin <= self.ymax
            and other.zmax >= self.zmin
            and other.zmin <= self.zmax
        )

    def in_out(self, other: Cuboid) -> tuple[list[Cuboid], list[Cuboid], list[Cuboid]]:
        """Returns three lists of cubes from the intersection of self & other.
        Cuboids only in self, cuboids only in other, cuboids in intersection"""
        if not self.intersects(other):
            return [self], [other], []

        xself, xother, xint = segments(self.xmin, self.xmax, other.xmin, other.xmax)
        yself, yother, yint = segments(self.ymin, self.ymax, other.ymin, other.ymax)
        zself, zother, zint = segments(self.zmin, self.zmax, other.zmin, other.zmax)
        cself = (
            [
                Cuboid(self.state, *xs, *ys, *zs)
                for xs in xself
                for ys in yself + yint
                for zs in zself + zint
            ]
            + [
                Cuboid(self.state, *xs, *ys, *zs)
                for xs in xint
                for ys in yself
                for zs in zself + zint
            ]
            + [
                Cuboid(self.state, *xs, *ys, *zs)
                for xs in xint
                for ys in yint
                for zs in zself
            ]
        )
        cother = (
            [
                Cuboid(other.state, *xo, *yo, *zo)
                for xo in xother
                for yo in yother + yint
                for zo in zother + zint
            ]
            + [
                Cuboid(other.state, *xo, *yo, *zo)
                for xo in xint
                for yo in yother
                for zo in zother + zint
            ]
            + [
                Cuboid(other.state, *xo, *yo, *zo)
                for xo in xint
                for yo in yint
                for zo in zother
            ]
        )
        cint = [
            Cuboid(self.state and other.state, *xi, *yi, *zi)
            for xi in xint
            for yi in yint
            for zi in zint
        ]
        return cself, cother, cint

    def on_cubes(self, other: Cuboid) -> list[Cuboid]:
        s, o, i = self.in_out(other)
        cubes = [c for c in s + o + i if c.state]
        return cubes

    def union(self, others: list[Cuboid]) -> list[Cuboid]:
        out = []
        for other in others:
            s, o, i = self.in_out(other)
            out += o
        return out + [self]


def coalesce(cubes: list[Cuboid]) -> list[Cuboid]:
    # Amalgamate common x,y
    cm = defaultdict(list)
    for c in cubes:
        cm[c.xmin, c.ymin, c.xmax, c.ymax].append(c)
    for clist in cm.values():
        index = 0
        clist.sort(key=lambda c: c.zmin)
        while index < len(clist) - 1:
            c = clist[index]
            if c.zmax + 1 == clist[index + 1].zmin:
                clist[index : index + 2] = [
                    Cuboid(
                        True,
                        c.xmin,
                        c.xmax,
                        c.ymin,
                        c.ymax,
                        c.zmin,
                        clist[index + 1].zmax,
                    )
                ]
            else:
                index += 1
    cubes = [c for cl in cm.values() for c in cl]

    # Amalgamate common x,z
    cm = defaultdict(list)
    for c in cubes:
        cm[c.xmin, c.zmin, c.xmax, c.zmax].append(c)
    for clist in cm.values():
        index = 1
        clist.sort(key=lambda c: c.ymin)
        while index < len(clist) - 1:
            c = clist[index]
            if c.ymax + 1 == clist[index + 1].ymin:
                clist[index : index + 2] = [
                    Cuboid(
                        True,
                        c.xmin,
                        c.xmax,
                        c.ymin,
                        clist[index + 1].ymax,
                        c.zmin,
                        c.zmax,
                    )
                ]
            else:
                index += 1
    cubes = [c for cl in cm.values() for c in cl]

    # Amalgamate common y,z
    cm = defaultdict(list)
    for c in cubes:
        cm[c.ymin, c.zmin, c.ymax, c.zmax].append(c)
    for clist in cm.values():
        index = 1
        clist.sort(key=lambda c: c.ymin)
        while index < len(clist) - 1:
            c = clist[index]
            if c.xmax + 1 == clist[index + 1].xmin:
                clist[index : index + 2] = [
                    Cuboid(
                        True,
                        c.xmin,
                        clist[index + 1].xmax,
                        c.ymin,
                        c.ymax,
                        c.zmin,
                        c.zmax,
                    )
                ]
            else:
                index += 1
    cubes = [c for cl in cm.values() for c in cl]

    return cubes


def load(filename: str) -> list[Cuboid]:
    data = []
    for line in open(filename):
        parts = re.match(
            r"(on|off) .*?(-?\d+).*?(-?\d+).*?(-?\d+).*?(-?\d+).*?(-?\d+).*?(-?\d+)",
            line.strip(),
        )
        if parts:
            groups = parts.groups()
            data.append(Cuboid(groups[0] == "on", *map(int, groups[1:])))
    return data


def count(cubes: list[Cuboid]) -> int:
    return sum(
        (c.xmax - c.xmin + 1) * (c.ymax - c.ymin + 1) * (c.zmax - c.zmin + 1)
        for c in cubes
    )


def part1(filename: str) -> int:
    cubes = [cube for cube in load(filename) if cube.in_region()]
    on = [cubes[0]]
    for cube in cubes:
        if cube.state:
            on_cubes = cube.union(on)
        else:
            on_cubes = []
            for other in on:
                on_cubes += cube.on_cubes(other)
        on = on_cubes
    total = count(on)
    return total


assert part1("input/day22-test.txt") == 590784
print(part1("input/day22.txt"))


def part2(filename: str) -> int:
    cubes = [cube for cube in load(filename)]
    on = [cubes[0]]
    for cube in cubes:
        if cube.state:
            on_cubes = cube.union(on)
        else:
            on_cubes = []
            for other in on:
                on_cubes += cube.on_cubes(other)
        on = on_cubes
    total = count(on)
    return total


assert part2("input/day22-test2.txt") == 2758514936282235
print(part2("input/day22.txt"))
