def load(s: str) -> str:
    return format(int("1" + s, 16), "0b")[1:]


def decode_packet(s: str) -> tuple:
    v = int(s[:3], 2)
    t = int(s[3:6], 2)
    if t == 4:
        # literal
        n = 0
        pos = 6
        while s[pos] == "1":
            n = n * 16 + int(s[pos + 1 : pos + 5], 2)
            pos += 5
        n = n * 16 + int(s[pos + 1 : pos + 5], 2)
        return v, t, n, s[pos + 5 :]
    # operator
    length_type = s[6]
    if length_type == "0":
        bits = int(s[7:22], 2)
        sub_packets = s[22 : 22 + bits]
        packets = []
        while sub_packets:
            sv, st, sb, sub_packets = decode_packet(sub_packets)
            packets.append((sv, st, sb))
        return v, t, packets, s[22 + bits :]
    else:
        n = int(s[7:18], 2)
        sub_packets = s[18:]
        packets = []
        while n > 0:
            sv, st, sb, sub_packets = decode_packet(sub_packets)
            packets.append((sv, st, sb))
            n -= 1
        return v, t, packets, sub_packets


# print(decode_packet('00111000000000000110111101000101001010010001001000000000'))
# print(decode_packet('11101110000000001101010000001100100000100011000001100000'))


def sum_versions(packets):
    v, t, sub = packets
    if isinstance(sub, list):
        return v + sum(sum_versions(p) for p in sub)
    return v


def part1(s: str) -> int:
    packets = decode_packet(load(s))
    total = sum_versions(packets[:3])
    # print("total", total)
    return total


assert part1("8A004A801A8002F478") == 16
assert part1("620080001611562C8802118E34") == 12
assert part1("C0015000016115A2E0802F182340") == 23
assert part1("A0016C880162017C3686B18A3D4780") == 31
print("Part 1", part1(open("../input/day16.txt").read().strip()))


def calculate(packet):
    v, t, x = packet
    match t:
        case 0:  # sum
            return sum(calculate(p) for p in x)
        case 1:  # prod
            prod = 1
            for p in x:
                prod *= calculate(p)
            return prod
        case 2:  # minimum
            return min([calculate(p) for p in x])
        case 3:  # maximum
            return max([calculate(p) for p in x])
        case 4:
            return x
        case 5:  # greater
            return calculate(x[0]) > calculate(x[1])
        case 6:  # less
            return calculate(x[0]) < calculate(x[1])
        case 7:  # equal
            return calculate(x[0]) == calculate(x[1])
        case _:
            assert False, "unknown packet type"


def part2(s: str) -> int:
    packets = decode_packet(load(s))
    total = calculate(packets[:3])
    return total


assert part2("C200B40A82") == 3, "finds the sum of 1 and 2, resulting in the value 3."
assert (
    part2("04005AC33890") == 54
), "finds the product of 6 and 9, resulting in the value 54."
assert (
    part2("880086C3E88112") == 7
), "finds the minimum of 7, 8, and 9, resulting in the value 7."
assert (
    part2("CE00C43D881120") == 9
), "finds the maximum of 7, 8, and 9, resulting in the value 9."
assert part2("D8005AC2A8F0") == 1, "produces 1, because 5 is less than 15."
assert part2("F600BC2D8F") == 0, "produces 0, because 5 is not greater than 15."
assert part2("9C005AC2F8F0") == 0, "produces 0, because 5 is not equal to 15."
assert part2("9C0141080250320F1802104A08") == 1, "produces 1, because 1 + 3 = 2 * 2."

print("Part 2", part2(open("../input/day16.txt").read().strip()))
