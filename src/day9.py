from rich import print

data = """2199943210
3987894921
9856789892
8767896789
9899965678""".split()


def neighbours(data, x, y):
    if x > 0:
        yield data[x - 1][y]
    if x < len(data) - 1:
        yield data[x + 1][y]
    if y > 0:
        yield data[x][y - 1]
    if y < len(data[x]) - 1:
        yield data[x][y + 1]


def low(data):
    for x in range(len(data)):
        for y in range(len(data[x])):
            v = data[x][y]
            if all(v < neighbour for neighbour in neighbours(data, x, y)):
                yield v, x, y


def part1(data):
    data = [[int(d) for d in line] for line in data]
    print("part 1", sum(v + 1 for v, _, _ in low(data)))


part1(data)
part1([s.strip() for s in open("../input/day9.txt").readlines()])


def npos(data, x, y):
    if x > 0:
        yield x - 1, y
    if x < len(data) - 1:
        yield x + 1, y
    if y > 0:
        yield x, y - 1
    if y < len(data[x]) - 1:
        yield x, y + 1


def basin(data, x, y):
    points = {(x, y)}
    v = data[x][y]
    queue = [(x1, y1) for (x1, y1) in npos(data, x, y) if data[x1][y1] != 9]
    while queue:
        x1, y1 = queue.pop()
        if (x1, y1) not in points:
            points.add((x1, y1))
            for x2, y2 in npos(data, x1, y1):
                if data[x2][y2] != 9:
                    queue.append((x2, y2))
    return len(points)


import heapq


def part2(data):
    data = [[int(d) for d in line] for line in data]
    largest = heapq.nlargest(3, [basin(data, x, y) for _, x, y in low(data)])
    print("Part 2", largest[0] * largest[1] * largest[2])


part2(data)
part2([s.strip() for s in open("../input/day9.txt").readlines()])
