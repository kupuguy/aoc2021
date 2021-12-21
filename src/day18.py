import json

Snail = list[int | list]
Flat = list[tuple[int, int]]


def flatten(number: Snail, depth: int = 1) -> Flat:
    a, b = number
    f = ([(a, depth)] if isinstance(a, int) else flatten(a, depth + 1)) + (
        [(b, depth)] if isinstance(b, int) else flatten(b, depth + 1)
    )
    return f


def reconstruct(flat: Flat) -> Snail:
    while len(flat) > 1:
        for i in range(len(flat) - 1):
            if flat[i][1] == flat[i + 1][1]:
                flat = (
                    flat[:i]
                    + [([flat[i][0], flat[i + 1][0]], flat[i][1] - 1)]
                    + flat[i + 2 :]
                )
                break
    return flat[0][0]


def explode_flattened(flat: Flat) -> Flat | None:
    for i in range(len(flat)):
        if flat[i][1] == 5:
            if i > 0:
                flat[i - 1] = (flat[i - 1][0] + flat[i][0], flat[i - 1][1])
            if i < len(flat) - 2:
                flat[i + 2] = (flat[i + 1][0] + flat[i + 2][0], flat[i + 2][1])
            flat[i : i + 2] = [(0, flat[i][1] - 1)]
            return flat
    return None


def explode(number: Snail) -> Snail:
    flat = flatten(number)
    exploded = explode_flattened(flat)
    if exploded:
        return reconstruct(exploded)
    return reconstruct(flat)


assert explode([[[[[9, 8], 1], 2], 3], 4]) == [[[[0, 9], 2], 3], 4]
assert explode([7, [6, [5, [4, [3, 2]]]]]) == [7, [6, [5, [7, 0]]]]
assert explode([[6, [5, [4, [3, 2]]]], 1]) == [[6, [5, [7, 0]]], 3]
assert explode([[3, [2, [1, [7, 3]]]], [6, [5, [4, [3, 2]]]]]) == [
    [3, [2, [8, 0]]],
    [9, [5, [4, [3, 2]]]],
]
assert explode([[3, [2, [8, 0]]], [9, [5, [4, [3, 2]]]]]) == [
    [3, [2, [8, 0]]],
    [9, [5, [7, 0]]],
]


def split_flattened(flat: Flat) -> Flat | None:
    for i in range(len(flat)):
        n, d = flat[i]
        if n >= 10:
            flat[i : i + 1] = [(n // 2, d + 1), ((n + 1) // 2, d + 1)]
            return flat
    return None


def reduce_flattened(flat: Flat) -> Snail:
    while True:
        exploded = explode_flattened(flat)
        if exploded:
            flat = exploded
            continue
        split = split_flattened(flat)
        if split:
            flat = split
            continue
        return reconstruct(flat)


def add_snailfish(numbers: list[Snail]) -> Snail:
    total = numbers[0]
    for n in numbers[1:]:
        total = reduce_flattened(flatten([total, n]))
    return total


def magnitude(number: Snail) -> int:
    if isinstance(number, int):
        return number
    return 3 * magnitude(number[0]) + 2 * magnitude(number[1])


def load(filename: str) -> list[Snail]:
    numbers = [json.loads(line) for line in open(filename)]
    return numbers


def part1(numbers: list[Snail]) -> int:
    # print('input', numbers)
    total: Snail = add_snailfish(numbers)
    # print(total)
    return magnitude(total)


print(part1(load("../input/day18.txt")))


def pairs(numbers):
    for a in numbers:
        for b in numbers:
            if a != b:
                yield [a, b]


def part2(numbers: list[Snail]) -> int:
    return max(part1(pair) for pair in pairs(numbers))


print(part2(load("../input/day18.txt")))
