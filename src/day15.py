from rich import print


def load(filename: str) -> list[list[int]]:
    with open(filename) as f:
        grid = [[int(n) for n in line.strip()] for line in f if line.strip()]
    return grid


test_data = load("../input/day15-test.txt")
real_data = load("../input/day15.txt")


def neighbours(x, y, limit):
    return [
        (x1, y1)
        for (x1, y1) in [(x, y + 1), (x + 1, y), (x, y - 1), (x - 1, y)]
        if 0 <= x1 < limit and 0 <= y1 < limit
    ]


def part1(data):
    costs = {(0, 0): 0}
    track = {}
    limit = len(data)
    assert limit == len(data[0])
    points = [(0, 0)]
    for (x, y) in points:
        for (x1, y1) in neighbours(x, y, limit):
            if (x1, y1) in costs and costs[x1, y1] <= costs[x, y] + data[y1][x1]:
                continue
            costs[x1, y1] = costs[x, y] + data[y1][x1]
            points.append((x1, y1))
            track[x1, y1] = (x, y)

    path = {(0, 0)}
    x, y = limit - 1, limit - 1
    while (x, y) != (0, 0):
        path.add((x, y))
        x, y = track[x, y]

    print(
        "\n".join(
            "".join(
                f"[green]{risk}[/green]"
                if (x, y) in path
                else f"[dim white]{risk}[/dim white]"
                for x, risk in enumerate(row)
            )
            for y, row in enumerate(data)
        )
    )
    return costs[limit - 1, limit - 1]


assert part1(test_data) == 40, part1(test_data)
print(part1(real_data))


def bump(row, n):
    return [((c + n - 1) % 9) + 1 for c in row]


def part2(data):
    full_map = [
        bump(row, n)
        + bump(row, n + 1)
        + bump(row, n + 2)
        + bump(row, n + 3)
        + bump(row, n + 4)
        for n in range(5)
        for row in data
    ]
    return part1(full_map)


assert part2(test_data) == 315, part2(test_data)
print(part2(real_data))
