from rich import print

def load(filename: str):
    coords = {}
    folds = []
    for line in open(filename):
        if line.strip():
            if line.startswith('fold along x='):
                folds.append(['x', int(line.split('=')[-1])])
            elif line.startswith('fold along y='):
                folds.append(['y', int(line.split('=')[-1])])
            else:
                x,y=map(int, line.split(','))
                coords[x,y]='#'
    return coords, folds

def fold_y(coords, fold_y):
    for x,y in list(coords):
        if y >= fold_y:
            del coords[x,y]
            coords[x, 2*fold_y-y] = '#'

def fold_x(coords, fold_x):
    for x,y in list(coords):
        if x >= fold_x:
            del coords[x,y]
            coords[2*fold_x-x, y] = '#'
            
def part1(filename):
    coords, folds = load(filename)
    xy, n = folds[0]
    if xy=='x':
        fold_x(coords, n)
    else:
        fold_y(coords, n)
    return len(coords)

assert part1('../input/day13-test.txt')==17
print("part 1", part1('../input/day13.txt'))

def part2(filename):
    coords, folds = load(filename)
    for xy, n in folds:
        if xy=='x':
            fold_x(coords, n)
        else:
            fold_y(coords, n)
    max_y = max(y for x,y in coords)
    max_x = max(x for x,y in coords)
    for y in range(max_y+1):
        print(''.join(coords.get((x,y), ' ') for x in range(max_x+1)))
        
    return len(coords)
    
part2('../input/day13-test.txt')
part2('../input/day13.txt')
