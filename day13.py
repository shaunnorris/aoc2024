from aoclib import read_file_lines
from sympy import symbols, Eq, solve
import math

def test_read_machine_data():
    testdata = read_file_lines('day13-test.txt')
    assert len(read_machine_data(testdata)) == 4


def read_machine_data(data):
    machines = []
    machine = {} 
    for line in data:
        if 'Button A' in line:
            a1,b1 = line.split(':')[1].split(',')
            machine['a1'] = int(a1.split('+')[1])
            machine['b1'] = int(b1.split('+')[1])
        elif 'Button B' in line:
            a2,b2 = line.split(':')[1].split(',')
            machine['a2'] = int(a2.split('+')[1])
            machine['b2'] = int(b2.split('+')[1])
        elif 'Prize' in line:
            t1,t2 = line.split(':')[1].split(',')
            machine['a3'] = int(t1.split('=')[1])
            machine['b3'] = int(t2.split('=')[1])
        elif line == '':
            machines.append(machine)
            machine = {}
    machines.append(machine)
    return machines

def test_solve_machine():
    testdata = read_file_lines('day13-test.txt')
    test_machines = read_machine_data(testdata)
    assert solve_machine(test_machines[0]) == (80,40)
    assert solve_machine(test_machines[1]) == False
    assert solve_machine(test_machines[2]) == (38, 86)
    assert solve_machine(test_machines[3]) == False

def solve_machine(machine):
    A, B = symbols('A B')
    eq1 = Eq(machine['a1'] * A + machine['a2'] * B, machine['a3'])
    eq2 = Eq(machine['b1'] * A + machine['b2'] * B, machine['b3'])
    solution = solve((eq1, eq2), (A, B))
    solA, solB = solution[A], solution[B]
    if solA % 1 == 0 and solB % 1 == 0:
        return int(solA), int(solB)
    else:
        return False
    
def test_count_tokens():
    testdata = read_file_lines('day13-test.txt')
    test_machines = read_machine_data(testdata)
    assert count_tokens(test_machines) == 480
    
def count_tokens(machines):
    tokens = 0
    for machine in machines:
        solution = solve_machine(machine)
        if solution:
            A, B = solution
            if A <= 100 and B <= 100:
                tokens += A * 3 + B
    return tokens



def count_tokens_part2(machines):
    tokens = 0
    for machine in machines:
        machine['a3'] += 10000000000000
        machine['b3'] += 10000000000000
        solution = solve_machine(machine)
        if solution:
            A, B = solution
            tokens += A * 3 + B
    return tokens

machines = read_machine_data(read_file_lines('day13-input.txt'))
part1 = count_tokens(machines)
print('part1:',part1)
part2 = count_tokens_part2(machines)
print('part2:',part2)