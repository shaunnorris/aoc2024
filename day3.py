from aoclib import read_file_lines
import re

testlines = read_file_lines('day3-test.txt')
testline = "".join(testlines)

def test_find_mults():
    assert find_mults(testline) == 322
    
def find_mults(line):
    total = 0
    pattern = r'mul\((\d+),(\d+)\)'
    valid_strings = re.findall(pattern, line)
    number_pairs = [(int(a), int(b)) for a, b in valid_strings]
    for pair in number_pairs:
        total += pair[0] * pair[1]
    return total

lines = read_file_lines('day3-input.txt')
bigline = "".join(lines)
part1 = find_mults(bigline)
print('part1:',part1)

def test_chop_input():
    assert find_mults(chop_input(testline)) == 96
    
def chop_input(line):
    dont_pattern = r"don't\(\)"
    donts = [m.start() for m in re.finditer(dont_pattern, line)]
    do_pattern = r"do\(\)"
    dos = [m.start() for m in re.finditer(do_pattern, line)]
    
    newline = ''
    keep = True
    for i in range(len(line)):
        if i in donts:
            keep = False
        if i in dos:
            keep = True
        if keep:
            newline += line[i]
    return newline

part2 = find_mults(chop_input(bigline))
print('part2:',part2)