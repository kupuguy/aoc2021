def read_board(f):
    board = []
    for row in range(5):
        board.append([int(n) for n in f.readline().strip().split()])
        if not len(board[-1])==5: return None
    assert not f.readline().strip()
    return board

def mark(board, numbers):
    '''Returns count numbers needed and score for board'''
    rows = [set(b) for b in board]
    columns = [set(b) for b in zip(*board)]
    for count, number in enumerate(numbers):
        for row in rows:
            if number in row:
                row.remove(number)
                if not row:
                    return count, sum(sum(r) for r in rows) * number
        for col in columns:
            if number in col:
                col.remove(number)
                if not col:
                    return count, sum(sum(c) for c in columns) * number
    
with open('../input/day4.txt') as f:
    numbers = [int(n) for n in f.readline().strip().split(',')]
    assert not f.readline().strip()
    boards = []
    while not boards or boards[-1] is not None:
        boards.append(read_board(f))
    boards.pop(-1)
    
    
print(f"{numbers=}")
print(f"{len(boards)=}")
scores = [mark(b, numbers) for b in boards]
winner = min(scores)
print(winner)
print(max(scores))
