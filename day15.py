from aoclib import read_file_lines,get_mapsize,in_bounds,tuple_add

def test_load_map():
    test1 = read_file_lines('day15-test1.txt')
    assert load_map(test1) == {
        "@": (2, 2),
        "O": [(1, 3), (1, 5), (2, 4), (3, 4), (4, 4), (5, 4)],
        ".": [
            (1, 1),
            (1, 2),
            (1, 4),
            (1, 6),
            (2, 3),
            (2, 5),
            (2, 6),
            (3, 1),
            (3, 2),
            (3, 3),
            (3, 5),
            (3, 6),
            (4, 1),
            (4, 3),
            (4, 5),
            (4, 6),
            (5, 1),
            (5, 2),
            (5, 3),
            (5, 5),
            (5, 6),
            (6, 1),
            (6, 2),
            (6, 3),
            (6, 4),
            (6, 5),
            (6, 6),
        ],
        "#": [
            (0, 0),
            (0, 1),
            (0, 2),
            (0, 3),
            (0, 4),
            (0, 5),
            (0, 6),
            (0, 7),
            (1, 0),
            (1, 7),
            (2, 0),
            (2, 1),
            (2, 7),
            (3, 0),
            (3, 7),
            (4, 0),
            (4, 2),
            (4, 7),
            (5, 0),
            (5, 7),
            (6, 0),
            (6, 7),
            (7, 0),
            (7, 1),
            (7, 2),
            (7, 3),
            (7, 4),
            (7, 5),
            (7, 6),
            (7, 7),
        ],
        "size": (8, 8),
        "moves": [
            "<",
            "^",
            "^",
            ">",
            ">",
            ">",
            "v",
            "v",
            "<",
            "v",
            ">",
            ">",
            "v",
            "<",
            "<",
        ],
    }


def load_map(lines):
    maplines = []
    movelines = []
    mappart = True
    for line in lines:
        if line == '':
            mappart = False
        elif mappart:
            maplines.append(line)
        else:
            movelines.append(line)
            
    mapdata = {'@':'','O':[],'.':[],'#':[],'size':'','moves':[]}
    for i in range(len(maplines)):
        for j in range(len(maplines[0])):
            if maplines[i][j] == '@':
                mapdata['@'] = (i,j)
            elif maplines[i][j] == '.':
                mapdata['.'].append((i,j))
            elif maplines[i][j] == '#':
                mapdata['#'].append((i,j))
            elif maplines[i][j] == 'O':
                mapdata['O'].append((i,j))
    mapdata['size'] = (len(maplines),len(maplines[0]))
    for moveline in movelines:
        for move in moveline:
            mapdata['moves'].append(move)
    return(mapdata)

def test_process_moves():
    testmap1 = load_map(read_file_lines('day15-test1.txt'))
    assert process_moves(testmap1) == {'@': (4, 4), 'O': [(1, 5), (5, 4), (1, 6), (6, 4), (3, 6), (4, 3)], '.': [(1, 1), (2, 5), (2, 6), (3, 1), (3, 2), (4, 1), (4, 6), (5, 1), (5, 2), (5, 3), (5, 5), (5, 6), (6, 1), (6, 2), (6, 3), (6, 5), (6, 6), (2, 2), (1, 2), (1, 3), (1, 4), (2, 4), (2, 3), (3, 3), (3, 4), (3, 5), (4, 5)], '#': [(0, 0), (0, 1), (0, 2), (0, 3), (0, 4), (0, 5), (0, 6), (0, 7), (1, 0), (1, 7), (2, 0), (2, 1), (2, 7), (3, 0), (3, 7), (4, 0), (4, 2), (4, 7), (5, 0), (5, 7), (6, 0), (6, 7), (7, 0), (7, 1), (7, 2), (7, 3), (7, 4), (7, 5), (7, 6), (7, 7)], 'size': (8, 8), 'moves': []}
    
