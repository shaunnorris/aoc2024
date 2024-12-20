from aoclib import read_file_lines
import math
import multiprocessing
import time



def test_load_program():
    assert load_program(read_file_lines("day17-test.txt")) == {
        "code": ["0", "1", "5", "4", "3", "0"],
        "A": 729,
        "B": 0,
        "C": 0,
    }


def load_program(lines):
    program = {"code": [], "A": 0, "B": 0, "C": 0}

    for line in lines:
        if "Register A: " in line:
            program["A"] = int(line.split(":")[1].strip())
        elif "Register B: " in line:
            program["B"] = int(line.split(":")[1].strip())
        elif "Register C: " in line:
            program["C"] = int(line.split(":")[1].strip())
        elif "Program:" in line:
            program["code"] = line.split(":")[1].strip().split(",")
    print(program)
    return program

def test_run_program():
    testprogram = load_program(read_file_lines("day17-test.txt"))
    assert run_program(testprogram) ==  "4,6,3,5,6,3,5,2,1,0"
    
def run_program(program):
    
    A = program["A"]
    B = program["B"]
    C = program["C"]
    code = program["code"]
    in_pointer = 0
    output = []
        
    def combo_operand(n):
        if n == 0:
            return 0
        elif n == 1:
            return 1
        elif n == 2:
            return 2
        elif n == 3:
            return 3
        elif n == 4:
            return A
        elif n == 5:
            return B
        elif n == 6:
            return C
        elif n == 7:
            return False
    
    while in_pointer < len(code)-1:
        opcode = int(code[in_pointer])
        operand = int(code[in_pointer + 1])
        jump = False
        
        if opcode == 0: # adv
            A = int(math.trunc(A // (2 ** combo_operand(operand))))
            
        elif opcode == 1: # bxl
            B =  B ^ operand
        elif opcode == 2: # bst
            B = combo_operand(operand) % 8
        elif opcode == 3: # jnz
            if A != 0:
                op_index = operand
                if 0 <= op_index < len(code):
                    in_pointer = operand
                    jump = True
                else:
                    print("jump out of range - halt")
                    break
        elif opcode == 4: # bxc
            B = B ^ C
        elif opcode == 5: # out
            output.append(combo_operand(operand) % 8)
        elif opcode == 6: # bdv
            B = int(math.trunc(A / (2 ** combo_operand(operand))))
        elif opcode == 7: # cdv
            C = int(math.trunc(A / (2 ** combo_operand(operand))))
        
        if not jump:
            in_pointer += 2
        else:
            jump = False
            
    return  ",".join(map(str, output))



def test_find_copyval():
    testprogram = load_program(read_file_lines("day17-test2.txt"))
    assert find_copyval(testprogram) == 117440

def find_copyval(program,n):
    orig_code = ','.join(map(str,program["code"]))
    check = run_program({"code": program["code"], "A": n, "B":program["B"], "C":program["C"]})
    print('dbg',n,check,orig_code)
    if check == orig_code:
        return n
    else:
        return None

part1 = run_program(load_program(read_file_lines("day17-input.txt")))
print('part1:',part1)

