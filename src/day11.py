from rich import print


def neighbours(xy, grid):
    x, y = xy
    for x1 in (x - 1, x, x + 1):
        for y1 in (y - 1, y, y + 1):
            if (x1, y1) in grid:
                yield (x1, y1)


def step(grid):
    for xy in grid:
        grid[xy] += 1

    flashed = [xy for xy in grid if grid[xy] == 10]

    for xy in flashed:
        for x1, y1 in neighbours(xy, grid):
            grid[x1, y1] += 1
            if grid[x1, y1] == 10:
                flashed.append((x1, y1))
    for xy in grid:
        if grid[xy] > 9:
            grid[xy] = 0
    return len(flashed)


def part1(filename):
    grid = {
        (x, y): int(c)
        for y, row in enumerate(line.strip() for line in open(filename) if line.strip())
        for x, c in enumerate(row)
    }

    return sum(step(grid) for _ in range(100))


assert part1("../input/day11-test.txt") == 1656
print("Part 1", part1("../input/day11.txt"))


def part2(filename):
    from itertools import count

    grid = {
        (x, y): int(c)
        for y, row in enumerate(line.strip() for line in open(filename) if line.strip())
        for x, c in enumerate(row)
    }

    for n in count(start=1):
        if step(grid) == 100:
            return n


assert part2("../input/day11-test.txt") == 195
print("Part 2", part2("../input/day11.txt"))
