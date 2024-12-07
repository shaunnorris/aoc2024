from aoclib import read_file_lines

def test_find_start():
    assert find_start(read_file_lines('day6-test.txt')) == ('U',6,4)
    
def find_start(lines):
    for linenum, line in enumerate(lines):
        if '^' in line:
            return 'U', linenum,line.index('^')
        
def test_walk_around():
    assert walk_around(read_file_lines('day6-test.txt')) == 41
    assert walk_around(read_file_lines('day6-loop-test.txt')) == 0
    
def walk_around(grid):
    walked = []
    rightturns = []
    walkmap = {'U': (-1,0), 'D': (1,0), 'L': (0,-1), 'R': (0,1)}
    rightturn = {'U': 'R', 'R': 'D', 'D': 'L', 'L': 'U'}
    start = find_start(grid)
    in_grid = True
    direction = start[0]
    pos = start[1:]
    while in_grid:   
       target = (pos[0] + walkmap[direction][0], pos[1] + walkmap[direction][1])
       if pos not in walked:
               walked.append(pos)
       if target[0] < 0 or target[0] >= len(grid[0]) or target[1] < 0 or target[1] >= len(grid):
           in_grid = False
       elif grid[target[0]][target[1]] == '#':
            direction = rightturn[direction]
            if (direction,pos) in rightturns:
                return 0
            rightturns.append((direction,pos))
       else:
           pos = (pos[0] + walkmap[direction][0], pos[1] + walkmap[direction][1])
    return len(walked)

grid = read_file_lines('day6-input.txt')
part1 = walk_around(grid)
print('part1:',part1)

def test_find_loops():
    assert find_loops(read_file_lines('day6-test.txt')) == 6
    
def find_loops(grid):
    loopsfound = 0
    for i in range(len(grid)):
        for j in range(len(grid[0])):
            checkgrid = [list(row) for row in grid]  # Create a copy of the grid as a list of lists
            if checkgrid[i][j] == '.':
                checkgrid[i][j] = '#'
                checkgrid[i] = ''.join(checkgrid[i])  # Convert the list back to a string
                print('.')
                if walk_around(checkgrid) == 0:
                    loopsfound += 1
    return loopsfound

part2 = find_loops(grid)
print('part2:',part2)