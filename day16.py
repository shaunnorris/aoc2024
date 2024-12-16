from aoclib import read_file_lines,get_mapsize,in_bounds,tuple_add

def test_load_map():
    test1 = read_file_lines('day16-test1.txt')
    assert load_map(test1) == {}


def load_map(maplines):
            
    mapdata = {'S':'','E':'','.':[],'#':[],'size':''}
    
    for i in range(len(maplines)):
        for j in range(len(maplines[0])):
            if maplines[i][j] == 'S':
                mapdata['S'] = (i,j)
            elif maplines[i][j] == 'E':
                mapdata['E'] = (i,j) 
            elif maplines[i][j] == '.':
                mapdata['.'].append((i,j))
            elif maplines[i][j] == '#':
                mapdata['#'].append((i,j))
    mapdata['size'] = (len(maplines),len(maplines[0]))
    print(mapdata)
    return(mapdata)

def test_best_path():
    test1 = read_file_lines('day16-test1.txt')
    assert best_path(load_map(test1)) == 7036
    
def best_path(mapdata):
    movemap = {'>':(0,1 ),'<':(0,-1),'^':(-1,0),'v':(1,0)}
    optionmap = {'>':('^','v'),'v':('<','>'),'<':('v','^'),'^':('<','>')}
    leftmap = {'>':'^','<':'v','^':'<','v':'>'}
    rightmap = {'>':'v','<':'^','^':'>','v':'<'}
    dir = '>'
    pos = mapdata['S']
    open_paths = [(pos,dir)]
    best_score = 10000000
    full_paths = []   
    while len(open_paths) > 0:
        current_path = open_paths.pop()
        pos = current_path[-1][0]
        dir = current_path[-1][1]
        forward = tuple_add(pos,movemap[dir])
        leftturn = tuple_add(pos,movemap[optionmap[dir][0]])
        rightturn = tuple_add(pos,movemap[optionmap[dir][1]])
        if forward in mapdata['.']:
            pathcopy = current_path[:]
            open_paths.append(pathcopy.append(forward,dir))
        if leftturn in mapdata['.']:
            pathcopy = current_path[:]
            newdir = leftmap[dir]
            open_paths.append(pathcopy.append(leftturn,newdir))
        if rightturn in mapdata['.']:
            pathcopy = current_path[:]
            newdir = rightmap[dir]
            open_paths.append(pathcopy.append(rightturn,newdir))
        for move in [leftturn,rightturn,forward]:     
            if move in mapdata['E']:
                score = len(current_path[0])
                if score < best_score:
                    best_score = score
                full_paths.append(current_path)