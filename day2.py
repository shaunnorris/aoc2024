from aoclib import read_file_lines

testlines = read_file_lines('day2-test.txt')

def test_get_reports():
    test_reports = get_reports(testlines)
    assert test_reports == [
        [7, 6, 4, 2, 1],
        [1, 2, 7, 8, 9],
        [9, 7, 6, 2, 1],
        [1, 3, 2, 4, 5],
        [8, 6, 4, 4, 1],
        [1, 3, 6, 7, 9],
    ]


def get_reports(lines):
    reports = []
    for line in lines:
        report = [int(num) for num in line.split()]
        reports.append(report)
    return reports

def test_check_safety():
    test_reports = get_reports(testlines)
    assert check_safety([7, 6, 4, 2, 1]) == True
    assert check_safety( [1, 2, 7, 8, 9])   == False
    assert check_safety( [9, 7, 6, 2, 1])   == False   
    assert check_safety( [1, 3, 2, 4, 5])   == False
    assert check_safety( [8, 6, 4, 4, 1])   == False
    assert check_safety( [1, 3, 6, 7, 9])   == True
    

def check_safety(report):
    #safe if both of the following are true:
    #   The levels are either all increasing or all decreasing.
    #   Any two adjacent levels differ by at least one and at most three.
    increasing = all(x < y for x, y in zip(report, report[1:]))
    decreasing = all(x > y for x, y in zip(report, report[1:]))
    in_limits = all(1 <= abs(x - y) <= 3 for x, y in zip(report, report[1:]))
    if increasing or decreasing:
        if in_limits:
            return True
    return False


def test_safety_count():
    test_reports = get_reports(testlines)
    assert safety_count(test_reports) == 2
    
def safety_count(reports):
    return sum(check_safety(report) for report in reports)

day2_lines = read_file_lines('day2-input.txt')
day2_reports = get_reports(day2_lines)

part1 = safety_count(day2_reports)
print('part1:',part1)

def test_check_safety_with_damper():
        assert check_safety_with_damper([7, 6, 4, 2, 1]) == True
        assert check_safety_with_damper( [1, 2, 7, 8, 9])   == False
        assert check_safety_with_damper( [9, 7, 6, 2, 1])   == False
        assert check_safety_with_damper( [1, 3, 2, 4, 5])   == True
        assert check_safety_with_damper( [8, 6, 4, 4, 1])   == True
        assert check_safety_with_damper( [1, 3, 6, 7, 9])   == True   

def check_safety_with_damper(report):
    safety = False
    for i in range(len(report)):
        subset = report[:i] + report[i+1:]
        if check_safety(subset):
            safety = True
    return safety

def test_damper_safety_count():
    test_reports = get_reports(testlines)
    assert damper_safety_count(test_reports) == 4

def damper_safety_count(reports):
    return sum(check_safety_with_damper(report) for report in reports)

part2 = damper_safety_count(day2_reports)
print('part2:',part2)