def process_moves(mapdata):
    print('initial map:')
    print_map(mapdata)
 
    moves = mapdata['moves']
    moves.reverse()
    movemap = {'>':(0,1 ),'<':(0,-1),'^':(-1,0),'v':(1,0)}
    
    while len(moves) > 0:
        move = moves.pop()
        
        start_pos = mapdata['@']
        target_pos = tuple_add(start_pos,movemap[move])
        if target_pos in mapdata['#']:
           continue # don't move the robot into a wall
        elif target_pos in mapdata['.']:
            mapdata['.'].remove(target_pos) # remove old empty space that robot will occupy
            mapdata['.'].append(start_pos) # add new empty space where robt was
            mapdata['@'] = target_pos
        elif target_pos in mapdata['O']:
            free_pos = False
            try_pos = target_pos
            while in_bounds(try_pos,mapdata['size']) and free_pos == False:   
                nextpos = tuple_add(try_pos,movemap[move])
                if nextpos in mapdata['#']:
                    break
                elif nextpos in mapdata['.']:
                    free_pos = nextpos
                else:
                    try_pos = nextpos
            if free_pos:
                mapdata['.'].remove(free_pos) # swap empty space with a box
                mapdata['O'].remove(target_pos) # remove old box position
                mapdata['O'].append(free_pos) # add new box position
                mapdata['.'].append(start_pos) # add new empty space where robt was
                mapdata['@'] = target_pos
            else:
                continue # if no free space continue to the next move
    return mapdata

def print_map(mapdata):
    for r in range(mapdata['size'][0]):
        for c in range(mapdata['size'][1]):
            if (r,c) == mapdata['@']:
                print('@',end='')
            elif (r,c) in mapdata['#']:
                print('#',end='')
            elif (r,c) in mapdata['.']:
                print('.',end='')
            elif (r,c) in mapdata['O']:
                print('O',end='')
        print('',end='\n')
        

def test_gps_score():
    testmap1 = load_map(read_file_lines('day15-test1.txt'))
    results1 = process_moves(testmap1) 
    gpstest1 = gps_score(results1)
    gpstest2 = gps_score(process_moves(load_map(read_file_lines('day15-test2.txt'))))
    assert gpstest1 == 2028
    assert gpstest2 == 10092
    
def gps_score(mapdata):
    score = 0
    for box in mapdata['O']:
        score += box[0] * 100 + box[1]
    return score

