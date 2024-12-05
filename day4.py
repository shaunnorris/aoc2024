from aoclib import read_file_lines, transpose
import re

def test_count_string():
    assert count_string('XMAS','MMMSXXMASM') == 1
    assert count_string('SAMX','MSAMXMSMSA') == 1
    
def count_string(string, line):
    return line.count(string)

def test_diagonal_slices():
    assert diagonal_slices(["abc", "def", "ghi"]) == {
        "up":  ['a', 'bd', 'ceg', 'fh', 'i'],
        "down": ['g', 'dh', 'aei', 'bf', 'c']}


def diagonal_slices(grid):
    rows, cols = len(grid), len(grid[0])
    diagonals_up = [[] for _ in range(rows + cols - 1)]
    diagonals_down = [[] for _ in range(rows + cols - 1)]

    for i in range(rows):
        for j in range(cols):
            diagonals_up[i + j].append(grid[i][j])
            diagonals_down[rows - i - 1 + j].append(grid[i][j])

    return {
        "up": ["".join(diag) for diag in diagonals_up],
        "down": ["".join(diag) for diag in diagonals_down]
    }
    
def test_count_all_strings():
    testgrid = read_file_lines('day4-test.txt')
    assert count_all_strings(testgrid) == 18

def count_all_strings(grid):
    count = 0
    for line in grid:
        count += count_string('XMAS', line)
        count += count_string('SAMX', line)
    for line in transpose(grid):
        count += count_string('XMAS', line)
        count += count_string('SAMX', line)
    for line in diagonal_slices(grid)['up']:
        count += count_string('XMAS', line)
        count += count_string('SAMX', line)
    for line in diagonal_slices(grid)['down']:
        count += count_string('XMAS', line)
        count += count_string('SAMX', line)
    return count

grid = read_file_lines('day4-input.txt')

part1 = count_all_strings(grid)
print('part1:',part1)

def test_count_xmas():
    testgrid = read_file_lines('day4-test.txt')
    assert count_xmas(testgrid) == 9
    
def count_xmas(grid):
    xcount = 0
    for i in range(len(grid)-2):
        for j in range(len(grid[0])-2):
            downrt = ''.join(grid[i][j] + grid[i+1][j+1] + grid[i+2][j+2])
            upright = ''.join(grid[i+2][j] + grid[i+1][j+1] + grid[i][j+2])
            if downrt in ['SAM','MAS'] and upright in ['SAM','MAS']:
                xcount += 1
    return xcount    

part2 = count_xmas(grid)
print('part2:',part2)