from rich import print


def maxy(ymax, ymin):
    possible = 0
    possytop = 0
    for v in range(1, abs(ymin) + 1):
        ytop = 0
        for steps in range(1, 10000):
            y = steps * v - steps * (steps - 1) // 2
            ytop = max(ytop, y)
            if y < ymin:
                break
            if ymin <= y <= ymax:
                # print(f"{v=}, {steps=}, {y=}")
                possible = v
                possytop = ytop
                break
    return possible, steps, possytop


def x_velocity(xmin, xmax, steps):
    for velocity in range(xmin // steps, xmax + 1):
        st = min(steps, velocity)
        x = velocity * st - st * (st - 1) // 2
        if xmin <= x <= xmax:
            return velocity


def part1(xmin, xmax, ymin, ymax):
    yv, steps, ytop = maxy(ymax, ymin)
    xv = x_velocity(xmin, xmax, steps)
    # print(xv,yv, steps,ytop)
    return (xv, yv), ytop


assert part1(20, 30, -10, -5) == ((6, 9), 45)
print("Part1", part1(117, 164, -140, -89))


def all_y(ymax, ymin):
    for v in range(ymin, abs(ymin) + 1):
        for steps in range(1, 10000):
            y = steps * v - steps * (steps - 1) // 2
            if y < ymin:
                break
            if ymin <= y <= ymax:
                # print(f"{v=}, {steps=}, {y=}")
                yield v, steps


def all_x(xmin, xmax, steps):
    pos = 0
    for velocity in range(xmin // steps, xmax + 1):
        st = min(steps, velocity)
        x = velocity * st - st * (st - 1) // 2
        if xmin <= x <= xmax:
            yield velocity


def part2(xmin, xmax, ymin, ymax):
    possible = set()
    for yv, steps in all_y(ymax, ymin):
        for xv in all_x(xmin, xmax, steps):
            possible.add((xv, yv))
    return len(possible)


assert part2(20, 30, -10, -5) == 112
p2 = part2(117, 164, -140, -89)
print("Part2", p2)
