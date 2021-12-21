from functools import cache


def die():
    while True:
        for roll in range(1, 101):
            yield roll


def part1(p1, p2):
    d100 = die()
    score1, score2 = 0, 0
    rolls = 0
    while score1 < 1000 and score2 < 1000:
        rolls += 3
        d = next(d100) + next(d100) + next(d100)
        p1 = (p1 + d - 1) % 10 + 1
        score1 += p1
        if score1 >= 1000:
            return score2 * rolls

        rolls += 3
        d = next(d100) + next(d100) + next(d100)
        p2 = (p2 + d - 1) % 10 + 1
        score2 += p2
        if score2 >= 1000:
            return score1 * rolls


assert part1(p1=4, p2=8) == 739785
print(part1(p1=10, p2=9))


ROLLS = {6: 7, 5: 6, 7: 6, 4: 3, 8: 3, 3: 1, 9: 1}
BACKWARD = {
    pos: {roll: (pos - roll + 9) % 10 + 1 for roll in ROLLS} for pos in range(1, 11)
}


@cache
def ways_to_reach(score, position, turns, start):
    if score == 0 and turns == 0 and position == start:
        return 1
    if score < 1 or turns == 0:
        return 0
    return sum(
        ways_to_reach(score - position, BACKWARD[position][r], turns - 1, start) * prob
        for r, prob in ROLLS.items()
    )


@cache
def all_ways_to_reach(score, turns, start):
    return sum(
        ways_to_reach(score, position, turns, start) for position in range(1, 11)
    )


@cache
def ways_to_win(turns, start):
    ways = 0
    for final_score in range(21, 31):
        for prev_score in range(final_score - 10, min(final_score, 21)):
            final_pos = final_score - prev_score
            ways += sum(
                ways_to_reach(prev_score, BACKWARD[final_pos][r], turns - 1, start)
                * ROLLS[r]
                for r in ROLLS
            )
    return ways


@cache
def ways_to_lose(turns, start):
    return sum(all_ways_to_reach(score, turns, start) for score in range(21))


def part2(p1, p2):
    p1_wins = sum(
        ways_to_win(turns, p1) * ways_to_lose(turns - 1, p2) for turns in range(2, 22)
    )
    p2_wins = sum(
        ways_to_win(turns, p2) * ways_to_lose(turns, p1) for turns in range(2, 22)
    )
    # print(p1_wins, p2_wins)
    return max(p1_wins, p2_wins)


assert part2(p1=4, p2=8) == 444356092776315
print(part2(p1=10, p2=9))
