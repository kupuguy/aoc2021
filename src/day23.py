from rich import print
from collections import deque

COSTS = {"A": 1, "B": 10, "C": 100, "D": 1000}

NO_STOP = {2, 4, 6, 8}
TARGET = {
    "A": {11, 12, 13, 14},
    "B": {15, 16, 17, 18},
    "C": {19, 20, 21, 22},
    "D": {23, 24, 25, 26},
}
TARGET_TOP = {"A": 11, "B": 15, "C": 19, "D": 23}


def switch(state, a, b):
    t = list(state)
    t[a], t[b] = t[b], t[a]
    return "".join(t)


START = "..........." "DDDD" "CCBA" "BBAA" "CACB"
START_TEST = "..........." "BDDA" "CCBD" "BBAC" "DACA"

R1T = 11
R2T = 15
R3T = 19
R4T = 23


def moves2(state):
    # room top to room lower if target room and empty
    for rt in (R1T, R2T, R3T, R4T):
        if (
            state[rt] != "."
            and all(state[rt + n] in (".", state[rt]) for n in (1, 2, 3))
            and rt in TARGET[state[rt]]
        ):
            if state[rt + 1] == ".":
                if state[rt + 2] == ".":
                    if state[rt + 3] == ".":
                        yield switch(state, rt, rt + 3), COSTS[state[rt]] * 3
                        return
                    else:
                        yield switch(state, rt, rt + 2), COSTS[state[rt]] * 2
                        return
                else:
                    yield switch(state, rt, rt + 1), COSTS[state[rt]]
                    return

    # room lower to room top if empty and not target room
    for rt, target in ((R1T, "A"), (R2T, "B"), (R3T, "C"), (R4T, "D")):
        if state[rt] == "." and any(
            state[rt + n] not in (".", target) for n in (1, 2, 3)
        ):
            if state[rt + 1] != ".":
                yield switch(state, rt, rt + 1), COSTS[state[rt + 1]]
                return
            elif state[rt + 2] != ".":
                yield switch(state, rt, rt + 2), 2 * COSTS[state[rt + 2]]
                return
            else:
                yield switch(state, rt, rt + 3), 3 * COSTS[state[rt + 3]]
                return

    # hallway to room top if target and empty and room lower empty or has target and intervening empty
    for hall in range(11):
        if state[hall] == ".":
            continue
        target = TARGET_TOP[state[hall]]
        if state[target] != "." or any(
            state[target + n] not in (".", state[hall]) for n in (1, 2, 3)
        ):
            continue
        h0 = (target - 11) // 2 + 2
        if h0 > hall and all(state[h] == "." for h in range(hall + 1, h0)):
            yield switch(state, hall, target), COSTS[state[hall]] * (h0 - hall + 1)
            return
        elif h0 < hall and all(state[h] == "." for h in range(h0, hall)):
            yield switch(state, hall, target), COSTS[state[hall]] * (hall - h0 + 1)
            return

    # room top to hallway space excluding no_stop and intervening empty
    for rt in (R1T, R2T, R3T, R4T):
        if state[rt] == ".":
            continue
        # Don't move out if right room and no blocker
        if rt in TARGET[state[rt]] and all(
            state[rt + n] in (".", state[rt]) for n in (1, 2, 3)
        ):
            continue
        h0 = (rt - 11) // 2 + 2
        for hall in range(h0 - 1, -1, -1):
            if hall in NO_STOP:
                continue
            if state[hall] != ".":
                break
            yield switch(state, rt, hall), COSTS[state[rt]] * (h0 - hall + 1)
        for hall in range(h0 + 1, 11):
            if hall in NO_STOP:
                continue
            if state[hall] != ".":
                break
            yield switch(state, rt, hall), COSTS[state[rt]] * (hall - h0 + 1)


def show(state, cost):
    print(
        f"""\
        ############# {cost}
        #{state[:11]}#
        ###{state[11]}#{state[15]}#{state[19]}#{state[23]}###
          #{state[12]}#{state[16]}#{state[20]}#{state[24]}#
          #{state[13]}#{state[17]}#{state[21]}#{state[25]}#
          #{state[14]}#{state[18]}#{state[22]}#{state[26]}#
          #########
"""
    )


def part2(start: str, trace=False) -> int:
    all_states = {start: (0, None)}
    queue = deque([start])
    while queue:
        state = queue.popleft()
        cost, prev = all_states[state]
        # print(state, cost)
        for next, next_cost in moves2(state):
            if next in all_states and all_states[next][0] <= cost + next_cost:
                continue
            all_states[next] = (cost + next_cost, state)
            queue.append(next)

    st = "...........AAAABBBBCCCCDDDD"
    path = []
    while st:
        path.append((st, all_states[st][0]))
        st = all_states[st][1]
    if trace:
        for st, cost in path[::-1]:
            show(st, cost)
    return all_states["...........AAAABBBBCCCCDDDD"][0]


assert part2(START_TEST) == 44169
print("Part 2", part2(START, True))
