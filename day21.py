from aoclib import read_file_lines

def test_load_codes():
    testcodes = read_file_lines('day21-test.txt')
    assert len(testcodes) == 5
    assert testcodes == ['029A', '980A','179A','456A', '379A']

def load_codes(lines):
    codes = []
    for line in lines: 
        codes.append(line.strip())
    return codes

def move_string(leftright,updown):
    output_str = ''
    if updown < 0:
        output_str += "^" * abs(updown)
    elif updown > 0:
        output_str += "v" * abs(updown)
    if leftright < 0:
        output_str += "<" * abs(leftright)
    elif leftright > 0:
        output_str += ">" * abs(leftright)   
    output_str += "A"
    return output_str


def test_dirkp_from_numkp():
    assert dirkp_from_numkp('029A') == "<A^A^^>AvvvA"
    
def dirkp_from_numkp(code):
    kp_positions = {"7": (0,0),"8": (0,1),"9": (0,2),
                    "4": (1,0),"5": (1,1),"6": (1,2),
                    "1": (2,0),"2": (2,1),"3": (2,2),
                    "0": (3,1),"A": (3,2)}
    moves = []
    moves.append("A"+code[0])
    dirkp_string = ''
    for i in range(len(code)-1):
        moves.append(code[i]+code[i+1])
    for move in moves:
        left = kp_positions[move[0]]
        right = kp_positions[move[1]]
        movediff = tuple(b - a for a, b in zip(left, right))
        updown = movediff[0]
        leftright = movediff[1]
        dirkp_string += move_string(leftright,updown)
    return dirkp_string

def test_numkp_from_numkp():
    assert numkp_from_numkp("<A^A^^>AvvvA") == 'v<<A^>>A<A>A<AAv>A^Av<AAA^>A'
    assert len(numkp_from_numkp("v<<A^>>A<A>A<AAv>A^Av<AAA^>A")) == 68    
                    
def numkp_from_numkp(input_str):
    kp_positions = {"^": (0,1),"A": (0,2),
                    "<": (1,0),"v": (1,1),">": (1,2),
                 }
    moves = []
    moves.append("A"+input_str[0])

    for i in range(0, len(input_str)-1):
        moves.append(input_str[i]+input_str[i+1])
    output_str = ''
    for move in moves:
        left = kp_positions[move[0]]
        right = kp_positions[move[1]]
        movediff = tuple(b - a for a, b in zip(left, right))
        updown = movediff[0]
        leftright = movediff[1]
        output_str += move_string(leftright,updown)
    return output_str

def test_complexity():
    testcodes = load_codes(read_file_lines('day21-test.txt'))
    assert complexity(testcodes) == 126384
    
def complexity(codes):
    complexity = 0
    for code in codes:
        print('code',code)
        l1 = dirkp_from_numkp(code)
        print('l1',l1)
        l2 = numkp_from_numkp(l1)
        print('l2',l2)  
        l3 = numkp_from_numkp(l2)
        print('l3',l3)
        print(len(l3),int(code[:3]))
        complexity += len(l3) * int(code[:3])
    return complexity