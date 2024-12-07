from aoclib import read_file_lines
import numpy as np

def test_get_numbersets():
    testdata = read_file_lines('day7-test.txt')
    parseddata = get_numbersets(testdata)
    assert len(parseddata) == 9
    
def get_numbersets(lines):
    numbersets = []
    for line in lines:
        leftside,rightside = line.split(':')
        target = int(leftside.strip())
        numstrings = rightside.strip().split(' ')
        operands = [int(x) for x in numstrings]
        numbersets.append([target,operands])
    return numbersets

def test_generate_operators():
    assert generate_operators(2) == [['+', '+'], ['+', '*'], ['*', '+'], ['*', '*']]

def generate_operators(length):
    binary_numbers = [bin(i)[2:].zfill(length) for i in range(2**length)]
    return [['+' if bit == '0' else '*' for bit in num] for num in binary_numbers]




def test_find_valid_sets():
    testdata = read_file_lines('day7-test.txt')
    testsets = get_numbersets(testdata)
    assert find_valid_sets(testsets) == 3749

def find_valid_sets(sets):
    validsum = 0
    for numberset in sets:
            if check_validity(numberset):
                validsum += numberset[0]
    return validsum

def test_check_validity():
    assert check_validity([3267, [81, 40, 27]]) == True
    assert check_validity([21037,[9, 7, 18, 13]]) == False

def check_validity(expression):
    target,operands = expression[0],expression[1]
    if len(operands) > 1:     
        operatorset = generate_operators(len(operands)-1)
        for option in operatorset:
            result = operands[0]
            for i in range(len(option)):
                if option[i] == '+':
                    result += operands[i+1]
                elif option[i] == '*':
                    result *= operands[i+1]
            if result == target:
                return True
    else:
        if operands[0] == target:
            return True
    return False


def test_base3():
    assert base3(1) == ['0', '1','2']
    assert base3(2) == ['00', '01','02', '10', '11', '12', '20', '21', '22']

def base3(n):
    return [np.base_repr(i, 3).zfill(n) for i in range(3**n)]
   

def test_gen_concat_operators(): 
    assert gen_concat_operators(1) == [['+'], ['*'], ['c']]
    assert len(gen_concat_operators(2)) == 9
    assert len(gen_concat_operators(3)) == 27
def gen_concat_operators(length):
    base3_numbers = base3(length)
    combined_list = [['+' if bit == '0' else '*' if bit == '1' else 'c' for bit in num] for num in base3_numbers]
    return combined_list


def test_concat():
    assert check_concat([156, [15, 6]]) == True
    assert check_concat([7290, [6, 8, 6, 15]]) == True
    assert check_concat([3267, [81, 40, 27]]) == True
    assert check_concat([192, [17,8,14]]) == True
    assert check_concat([190,[10,19]]) == True
    
def check_concat(expression):
    target,operands = expression[0],expression[1]
    operatorset = gen_concat_operators(len(operands)-1)
    for option in operatorset:
        result = operands[0]
        for i in range(len(option)):
            if option[i] == '+':
                result += operands[i+1]
            elif option[i] == '*':
                result *= operands[i+1]
            elif option[i] == 'c':
                result = int(str(result) + str(operands[i+1]))
        if result == target:
            return True
    return False

def test_part2():
    testdata = read_file_lines('day7-test.txt')
    testsets = get_numbersets(testdata)
    assert part2(testsets) == 11387

def part2(sets):
    validsum = 0
    for numberset in sets:
        if check_concat(numberset):
            validsum += numberset[0]
    return validsum

numbersets = get_numbersets(read_file_lines('day7-input.txt'))
part1 = find_valid_sets(numbersets)
print('part1:',part1)
parttwo = part2(numbersets)
print('part2:',parttwo)