def test_load_map_pt2():
    test1 = read_file_lines('day15-test2.txt')
    assert load_map_pt2(test1) == {
        "@": (4, 8),
        "[]": [
            (1, 6),
            (1, 12),
            (1, 16),
            (2, 14),
            (3, 4),
            (3, 6),
            (3, 12),
            (3, 16),
            (4, 6),
            (4, 14),
            (5, 2),
            (5, 10),
            (6, 2),
            (6, 8),
            (6, 14),
            (7, 4),
            (7, 6),
            (7, 10),
            (7, 14),
            (7, 16),
            (8, 10),
        ],
        ".": [
            (1, 2),
            (1, 3),
            (1, 4),
            (1, 5),
            (1, 8),
            (1, 9),
            (1, 10),
            (1, 11),
            (1, 14),
            (1, 15),
            (2, 2),
            (2, 3),
            (2, 4),
            (2, 5),
            (2, 6),
            (2, 7),
            (2, 8),
            (2, 9),
            (2, 10),
            (2, 11),
            (2, 12),
            (2, 13),
            (2, 16),
            (2, 17),
            (3, 2),
            (3, 3),
            (3, 8),
            (3, 9),
            (3, 10),
            (3, 11),
            (3, 14),
            (3, 15),
            (4, 2),
            (4, 3),
            (4, 4),
            (4, 5),
            (4, 9),
            (4, 10),
            (4, 11),
            (4, 12),
            (4, 13),
            (4, 16),
            (4, 17),
            (5, 6),
            (5, 7),
            (5, 8),
            (5, 9),
            (5, 12),
            (5, 13),
            (5, 14),
            (5, 15),
            (5, 16),
            (5, 17),
            (6, 4),
            (6, 5),
            (6, 6),
            (6, 7),
            (6, 10),
            (6, 11),
            (6, 12),
            (6, 13),
            (6, 16),
            (6, 17),
            (7, 2),
            (7, 3),
            (7, 8),
            (7, 9),
            (7, 12),
            (7, 13),
            (8, 2),
            (8, 3),
            (8, 4),
            (8, 5),
            (8, 6),
            (8, 7),
            (8, 8),
            (8, 9),
            (8, 12),
            (8, 13),
            (8, 14),
            (8, 15),
            (8, 16),
            (8, 17),
        ],
        "#": [
            (0, 0),
            (0, 1),
            (0, 2),
            (0, 3),
            (0, 4),
            (0, 5),
            (0, 6),
            (0, 7),
            (0, 8),
            (0, 9),
            (0, 10),
            (0, 11),
            (0, 12),
            (0, 13),
            (0, 14),
            (0, 15),
            (0, 16),
            (0, 17),
            (0, 18),
            (0, 19),
            (1, 0),
            (1, 1),
            (1, 18),
            (1, 19),
            (2, 0),
            (2, 1),
            (2, 18),
            (2, 19),
            (3, 0),
            (3, 1),
            (3, 18),
            (3, 19),
            (4, 0),
            (4, 1),
            (4, 18),
            (4, 19),
            (5, 0),
            (5, 1),
            (5, 4),
            (5, 5),
            (5, 18),
            (5, 19),
            (6, 0),
            (6, 1),
            (6, 18),
            (6, 19),
            (7, 0),
            (7, 1),
            (7, 18),
            (7, 19),
            (8, 0),
            (8, 1),
            (8, 18),
            (8, 19),
            (9, 0),
            (9, 1),
            (9, 2),
            (9, 3),
            (9, 4),
            (9, 5),
            (9, 6),
            (9, 7),
            (9, 8),
            (9, 9),
            (9, 10),
            (9, 11),
            (9, 12),
            (9, 13),
            (9, 14),
            (9, 15),
            (9, 16),
            (9, 17),
            (9, 18),
            (9, 19),
        ],
        "size": (10, 20),
        "moves": [
            "<",
            "v",
            "v",
            ">",
            "^",
            "<",
            "v",
            "^",
            ">",
            "v",
            ">",
            "^",
            "v",
            "v",
            "^",
            "v",
            ">",
            "v",
            "<",
            ">",
            "v",
            "^",
            "v",
            "<",
            "v",
            "<",
            "^",
            "v",
            "v",
            "<",
            "<",
            "<",
            "^",
            ">",
            "<",
            "<",
            ">",
            "<",
            ">",
            ">",
            "v",
            "<",
            "v",
            "v",
            "v",
            "<",
            ">",
            "^",
            "v",
            "^",
            ">",
            "^",
            "<",
            "<",
            "<",
            ">",
            "<",
            "<",
            "v",
            "<",
            "<",
            "<",
            "v",
            "^",
            "v",
            "v",
            "^",
            "v",
            ">",
            "^",
            "v",
            "v",
            "v",
            "<",
            "<",
            "^",
            ">",
            "^",
            "v",
            "^",
            "^",
            ">",
            "<",
            "<",
            ">",
            ">",
            ">",
            "<",
            ">",
            "^",
            "<",
            "<",
            ">",
            "<",
            "^",
            "v",
            "v",
            "^",
            "^",
            "<",
            ">",
            "v",
            "v",
            "v",
            "<",
            ">",
            ">",
            "<",
            "^",
            "^",
            "v",
            ">",
            "^",
            ">",
            "v",
            "v",
            "<",
            ">",
            "v",
            "<",
            "<",
            "<",
            "<",
            "v",
            "<",
            "^",
            "v",
            ">",
            "^",
            "<",
            "^",
            "^",
            ">",
            ">",
            ">",
            "^",
            "<",
            "v",
            "<",
            "v",
            ">",
            "<",
            ">",
            "v",
            "v",
            ">",
            "v",
            "^",
            "v",
            "^",
            "<",
            ">",
            ">",
            "<",
            ">",
            ">",
            ">",
            ">",
            "<",
            "^",
            "^",
            ">",
            "v",
            "v",
            ">",
            "v",
            "<",
            "^",
            "^",
            "^",
            ">",
            ">",
            "v",
            "^",
            "v",
            "^",
            "<",
            "^",
            "^",
            ">",
            "v",
            "^",
            "^",
            ">",
            "v",
            "^",
            "<",
            "^",
            "v",
            ">",
            "v",
            "<",
            ">",
            ">",
            "v",
            "^",
            "v",
            "^",
            "<",
            "v",
            ">",
            "v",
            "^",
            "^",
            "<",
            "^",
            "^",
            "v",
            "v",
            "<",
            "<",
            "<",
            "v",
            "<",
            "^",
            ">",
            ">",
            "^",
            "^",
            "^",
            "^",
            ">",
            ">",
            ">",
            "v",
            "^",
            "<",
            ">",
            "v",
            "v",
            "v",
            "^",
            ">",
            "<",
            "v",
            "<",
            "<",
            "<",
            ">",
            "^",
            "^",
            "^",
            "v",
            "v",
            "^",
            "<",
            "v",
            "v",
            "v",
            ">",
            "^",
            ">",
            "v",
            "<",
            "^",
            "^",
            "^",
            "^",
            "v",
            "<",
            ">",
            "^",
            ">",
            "v",
            "v",
            "v",
            "v",
            ">",
            "<",
            ">",
            ">",
            "v",
            "^",
            "<",
            "<",
            "^",
            "^",
            "^",
            "^",
            "^",
            "^",
            ">",
            "<",
            "^",
            ">",
            "<",
            ">",
            ">",
            ">",
            "<",
            ">",
            "^",
            "^",
            "<",
            "<",
            "^",
            "^",
            "v",
            ">",
            ">",
            ">",
            "<",
            "^",
            "<",
            "v",
            ">",
            "^",
            "<",
            "v",
            "v",
            ">",
            ">",
            "v",
            ">",
            ">",
            ">",
            "^",
            "v",
            ">",
            "<",
            ">",
            "^",
            "v",
            ">",
            "<",
            "<",
            "<",
            "<",
            "v",
            ">",
            ">",
            "v",
            "<",
            "v",
            "<",
            "v",
            ">",
            "v",
            "v",
            "v",
            ">",
            "^",
            "<",
            ">",
            "<",
            "<",
            ">",
            "^",
            ">",
            "<",
            "^",
            ">",
            ">",
            "<",
            ">",
            "^",
            "v",
            "<",
            ">",
            "<",
            "^",
            "v",
            "v",
            "v",
            "<",
            "^",
            "^",
            "<",
            ">",
            "<",
            "v",
            "<",
            "<",
            "<",
            "<",
            "<",
            ">",
            "<",
            "^",
            "v",
            "<",
            "<",
            "<",
            ">",
            "<",
            "<",
            "<",
            "^",
            "^",
            "<",
            "v",
            "<",
            "^",
            "^",
            "^",
            ">",
            "<",
            "^",
            ">",
            ">",
            "^",
            "<",
            "v",
            "^",
            ">",
            "<",
            "<",
            "<",
            "^",
            ">",
            ">",
            "^",
            "v",
            "<",
            "v",
            "^",
            "v",
            "<",
            "v",
            "^",
            ">",
            "^",
            ">",
            ">",
            "^",
            "v",
            ">",
            "v",
            "v",
            ">",
            "^",
            "<",
            "<",
            "^",
            "v",
            "<",
            ">",
            ">",
            "<",
            "<",
            ">",
            "<",
            "<",
            "v",
            "<",
            "<",
            "v",
            ">",
            "<",
            ">",
            "v",
            "<",
            "^",
            "v",
            "v",
            "<",
            "<",
            "<",
            ">",
            "^",
            "^",
            "v",
            "^",
            ">",
            "^",
            "^",
            ">",
            ">",
            ">",
            "<",
            "<",
            "^",
            "v",
            ">",
            ">",
            "v",
            "^",
            "v",
            ">",
            "<",
            "^",
            "^",
            ">",
            ">",
            "^",
            "<",
            ">",
            "v",
            "v",
            "^",
            "<",
            ">",
            "<",
            "^",
            "^",
            ">",
            "^",
            "^",
            "^",
            "<",
            ">",
            "<",
            "v",
            "v",
            "v",
            "v",
            "v",
            "^",
            "v",
            "<",
            "v",
            "<",
            "<",
            ">",
            "^",
            "v",
            "<",
            "v",
            ">",
            "v",
            "<",
            "<",
            "^",
            ">",
            "<",
            "<",
            ">",
            "<",
            "<",
            ">",
            "<",
            "<",
            "<",
            "^",
            "^",
            "<",
            "<",
            "<",
            "^",
            "<",
            "<",
            ">",
            ">",
            "<",
            "<",
            ">",
            "<",
            "^",
            "^",
            "^",
            ">",
            "^",
            "^",
            "<",
            ">",
            "^",
            ">",
            "v",
            "<",
            ">",
            "^",
            "^",
            ">",
            "v",
            "v",
            "<",
            "^",
            "v",
            "^",
            "v",
            "<",
            "v",
            "v",
            ">",
            "^",
            "<",
            ">",
            "<",
            "v",
            "<",
            "^",
            "v",
            ">",
            "^",
            "^",
            "^",
            ">",
            ">",
            ">",
            "^",
            "^",
            "v",
            "v",
            "v",
            "^",
            ">",
            "v",
            "v",
            "v",
            "<",
            ">",
            ">",
            ">",
            "^",
            "<",
            "^",
            ">",
            ">",
            ">",
            ">",
            ">",
            "^",
            "<",
            "<",
            "^",
            "v",
            ">",
            "^",
            "v",
            "v",
            "v",
            "<",
            ">",
            "^",
            "<",
            ">",
            "<",
            "<",
            "v",
            ">",
            "v",
            "^",
            "^",
            ">",
            ">",
            ">",
            "<",
            "<",
            "^",
            "^",
            "<",
            ">",
            ">",
            "^",
            "v",
            "^",
            "<",
            "v",
            "^",
            "v",
            "v",
            "<",
            ">",
            "v",
            "^",
            "<",
            "<",
            ">",
            "^",
            "<",
            "^",
            "v",
            "^",
            "v",
            ">",
            "<",
            "^",
            "<",
            "<",
            "<",
            ">",
            "<",
            "<",
            "^",
            "<",
            "v",
            ">",
            "<",
            "v",
            "<",
            ">",
            "v",
            "v",
            ">",
            ">",
            "v",
            ">",
            "<",
            "v",
            "^",
            "<",
            "v",
            "v",
            "<",
            ">",
            "v",
            "^",
            "<",
            "<",
            "^",
        ],
    }


