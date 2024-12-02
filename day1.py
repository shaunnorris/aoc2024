from aoclib import read_file_lines

testlines = read_file_lines('day1-test.txt')
def test_get_lists():   
    assert get_lists(testlines) == ([1, 2, 3, 3, 3, 4], [3, 3, 3, 4, 5, 9])

def get_lists(lines):
    llist = []
    rlist = []
    for line in lines:
        left, right = map(int, line.split())
        llist.append(left)
        rlist.append(right)
    return sorted(llist), sorted(rlist)

def test_get_distance():
    testlists = get_lists(testlines)
    assert get_distance(testlists) == 11
    
def get_distance(lists):
    return sum([abs(a-b) for a, b in zip(lists[0], lists[1])])

def test_get_similarity():
    testlists = get_lists(testlines)
    assert get_similarity(testlists) == 31

def get_similarity(lists):
    similarity = 0
    left, right = lists
    for number in left:
        similarity += number * right.count(number)
    return similarity

day1lists = get_lists(read_file_lines('day1-input.txt'))
part1 = get_distance(day1lists)
print('part1:',part1)
part2 = get_similarity(day1lists)
print('part2:',part2)