from aoclib import read_file_lines

testrocks = [125, 17]

def test_blink():
    assert blink(125) == (253000,None)
    assert blink(0) == (1,None)
    assert blink(10) == (1,0)
    assert blink(1) == (2024,None)

def blink(rock):
    if rock == 0:
        return (1,None)
    elif len(str(rock)) % 2 == 0:
        rock1 = int(str(rock)[:len(str(rock))// 2])
        rock2 = int(str(rock)[len(str(rock))// 2:])
        return (rock1,rock2)
    else:
        return (rock * 2024, None)

def test_multi_blink():
    assert multi_blink(testrocks,25) == 55312
    
def multi_blink(rocks,n):
    rockcount = {}
    for rock in rocks:
        if rock in rockcount.keys():
            rockcount[rock] += 1
        else:
            rockcount[rock] = 1

    for i in range(n):
        nextcount = {}
        current_row = list(rockcount.keys())
        for rock in current_row:
            next_rocks = blink(rock)
            for newrock in next_rocks:
                if newrock != None:
                    if newrock in nextcount.keys():
                        nextcount[newrock] += 1 * rockcount[rock]
                    else:
                        nextcount[newrock] = 1 * rockcount[rock]
        rockcount = nextcount
    return sum(rockcount.values())

rocksstr = read_file_lines('day11-input.txt')[0].split(" ")
day11rocks = [int(s) for s in rocksstr]
part1 = multi_blink(day11rocks,25)
print('part1',part1)
part2 = multi_blink(day11rocks,75)
print('part2',part2)