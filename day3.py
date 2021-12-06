data = '''00100
11110
10110
10111
10101
01111
00111
11100
10000
11001
00010
01010'''.split()

data = [l.strip() for l in open('day3.txt').readlines() if l.strip()]

from collections import Counter
most = []
for column in zip(*data):
    counts = Counter(column)
    most.append(counts.most_common(1)[0][0])
    print(counts)
gamma = int(''.join(most), 2)
epsilon = int(''.join('0' if c=='1' else '1' for c in most), 2)
print(gamma * epsilon)

def count_bits(data, pos):
    counts = Counter(d[pos] for d in data)
    print(counts)
    ones, zeros = counts.get('1', 0), counts.get('0', 0)
    keep_bit = '1' if ones >= zeros else '0'
    return [d for d in data if d[pos] == keep_bit]

def keep_least(data, pos):
    counts = Counter(d[pos] for d in data)
    print(counts)
    ones, zeros = counts.get('1', 0), counts.get('0', 0)
    keep_bit = '0' if zeros <= ones else '1'
    return [d for d in data if d[pos] == keep_bit]


data2 = data
pos = 0
while len(data) > 1:
    print("len=", len)
    data = count_bits(data, pos)
    pos += 1
oxygen = int(data[0],2)
print(oxygen)
data = data2
pos = 0
while len(data) > 1:
    print("len=", len)
    data = keep_least(data, pos)
    pos += 1
co2 = int(data[0], 2)
print(co2, oxygen*co2)


    
    
