from aoclib import read_file_lines, transpose
import fnvhash

def test_load_mirrors():
    testdata = read_file_lines('day2313-test.txt')
    assert len(load_mirrors(testdata)) == 2
    
def load_mirrors(data):
    mirrors = []
    current_mirror = []
    for line in data:
        if line == '':
            mirrors.append(current_mirror)
            current_mirror = []
        else:
            current_mirror.append(line)
    mirrors.append(current_mirror)
    return mirrors

def test_get_binary():
    assert get_binary("#.##..##.") == 358
    
def get_binary(line):
    binary_string = ''.join(['1' if x == '#' else '0' for x in line])
    return int(binary_string, 2)

def test_convert_mirror():
    testmirror = load_mirrors(read_file_lines('day2313-test.txt'))[0]
    assert convert_mirror(testmirror) == [[358, 90, 385, 385, 90, 102, 346],[89, 24, 103, 66, 37, 37, 66, 103, 24]]
    
def convert_mirror(mirror):
    horizontal = [get_binary(xline) for xline in mirror]
    vertical = [get_binary(yline) for yline in transpose(mirror)]
    return [horizontal, vertical]

def test_find_dupes():
    assert find_dupes([358, 90, 385, 385, 90, 102, 346]) == [2]
    assert find_dupes([89, 24, 103, 66, 37, 37, 66, 103, 24]) == [4]
    assert find_dupes([1,2,3,3,4,5,6,6,7,8,9,9]) == [2,6,10]
    
def find_dupes(lst):
    duplicates = []
    for i in range(len(lst) - 1):
        if lst[i] == lst[i + 1]:
            duplicates.append(i)
    return duplicates

def test_reflection():
    assert reflection([358, 90, 385, 385, 90, 102, 346]) == False
    assert reflection([89, 24, 103, 66, 37, 37, 66, 103, 24]) == 5
    assert reflection([1,2,2,3,4,5,5,6,7,8,8,7,6,5,5,4,3]) == 10

def reflection(line):
    pairs = find_dupes(line)
    for pair in pairs:
        cut = pair +1
        leftside = line[:cut]
        rightside = line[cut:]
        revleft = leftside[::-1]
        shortest_index = min(len(leftside), len(rightside))
        if revleft[:shortest_index] == rightside[:shortest_index]:
            return cut
    return False

def test_tally_mirrors():
    testdata = read_file_lines('day2313-test.txt')
    assert tally_mirrors(load_mirrors(testdata)) == 405
    
def tally_mirrors(mirrors):
    total = 0
    for mirror in mirrors:
        h,v = convert_mirror(mirror)
        htest = reflection(h)
        if not htest:
            vtest = reflection(v)
            total += vtest
        else:
            total += htest * 100
    return total

part1 = tally_mirrors(load_mirrors(read_file_lines('day2313-input.txt')))
print('part1:',part1)