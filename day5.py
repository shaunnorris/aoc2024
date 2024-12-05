from aoclib import read_file_lines

def test_parse_data():
    testdata = read_file_lines('day5-test.txt')
    parseddata = parse_data(testdata)
    assert len(parseddata['rules']) == 21
    assert len(parseddata['prints']) == 6
    
def parse_data(data):
    rules = []
    prints = []
    firstsection = True
    for line in data:    
        if line != '':
            if firstsection:
                rules.append([int(x) for x in line.split('|')])
            else:
                prints.append([int(x) for x in line.split(',')])
        else:
            firstsection = False
    return {'rules': rules, 'prints': prints}

def test_fix_rank():
    testdata = read_file_lines('day5-test.txt')
    parseddata = parse_data(testdata)
    testrules = parseddata['rules']
    brokenprint = parseddata['prints'][5]
    assert fix_rank(testrules,brokenprint) == 47
    
def fix_rank(rules,printjob):
    neworder = []
    while printjob:
        for element in printjob:
            toprank = True       
            for rule in rules:
                leftside, rightside = rule[0],rule[1]
                if leftside in printjob and rightside in printjob:
                    if element == rightside:
                        toprank = False
            if toprank:
                neworder.append(element)
                printjob.remove(element)
    return neworder[len(neworder) //2]

def test_apply_rules():
    testdata = read_file_lines('day5-test.txt')
    parseddata = parse_data(testdata)
    assert apply_rules(parseddata) == (143,123)

    
def apply_rules(dataset):
    rules = dataset['rules']
    prints = dataset['prints']
    finalset = []
    brokenset = []
    for printjob in prints:
        validprint = True
        for rule in rules:
            leftside, rightside = rule[0],rule[1]
            if leftside in printjob and rightside in printjob:
                if printjob.index(leftside) > printjob.index(rightside):
                    validprint = False
        if validprint:
            finalset.append(printjob[len(printjob) //2])
        else:
            brokenset.append(fix_rank(rules,printjob))
    return sum(finalset),sum(brokenset)

dataset = parse_data(read_file_lines('day5-input.txt'))
part1,part2 = apply_rules(dataset)
print('part1:',part1)
print('part2:',part2)   