def load_map_pt2(lines):
    maplines = []
    movelines = []
    mappart = True
    for line in lines:
        if line == '':
            mappart = False
        elif mappart:
            maplines.append(line)
        else:
            movelines.append(line)
    
    expanded_maplines = []
    for mapline in maplines:
        expline = ''
        for char in mapline:
            if char == '@':
                expline += '@.'
            elif char == '#':
                expline += '##'
            elif char == '.':
                expline += '..'
            elif char == 'O':
                expline += '[]'
        expanded_maplines.append(expline)
        print (expline)   
    maplines = expanded_maplines[:]
    mapdata = {'@':'','[]':[],'.':[],'#':[],'size':'','moves':[]}
    for i in range(len(maplines)):
        for j in range(len(maplines[0])):
            if maplines[i][j] == '@':
                mapdata['@'] = (i,j)
            elif maplines[i][j] == '.':
                mapdata['.'].append((i,j))
            elif maplines[i][j] == '#':
                mapdata['#'].append((i,j))
            elif maplines[i][j] == '[':
                mapdata['[]'].append((i,j))
    mapdata['size'] = (len(maplines),len(maplines[0]))
    for moveline in movelines:
        for move in moveline:
            mapdata['moves'].append(move)
    print_map_pt2(mapdata)
    print(mapdata)
    return(mapdata)

