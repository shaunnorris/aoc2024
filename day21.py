from aoclib import read_file_lines
import networkx as nx

def test_load_codes():
    testcodes = read_file_lines('day21-test.txt')
    assert len(testcodes) == 5
    assert testcodes == ['029A', '980A','179A','456A', '379A']

def load_codes(lines):
    codes = []
    for line in lines: 
        codes.append(line.strip())
    return codes

numpad = {"7": (0,0),"8": (0,1),"9": (0,2),
                    "4": (1,0),"5": (1,1),"6": (1,2),
                    "1": (2,0),"2": (2,1),"3": (2,2),
                    "0": (3,1),"A": (3,2)}

arrowpad = {"^": (0,1),"A": (0,2),
                    "<": (1,0),"v": (1,1),">": (1,2)}

def test_build_pad_lookup():
    assert len(build_pad_lookup(numpad).keys()) == 121
    assert len(build_pad_lookup(arrowpad).keys()) == 25
    
def build_pad_lookup(node_positions):
    
    G = nx.Graph()   
    move_chars = {(1,0): "v", (0,1): ">", (-1,0): "^", (0,-1): "<"}
    
    for node, position in node_positions.items():
        G.add_node(node, pos=position)

    # Add edges between nodes that are adjacent
    for node1, position1 in node_positions.items():
        for node2, position2 in node_positions.items():
            if abs(position1[0] - position2[0]) + abs(position1[1] - position2[1]) == 1:
                G.add_edge(node1, node2)

    lookup_table = {}
    
    for start in G.nodes():
        for end in G.nodes():
            if start == end:
                lookup_table[(start,end)] = ''
            else:
                start_position = start
                end_position = end
                path = nx.shortest_path(G, source=start_position, target=end_position)
                pathpoints = []
                for stop in path:
                    pathpoints.append(node_positions[stop])
                moves = []
                for i in range(len(pathpoints)-1): #for each point in pathpoints:
                    diff = tuple(b - a for a, b in zip(pathpoints[i], pathpoints[i+1]))                
                    moves.append(move_chars[diff])
                lookup_table[(start,end)] = ''.join(moves)

    return(lookup_table)



def test_translate():
    assert translate('numpad','029A') in ['<A^A>^^AvvvA', '<A^A^>^AvvvA', '<A^A^^>AvvvA']
    assert translate('arrowpad', "<A^A^^>AvvvA") == ''
    #assert translate('numpad','379A') == "^A^^<<A>>AvvvA"
    #assert translate('numpad','179A') == '^<<A^^A>>AvvvA'
    #assert translate('numpad','456A') == '^^<<A>A>AvvA' 
    #assert translate('numpad','379A') == '^A^^<<A>>AvvvA'
     
def translate(type,code):
    if type == 'numpad':
        lookup_pad = build_pad_lookup(numpad)
    elif type == 'arrowpad':
        lookup_pad = build_pad_lookup(arrowpad)
        
    code = "A" + code
    move_str = []
    for i in range(len(code)-1):
        thismove = (code[i],code[i+1])
        nextstr = lookup_pad[thismove] + 'A'
        move_str.append(nextstr)
        print('next move',(code[i],code[i+1]),'generates',nextstr)
       
           
    return ''.join(move_str)



def test_complexity():
    testcodes = load_codes(read_file_lines('day21-test.txt'))
    #assert complexity(testcodes) == 126384
    
def complexity(codes):
    complexity = 0
    for code in codes:
        print('code',code)
        l1 = translate('numpad',code)
        print('L1:',l1)
        l2 = translate('arrowpad',l1)
        print('L2:',l2,len(l2))  
        l3 = translate('arrowpad',l2)
        print('L3:',l3, len(l3))
        complexity += len(l3) * int(code[:3])
        print('code',code,'complexity',complexity,'from',len(l3),'*', int(code[:3]))
    return complexity

