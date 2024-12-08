from aoclib import read_file_lines
from itertools import combinations

def test_get_mapsize():
    assert get_mapsize(read_file_lines('day8-test.txt')) == (11,11)

def get_mapsize(grid):
    return (len(grid)-1, len(grid[0])-1)

def test_get_antennas():
    testgrid = read_file_lines('day8-test.txt')
    assert get_antennas(testgrid) == {
        "0": [(1, 8), (2, 5), (3, 7), (4, 4)],
        "A": [(5, 6), (8, 8), (9, 9)],
    }
   
def get_antennas(grid):
    ants = {}
    for row in range(len(grid)):
        for col in range(len(grid[0])):
            coord = (row,col)
            value = grid[row][col]
            if value != '.':
                if value in ants.keys():
                    ants[value].append(coord)
                else:
                    ants[value] = [coord]
    return ants

def test_get_all_pairs():
    assert get_all_pairs([(1, 8), (2, 5), (3, 7), (4, 4)]) == [
        ((1, 8), (2, 5)),
        ((1, 8), (3, 7)),
        ((1, 8), (4, 4)),
        ((2, 5), (3, 7)),
        ((2, 5), (4, 4)),
        ((3, 7), (4, 4)),
    ]
    assert get_all_pairs( [(5, 6), (8, 8), (9, 9)]) == [((5,6),(8,8)), ((5,6),(9,9)), ((8,8),(9,9))]

def get_all_pairs(pointlist):
    return list(combinations(pointlist, 2))

def test_tuple_diff():
    assert tuple_diff((1,2),(3,4)) == (-2,-2)
    assert tuple_diff((3,4),(1,2)) == (2,2)
    
def tuple_diff(t1, t2):
    return tuple(a - b for a, b in zip(t1, t2))

def test_tuple_add():
    assert tuple_add((1,2),(3,4)) == (4,6)
def tuple_add(t1,t2):
    return tuple(a + b for a, b in zip(t1, t2))


def test_in_bounds():
    testmapsize = get_mapsize(read_file_lines('day8-test.txt'))
    assert in_bounds((1,2),testmapsize) == True
    assert in_bounds((-1,2),testmapsize) == False
    assert in_bounds((1,-2),testmapsize) == False
    assert in_bounds((12,2),testmapsize) == False
    assert in_bounds((1,12),testmapsize) == False
    
def in_bounds(coord,mapsize):
    return coord[0] >= 0 and coord[0] <= mapsize[0] and coord[1] >= 0 and coord[1] <= mapsize[1]
    
def test_count_nodes():
    testgrid = read_file_lines('day8-test.txt')
    ants = get_antennas(testgrid)
    testmapsize = get_mapsize(testgrid)
    assert count_nodes(ants,testmapsize) == 14
    
def count_nodes(ants,mapsize):
    nodes = []
    for ant in ants.values():
        pairs = get_all_pairs(ant)
        for pair in pairs:
            rightdiff = tuple_diff(pair[0], pair[1])
            leftdiff = tuple_diff(pair[1], pair[0])
            rightnode = tuple_add(pair[1], leftdiff)
            leftnode = tuple_add(pair[0], rightdiff)
            for node in [leftnode, rightnode]:
                if in_bounds(node, mapsize):
                    if node not in nodes:
                        nodes.append(node)
    return len(nodes)



def test_get_points_on_line():
    testmapsize = get_mapsize(read_file_lines('day8-test.txt'))
    assert get_points_on_line(((0,0),(1,3)),testmapsize) == [(0,0),(1,3),(2,6),(3,9)]
    assert get_points_on_line(((3, 3), (4, 4)), (9, 9)) == [
        (3, 3),
        (4, 4),
        (2, 2),
        (1, 1),
        (0, 0),
        (5, 5),
        (6, 6),
        (7, 7),
        (8, 8),
        (9, 9),
    ]
    assert get_points_on_line(((2,5),(3,7)),testmapsize) == [(2,5),(3,7),(1,3),(0,1),(4,9),(5,11)]
def get_points_on_line(pair, mapsize):
    points = []
    points.append(pair[0])
    points.append(pair[1])
    rightdiff = tuple_diff(pair[0], pair[1])  
    leftdiff = tuple_diff(pair[1], pair[0])
    
    nextleft = tuple_add(pair[0], rightdiff)
    while in_bounds(nextleft, mapsize):
        points.append(nextleft)
        nextleft = tuple_add(nextleft, rightdiff)
    
    nextright = tuple_add(pair[1], leftdiff)
    while in_bounds(nextright,mapsize):
        points.append(nextright)
        nextright = tuple_add(nextright, leftdiff)
    return points


def test_count_harmonic_nodes():
    testgrid = read_file_lines('day8-test.txt')
    ants = get_antennas(testgrid)
    testmapsize = get_mapsize(testgrid)
    assert count_harmonic_nodes(ants,testmapsize) == 34
    
def count_harmonic_nodes(ants,mapsize):
    nodes = []
    for ant in ants.values():
        pairs = get_all_pairs(ant)
        for pair in pairs:
            points = get_points_on_line(pair, mapsize)
            for point in points:
                if point not in nodes:
                    nodes.append(point)
    return len(nodes)

grid = read_file_lines('day8-input.txt')
ants = get_antennas(grid)
mapsize = get_mapsize(grid)
part1 = count_nodes(ants,mapsize)
print('part1:',part1)
part2 = count_harmonic_nodes(ants,mapsize)
print('part2:',part2)