def print_map_pt2(mapdata):
    for r in range(mapdata['size'][0]):
        for c in range(mapdata['size'][1]):
            if (r,c) == mapdata['@']:
                print('@',end='')
            elif (r,c) in mapdata['#']:
                print('#',end='')
            elif (r,c) in mapdata['.']:
                print('.',end='')
            elif (r,c) in mapdata['[]']:
                print('[]',end='')
        print('',end='\n')


def test_process_moves_pt2():
    testmap1 = load_map_pt2(read_file_lines('day15-test4.txt'))
    assert process_moves_pt2(testmap1) == {}

def process_moves_pt2(mapdata):
    print('initial map:')
    print_map_pt2(mapdata)
 
    moves = mapdata['moves']
    moves.reverse()
    movemap = {'>':(0,1 ),'<':(0,-1),'^':(-1,0),'v':(1,0),'UL':(-1,-1),'UR':(-1,1),'DL':(1,-1),'DR':(1,1)}
    
    while len(moves) > 0:
        move = moves.pop()
        start_pos = mapdata['@']
        target_pos = tuple_add(start_pos,movemap[move])
        if target_pos in mapdata['#']:
           continue # don't move the robot into a wall
        elif target_pos in mapdata['.']:
            mapdata['.'].remove(target_pos) # remove old empty space that robot will occupy
            mapdata['.'].append(start_pos) # add new empty space where robt was
            mapdata['@'] = target_pos
        elif move in ['>']:
            if target_pos in mapdata['[]']:
                free_spot = False
                boxes_found = []
                for i in range(target_pos[1],mapdata['size'][1]):
                    if (target_pos[0],i) in mapdata['#']:
                        break
                    elif (target_pos[0],i) in mapdata['[]']:
                        boxes_found.append((target_pos[0],i))
                    elif (target_pos[0],i) in mapdata['.']:
                        free_spot = (target_pos[0],i)
                        break
                if free_spot:
                    mapdata['.'].remove(free_spot)
                    mapdata['.'].append(start_pos)
                    mapdata['@'] = target_pos
                    for box in boxes_found:
                        mapdata['[]'].remove(box)
                        mapdata['[]'].append(tuple_add(box,movemap[move]))
        elif move in ['<']:
            one_left = tuple_add(target_pos,movemap[move])
            if one_left in mapdata['[]']:
                free_spot = False
                boxes_found = []
                for i in range(target_pos[1],0,-1):
                    if (target_pos[0],i) in mapdata['#']:
                        break
                    elif (target_pos[0],i) in mapdata['[]']:
                        boxes_found.append((target_pos[0],i))
                    elif (target_pos[0],i) in mapdata['.']:
                        free_spot = (target_pos[0],i)
                        break
                if free_spot:
                    mapdata['.'].remove(free_spot)
                    mapdata['.'].append(start_pos)
                    mapdata['@'] = target_pos
                    for box in boxes_found:
                        mapdata['[]'].remove(box)
                        mapdata['[]'].append(tuple_add(box,movemap[move]))
        elif move in ['v']:
            one_left = tuple_add(target_pos,movemap['<'])
            one_right = tuple_add(target_pos,movemap['>'])
            boxes_to_push = []
            checklist = [target_pos,one_left]
            while len(checklist) > 0:
                current_check = checklist.pop()
                if current_check in mapdata['[]']:
                    if current_check not in boxes_to_push:
                        boxes_to_push.append(current_check)
                    checklist.append(tuple_add(current_check,movemap['v']))
                    checklist.append(tuple_add(current_check,movemap['DL']))
                    checklist.append(tuple_add(current_check,movemap['DR']))                    
            print('boxes to push:',boxes_to_push)   
        else:
            continue # if no free space continue to the next move
        print('move:',move)
        print_map_pt2(mapdata)
    return mapdata 
        
#mapdata = load_map(read_file_lines('day15-input.txt'))
#part1 = gps_score(process_moves(mapdata))
#print('part1:',part1)