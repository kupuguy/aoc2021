from rich import print
from collections import Counter
from typing import Generator


def load(filename: str) -> tuple[str, list[str]]:
    with open(filename) as f:
        rules = f.readline().strip()

        data = [line.strip() for line in f if line.strip()]
    return rules, data


def neighbours(x: int, y: int) -> Generator[tuple[int, int], None, None]:
    yield from [(xn, yn) for yn in (y - 1, y, y + 1) for xn in (x - 1, x, x + 1)]


def bounds(grid: dict[tuple[int, int], str]) -> tuple[int, int, int, int]:
    left = min(x for x, _ in grid) - 1
    right = max(x for x, _ in grid) + 1
    top = min(y for _, y in grid) - 1
    bottom = max(y for _, y in grid) + 1
    return left, top, right, bottom


def algorithm(rules: str, grid: dict[tuple[int, int], str], default: str):
    new_grid: dict[tuple[int, int], str] = {}

    left, top, right, bottom = bounds(grid)
    for x in range(left, right + 1):
        for y in range(top, bottom + 1):
            index = int(
                "".join(grid.get((x1, y1), default) for x1, y1 in neighbours(x, y)), 2
            )
            if rules[index] == "#":
                new_grid[x, y] = "1"
            else:
                new_grid[x, y] = "0"
    return new_grid


def reconstruct(grid: dict[tuple[int, int], str]) -> str:
    left, top, right, bottom = bounds(grid)
    rows: list[str] = []
    for y in range(top, bottom):
        rows.append("".join(grid.get((x, y), " ") for x in range(left, right)))
    return "\n".join(rows)


def part1(filename: str, nsteps: int = 2) -> int:
    rules, raw = load(filename)
    grid = {
        (x, y): ("1" if c == "#" else "0")
        for y, row in enumerate(raw)
        for x, c in enumerate(row)
    }

    grid = algorithm(rules, grid, "0")
    default = "1" if rules[0] == "#" else "0"
    for n in range(nsteps - 1):
        grid = algorithm(rules, grid, default)
        dc = rules[0] if default == "0" else rules[511]
        default = "1" if dc == "#" else "0"
    counts = Counter(grid.values())
    return counts["1"]


assert part1("../input/day20-test.txt") == 35
print("Part 1", part1("../input/day20.txt"))

part2 = part1
assert part2("../input/day20-test.txt", 50) == 3351
print("Part 2", part2("../input/day20.txt", 50))
