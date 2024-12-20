from aoclib import read_file_lines, tuple_add
import networkx as nx

def test_load_map():
    testdata = read_file_lines('day18-test.txt')
    assert load_map(testdata,7,12) == {'.': [(0, 0), (0, 1), (0, 2), (0, 3), (0, 4), (0, 5), (1, 0), (1, 1), (1, 2), (1, 3), (1, 4), (1, 6), (2, 0), (2, 2), (2, 3), (2, 5), (3, 1), (3, 2), (3, 4), (3, 5), (3, 6), (4, 0), (4, 1), (4, 3), (4, 4), (4, 6), (5, 0), (5, 2), (5, 3), (5, 5), (5, 6), (6, 0), (6, 1), (6, 2), (6, 4), (6, 5), (6, 6)], '#': [(5, 4), (4, 2), (4, 5), (3, 0), (2, 1), (6, 3), (2, 4), (1, 5), (0, 6), (3, 3), (2, 6), (5, 1)], 'size': (7, 7)} 

def load_map(lines,size,bytes):
    mapdata = {'.':[],'#':[]}
    for line in lines[:bytes]:
        x,y = line.split(',')
        mapdata['#'].append((int(x),int(y)))
    
    for i in range(size):
        for j in range(size):
            if (i,j) not in mapdata['#']:
                mapdata['.'].append((i,j))
    mapdata['size'] = (size,size)
    return mapdata

def test_find_shortest_path():
    testdata = read_file_lines('day18-test.txt')
    mapdata = load_map(testdata,7,12)
    assert find_shortest_path(mapdata) == 22



def find_shortest_path(mapdata):
    obstacles = mapdata['#']
    G = nx.grid_2d_graph(mapdata['size'][0],mapdata['size'][1])
    G.remove_nodes_from(obstacles)
    start = (0,0)
    end = (mapdata['size'][0]-1,mapdata['size'][1]-1)
    path = nx.astar_path(G,start,end,heuristic=lambda u, v: abs(u[0]-v[0]) + abs(u[1]-v[1]))
    return len(path)-1    

def test_find_first_block():
    bytedata = read_file_lines('day18-test.txt')
    assert find_first_block(bytedata,7) == (6,1)
    
def find_first_block(bytedata,size):
    obstacles = []
    for byte in bytedata:
        x,y = byte.split(',')
        obstacles.append((int(x),int(y)))
    
    G = nx.grid_2d_graph(size,size)

    for obstacle in obstacles:
        G.remove_node(obstacle)
        start = (0,0)
        end = (size-1,size-1)
        if not nx.has_path(G, start, end):
            return obstacle   

    return None 

    
mazebytes = read_file_lines("day18-input.txt")    
mapdata = load_map(mazebytes,71,1024)
part1 = find_shortest_path(mapdata)
print('part1:',part1)
part2 = find_first_block(mazebytes,71)
print('part2:', part2)