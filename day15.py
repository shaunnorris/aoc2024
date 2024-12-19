from aoclib import read_file_lines,get_mapsize,in_bounds,tuple_add

def test_load_map():
    test1 = read_file_lines('day15-test1.txt')
    #assert load_map(test1) == 


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
    testmap = load_map_pt2(read_file_lines('day15-test2.txt'))
    assert testmap['@'] == (4,8)


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
    mapdata = {'@':'','[':[],']':[],'.':[],'#':[],'size':'','moves':[]}
    for i in range(len(maplines)):
        for j in range(len(maplines[0])):
            if maplines[i][j] == '@':
                mapdata['@'] = (i,j)
            elif maplines[i][j] == '.':
                mapdata['.'].append((i,j))
            elif maplines[i][j] == '#':
                mapdata['#'].append((i,j))
            elif maplines[i][j] == '[':
                mapdata['['].append((i,j))
            elif maplines[i][j] == ']':
                mapdata[']'].append((i,j))
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
            elif (r,c) in mapdata['[']:
                print('[',end='')
            elif (r,c) in mapdata[']']:
                print(']',end='')
            elif (r,c) in mapdata['.']:
                print('.',end='')
        print('',end='\n')


def test_process_moves_pt2():
    testmap = load_map_pt2(read_file_lines('day15-test2.txt'))
    assert process_moves_pt2(testmap)['@'] == (7,4)


