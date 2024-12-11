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
    
def test_blink_row():
    assert blink_row(testrocks) == [253000, 1, 7]

def blink_row(rocks):
    newrow = []
    for rock in rocks:
        rock = int(rock)
        newrocks = blink(rock)
        for newrock in newrocks:
            if newrock != None:
                newrow.append(newrock)
    return newrow

def test_multi_blink():
    assert len(multi_blink(testrocks,25)) == 55312
    
def multi_blink(rocks,n):
    current_row = rocks
    for i in range(n):
        nextrow = blink_row(current_row)
        current_row = nextrow
        print(i, len(current_row))
    return current_row

#rocksstr = read_file_lines('day11-input.txt')[0].split(" ")
rocksstr = "0"
day11rocks = [int(s) for s in rocksstr]
part1 = len(multi_blink(day11rocks,25))
print('part1',part1)

part2 = multi_blink(day11rocks,75)
print('part2',part2)