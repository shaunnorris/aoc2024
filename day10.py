from aoclib import read_file_lines, get_mapsize, in_bounds, tuple_add

def test_find_trails():
    testmap = read_file_lines('day10-test.txt')
    assert (
        find_trailheads(testmap) == [
            (0, 2),
            (0, 4),
            (2, 4),
            (4, 6),
            (5, 2),
            (5, 5),
            (6, 0),
            (6, 6),
            (7, 1),
        ]
    )


def find_trailheads(grid):
    mapsize = get_mapsize(grid)
    trailheads = []
    for r in range(len(grid)):
        for c in range(len(grid[0])):
            if int(grid[r][c]) == 0:
                trailheads.append((r,c))
    return trailheads

def test_adjacent_moves():
    testmap = read_file_lines('day10-test.txt')
    assert adjacent_moves((0,0),get_mapsize(testmap)) == [(1,0),(0,1)]
    assert adjacent_moves((1,1),get_mapsize(testmap)) == [(2,1),(1,2),(0,1),(1,0)]
    assert adjacent_moves((7,7),get_mapsize(testmap)) == [(6,7),(7,6)]
 
def adjacent_moves(coord,size):
    offsets = [(1,0),(0,1),(-1,0),(0,-1)]
    moves = []
    for offset in offsets:
        possible = tuple_add(coord,offset)
        if in_bounds(possible, size):
            moves.append(possible)
    return moves


def test_count_trails():
     testmap = read_file_lines('day10-test.txt')
     assert count_trails(testmap) == 36
     assert count_trails(testmap,2) == 81

     
def count_trails(grid,part=1):
    trailheads = find_trailheads(grid)
    open_trails = []
    for trailhead in trailheads:
        open_trails.append([trailhead])
    finished_trails = []
    mapsize = get_mapsize(grid)
    more_moves = True
    while more_moves:
        if open_trails:
            trail = open_trails.pop()
            r,c = trail[-1]
            if grid[r][c] == '9':
                finished_trails.append(trail)
            else:
                moves = adjacent_moves((r,c),mapsize)
                for move in moves:
                    i, j = move[0],move[1]
                    if int(grid[i][j]) == int(grid[r][c]) + 1:
                        trailcopy = trail[:]
                        trailcopy.append((i,j))
                        if trailcopy not in open_trails:
                            open_trails.append(trailcopy)
        else:
            more_moves = False
            
    ts = {}
    for trail in finished_trails:
        th = trail[0]
        te = trail[-1]
        if th in ts.keys():
            if te not in ts[th]:
                ts[th].append(te)
        else:
            ts[th] = [te]
    total = 0
    for key, value in ts.items():
        total += len(value)
    if part == 1:    
        return total
    else:
        return len(finished_trails)

part1 = count_trails(read_file_lines('day10-input.txt'))
part2 = count_trails(read_file_lines('day10-input.txt'),2)
print('part1',part1)
print('part2',part2)