def process_moves_pt2(mapdata): 
    moves = mapdata['moves']
    moves.reverse()
    movemap = {'>':(0,1 ),'<':(0,-1),'^':(-1,0),'v':(1,0),'UL':(-1,-1),'UR':(-1,1),'DL':(1,-1),'DR':(1,1)}
    
    def integrity_check(mapdata):
        integrity = 0
        integrity += len(mapdata['.'])
        integrity += len(mapdata['#'])
        integrity += len(mapdata['['])
        integrity += len(mapdata[']'])
        return(integrity)
        
    while len(moves) > 0:
        prev_integrity = integrity_check(mapdata)
        move = moves.pop()
        start_pos = mapdata['@']
        target_pos = tuple_add(start_pos,movemap[move])
        if target_pos in mapdata['#']:
           continue # don't move the robot into a wall
        elif target_pos in mapdata['.']:
            mapdata['.'].remove(target_pos) # remove old empty space that robot will occupy
            if start_pos not in mapdata['.']:
                mapdata['.'].append(start_pos) # add new empty space where robt was
            mapdata['@'] = target_pos
        elif move in ['>']:
            if target_pos in mapdata['[']:
                free_spot = False
                lboxes_found = []
                rboxes_found = []
                for i in range(target_pos[1],mapdata['size'][1]):
                    if (target_pos[0],i) in mapdata['#']:
                        break
                    elif (target_pos[0],i) in mapdata['[']:
                        lboxes_found.append((target_pos[0],i))
                    elif (target_pos[0],i) in mapdata[']']:
                        rboxes_found.append((target_pos[0],i))
                    elif (target_pos[0],i) in mapdata['.']:
                        free_spot = (target_pos[0],i)
                        break
                if free_spot:
                    mapdata['.'].remove(free_spot)
                    if start_pos not in mapdata['.']:
                        mapdata['.'].append(start_pos)
                    mapdata['@'] = target_pos
                    for box in lboxes_found:
                        mapdata['['].remove(box)
                        mapdata['['].append(tuple_add(box,movemap[move]))
                    for box in rboxes_found:
                        mapdata[']'].remove(box)
                        mapdata[']'].append(tuple_add(box,movemap[move]))
                    
        elif move in ['<']:
            if target_pos in mapdata[']']:
                free_spot = False
                lboxes_found = []
                rboxes_found = []
                for i in range(target_pos[1],0,-1):
                    if (target_pos[0],i) in mapdata['#']:
                        break
                    elif (target_pos[0],i) in mapdata[']']:
                        rboxes_found.append((target_pos[0],i))
                    elif (target_pos[0],i) in mapdata['[']:
                        lboxes_found.append((target_pos[0],i))
                    elif (target_pos[0],i) in mapdata['.']:
                        free_spot = (target_pos[0],i)
                        break
                if free_spot:
                    mapdata['.'].remove(free_spot)
                    if start_pos not in mapdata['.']:
                        mapdata['.'].append(start_pos)
                    mapdata['@'] = target_pos
                    for box in lboxes_found:
                        mapdata['['].remove(box)
                        mapdata['['].append(tuple_add(box,movemap[move]))
                    for box in rboxes_found:
                        mapdata[']'].remove(box)
                        mapdata[']'].append(tuple_add(box,movemap[move]))
                    
        elif move in ['v','^']:
            lboxes_to_push = []
            rboxes_to_push = []
            checklist = [target_pos]
            good_to_move = True
            checked = []
            while len(checklist) > 0 and good_to_move:
                current_check = checklist.pop()
                checked.append(current_check)
                if current_check in mapdata['#']:
                    good_to_move = False
                    break
                elif current_check in mapdata['[']:
                    if current_check not in lboxes_to_push:
                        lboxes_to_push.append(current_check)
                    one_over = tuple_add(current_check,movemap['>'])
                    if one_over not in rboxes_to_push:
                        rboxes_to_push.append(one_over)
                    if tuple_add(current_check,movemap[move]) not in checked:
                        checklist.append(tuple_add(current_check,movemap[move]))
                    if one_over not in checked: 
                        checklist.append(tuple_add(one_over,movemap[move]))
                elif current_check in mapdata[']']:
                    if current_check not in rboxes_to_push:
                        rboxes_to_push.append(current_check)
                    one_over = tuple_add(current_check,movemap['<'])
                    if one_over not in lboxes_to_push:
                        lboxes_to_push.append(one_over)
                    if tuple_add(current_check,movemap[move]) not in checked:
                        checklist.append(tuple_add(current_check,movemap[move]))
                    if one_over not in checked: 
                        checklist.append(tuple_add(one_over,movemap[move]))
            if good_to_move:
                before_points = lboxes_to_push + rboxes_to_push
                after_points = []
                for lbox in lboxes_to_push:
                    new_pos = tuple_add(lbox,movemap[move])
                    after_points.append(new_pos)
                    mapdata['['].remove(lbox)
                    mapdata['['].append(new_pos)
                for rbox in rboxes_to_push:
                    new_pos = tuple_add(rbox,movemap[move])
                    after_points.append(new_pos)
                    mapdata[']'].remove(rbox)
                    mapdata[']'].append(new_pos)
                for point in set(before_points):
                    if point not in after_points:
                        if point not in mapdata[']'] and point not in mapdata['[']:
                            mapdata['.'].append(point)
                for point in set(after_points):
                    if point in mapdata['.']:
                        mapdata['.'].remove(point)
                if start_pos not in mapdata['.']: 
                    mapdata['.'].append(start_pos)
                mapdata['@'] = target_pos
                if target_pos in mapdata['.']:
                    mapdata['.'].remove(target_pos)
                        
        else:
            continue # if no free space continue to the next move
        if integrity_check(mapdata) != prev_integrity:
            print('integrity:',move, integrity_check(mapdata))
            for key in mapdata.keys():
                print(key,len(mapdata[key]))
    return mapdata 

def test_gps_score_pt2():
    testmap = load_map_pt2(read_file_lines('day15-test2.txt'))
    assert gps_score_pt2(process_moves_pt2(testmap)) == 9021
    
def gps_score_pt2(mapdata):
    score = 0
    for box in mapdata['[']:
        score += box[0] * 100 + box[1]
    return score
    
mapdata = load_map(read_file_lines('day15-input.txt'))
mapdata2 = load_map_pt2(read_file_lines('day15-input.txt'))
part1 = gps_score(process_moves(mapdata))
print('part1:',part1)
part2 = gps_score_pt2(process_moves_pt2(mapdata2))
print('part2:',part2)
