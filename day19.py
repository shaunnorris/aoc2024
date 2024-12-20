from aoclib import read_file_lines
from collections import deque

def test_load_patterns():
    lines = read_file_lines('day19-test.txt')
    assert load_patterns(lines) == {
        "towels": ["r", "wr", "b", "g", "bwu", "rb", "gb", "br"],
        "patterns": [
            "brwrr",
            "bggr",
            "gbbr",
            "rrbgbr",
            "ubwu",
            "bwurrg",
            "brgr",
            "bbrgwb",
        ],
    }


def load_patterns(lines):
    patterns = []
    for line in lines:
        if "," in line:
            towels = [towel.strip() for towel in line.split(",")]
        elif len(line) > 0:
            patterns.append(line)
    return {'towels':towels, 'patterns':patterns}

def test_match_substrings():
    # Test case 1: Simple match
    towels = ["ab", "cd"]
    given_string = "abcd"
    assert match_substrings(given_string, towels) == True

    # Test case 2: No match
    towels = ["ab", "cd"]
    given_string = "efgh"
    assert match_substrings(given_string, towels) == False

    # Test case 3: Multiple matches
    towels = ["ab", "abc", "abcd"]
    given_string = "abcd"
    assert match_substrings(given_string, towels) == True

    # Test case 4: Overlapping matches
    towels = ["ab", "bc", "cd"]
    given_string = "abcd"
    assert match_substrings(given_string, towels) == True

    # Test case 5: Empty string
    towels = ["ab", "cd"]
    given_string = ""
    assert match_substrings(given_string, towels) == True

    # Test case 6: Empty towels list
    towels = []
    given_string = "abcd"
    assert match_substrings(given_string, towels) == False

    # Test case 7: Towels list with single element
    towels = ["abcd"]
    given_string = "abcd"
    assert match_substrings(given_string, towels) == True

    # Test case 8: Given string is a substring of a towel
    towels = ["abcd"]
    given_string = "ab"
    assert match_substrings(given_string, towels) == False

def match_substrings(given_string, towels):
    queue = deque()
    for towel in towels:
        if given_string.startswith(towel):
            queue.append(towel)

    # Try to combine substrings to form the original string
    def combine_substrings(queue, remaining_string):
        if not remaining_string:
            return True
        for towel in towels:  # Changed queue to towels
            if remaining_string.startswith(towel):
                new_remaining_string = remaining_string[len(towel):]
                if combine_substrings(queue, new_remaining_string):
                    return True
        return False

    return combine_substrings(queue, given_string)

def test_towel_match():
    testdata = load_patterns(read_file_lines('day19-test.txt'))
    assert towel_match(testdata) == 6
    
def towel_match(toweldata):
    towels = toweldata['towels']
    patterns = toweldata['patterns']
    count = 0
    for pattern in patterns:
        if match_substrings(pattern, towels):
            count += 1
    return count

def test_count_substrings():
    # Test case 1: Simple match
    towels = ["ab", "cd"]
    given_string = "abcd"
    assert count_substrings(given_string, towels) == 1

    # Test case 2: No match
    towels = ["ab", "cd"]
    given_string = "efgh"
    assert count_substrings(given_string, towels) == 0

    # Test case 3: Multiple matches
    towels = ["ab", "bc", "cd","a","d"]
    given_string = "abcd"
    assert count_substrings(given_string, towels) == 2

    # Test case 4: Overlapping matches
    towels = ["ab", "bc", "cd"]
    given_string = "abcd"
    assert count_substrings(given_string, towels) == 1

    # Test case 5: Empty string
    towels = ["ab", "cd"]
    given_string = ""
    assert count_substrings(given_string, towels) == 1

    # Test case 6: Empty towels list
    towels = []
    given_string = "abcd"
    assert count_substrings(given_string, towels) == 0

    # Test case 7: Towels list with single element
    towels = ["abcd"]
    given_string = "abcd"
    assert count_substrings(given_string, towels) == 1

    # Test case 8: Given string is a substring of a towel
    towels = ["abcd"]
    given_string = "ab"
    assert count_substrings(given_string, towels) == 0

    # Test case 9: No combinations, but string is not empty
    towels = ["ab", "cd"]
    given_string = "efgh"
    assert count_substrings(given_string, towels) == 0
    
    # Test case 10: Multiple combinations
    towels = ["a", "b", "ab"]
    given_string = "ab"
    assert count_substrings(given_string, towels) == 2

    # Test case 11: Multiple combinations
    towels = ["a", "b", "c", "ab", "bc"]
    given_string = "abc"
    assert count_substrings(given_string, towels) == 3

def count_substrings(given_string, towels):
    queue = deque()
    for towel in towels:
        if given_string.startswith(towel):
            queue.append(towel)

    memo = {}  # Memoization table

    def combine_substrings(remaining_string):
        if remaining_string in memo:
            return memo[remaining_string]
        if not remaining_string:
            return 1  # Base case: empty string has 1 combination (the empty combination)
        count = 0
        for towel in towels:
            if remaining_string.startswith(towel):
                new_remaining_string = remaining_string[len(towel):]
                count += combine_substrings(new_remaining_string)
        if count == 0 and remaining_string:  # If no towels match and string is not empty
            return 0
        memo[remaining_string] = count
        return count

    return combine_substrings(given_string)

def test_towel_count():
    testdata = load_patterns(read_file_lines('day19-test.txt'))
    assert towel_count(testdata) == 16
    
def towel_count(toweldata):
    towels = toweldata['towels']
    patterns = toweldata['patterns']
    count = 0
    for pattern in patterns:
        count += count_substrings(pattern, towels)
    return count

toweldata = load_patterns(read_file_lines('day19-input.txt'))
part1 = towel_match(toweldata)
print('part1:', part1)
part2 = towel_count(toweldata)
print('part2:', part2)


