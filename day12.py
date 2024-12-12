from aoclib import read_file_lines, in_bounds, tuple_add,get_mapsize

def test_find_regions():
    lines = read_file_lines('day12-test.txt')
    assert find_regions(lines) == [
        {
            "letter": "R",
            "area": 12,
            "perimeter": 18,
            "coordinates": [
                (0, 1),
                (2, 4),
                (1, 2),
                (0, 0),
                (1, 1),
                (0, 3),
                (2, 3),
                (0, 2),
                (2, 2),
                (1, 0),
                (3, 2),
                (1, 3),
            ],
        },
        {
            "letter": "I",
            "area": 4,
            "perimeter": 8,
            "coordinates": [(0, 5), (0, 4), (1, 4), (1, 5)],
        },
        {
            "letter": "C",
            "area": 14,
            "perimeter": 28,
            "coordinates": [
                (4, 4),
                (0, 7),
                (5, 5),
                (3, 4),
                (6, 5),
                (5, 4),
                (1, 8),
                (0, 6),
                (1, 7),
                (3, 3),
                (2, 6),
                (1, 6),
                (2, 5),
                (3, 5),
            ],
        },
        {
            "letter": "F",
            "area": 10,
            "perimeter": 18,
            "coordinates": [
                (3, 8),
                (2, 7),
                (3, 7),
                (0, 9),
                (2, 9),
                (3, 9),
                (4, 8),
                (0, 8),
                (1, 9),
                (2, 8),
            ]},
        {
            "letter": "V",
            "area": 13,
            "perimeter": 20,
            "coordinates": [
                (4, 0),
                (2, 1),
                (4, 3),
                (3, 1),
                (6, 1),
                (2, 0),
                (5, 1),
                (4, 2),
                (3, 0),
                (5, 0),
                (6, 0),
                (5, 3),
                (4, 1),
            ],
        },
        {
            "letter": "J",
            "area": 11,
            "perimeter": 20,
            "coordinates": 
               [ (7, 7),
                (9, 6),
                (4, 6),
                (5, 7),
                (6, 7),
                (4, 5),
                (7, 6),
                (5, 6),
                (8, 6),
                (3, 6),
                (6, 6),]
            ,
        },
        {"letter": "C", "area": 1, "perimeter": 4, "coordinates": [(4, 7)]},
        {
            "letter": "E",
            "area": 13,
            "perimeter": 18,
            "coordinates": 
                [(8, 8),
                (9, 7),
                (9, 9),
                (4, 9),
                (8, 7),
                (6, 8),
                (5, 8),
                (7, 9),
                (8, 9),
                (9, 8),
                (5, 9),
                (6, 9),
                (7, 8),
            ],
        },
        {
            "letter": "I",
            "area": 14,
            "perimeter": 22,
            "coordinates": 
               [ (7, 4),
                (6, 2),
                (7, 1),
                (9, 3),
                (8, 1),
                (6, 4),
                (7, 3),
                (8, 3),
                (7, 2),
                (8, 2),
                (7, 5),
                (6, 3),
                (8, 5),
                (5, 2),]
            ,
        },
        {
            "letter": "M",
            "area": 5,
            "perimeter": 12,
            "coordinates": [(9, 0), (7, 0), (9, 2), (8, 0), (9, 1)],
        },
        {
            "letter": "S",
            "area": 3,
            "perimeter": 8,
            "coordinates": [(9, 5), (8, 4), (9, 4)],
        },
    ]


def find_regions(grid):
    mapsize = get_mapsize(grid)
    r, c = mapsize
    visited = [[False for _ in range(c+1)] for _ in range(r+1)]
    directions = [[0,1], [0,-1], [1,0], [-1,0]]
    
    def flood_fill(x,y):
        stack = [(x,y)]
        visited[x][y] = True
        letter = grid[x][y]
        area = 0
        perimeter = 0
        coordinates = set()
        
        while stack:
            cx, cy = stack.pop()
            area += 1
            coordinates.add((cx, cy))
            for dx, dy in directions:
                nx, ny = tuple_add((cx,cy), (dx,dy))
                if in_bounds((nx,ny), mapsize):
                    if not visited[nx][ny] and grid[nx][ny] == letter:
                        stack.append((nx,ny))
                        visited[nx][ny] = True
                    elif grid[nx][ny] != letter:
                        perimeter += 1
                else:
                    perimeter += 1
        return {
            'letter': letter,
            'area': area,
            'perimeter': perimeter,
            'coordinates': list(coordinates)
        }
    
    regions = []
    for r in range(r+1):
        for c in range(c+1):
            if not visited[r][c]:
                region = flood_fill(r,c)
                regions.append(region)
    return regions


def test_price_regions():
    test_regions = [
        {
            "letter": "R",
            "area": 12,
            "perimeter": 18,
            "coordinates": {
                (0, 1),
                (2, 4),
                (1, 2),
                (0, 0),
                (1, 1),
                (0, 3),
                (2, 3),
                (0, 2),
                (2, 2),
                (1, 0),
                (3, 2),
                (1, 3),
            },
        },
        {
            "letter": "I",
            "area": 4,
            "perimeter": 8,
            "coordinates": {(0, 5), (0, 4), (1, 4), (1, 5)},
        },
        {
            "letter": "C",
            "area": 14,
            "perimeter": 28,
            "coordinates": {
                (4, 4),
                (0, 7),
                (5, 5),
                (3, 4),
                (6, 5),
                (5, 4),
                (1, 8),
                (0, 6),
                (1, 7),
                (3, 3),
                (2, 6),
                (1, 6),
                (2, 5),
                (3, 5),
            },
        },
        {
            "letter": "F",
            "area": 10,
            "perimeter": 18,
            "coordinates": {
                (3, 8),
                (2, 7),
                (3, 7),
                (0, 9),
                (2, 9),
                (3, 9),
                (4, 8),
                (0, 8),
                (1, 9),
                (2, 8),
            },
        },
        {
            "letter": "V",
            "area": 13,
            "perimeter": 20,
            "coordinates": {
                (4, 0),
                (2, 1),
                (4, 3),
                (3, 1),
                (6, 1),
                (2, 0),
                (5, 1),
                (4, 2),
                (3, 0),
                (5, 0),
                (6, 0),
                (5, 3),
                (4, 1),
            },
        },
        {
            "letter": "J",
            "area": 11,
            "perimeter": 20,
            "coordinates": {
                (7, 7),
                (9, 6),
                (4, 6),
                (5, 7),
                (6, 7),
                (4, 5),
                (7, 6),
                (5, 6),
                (8, 6),
                (3, 6),
                (6, 6),
            },
        },
        {"letter": "C", "area": 1, "perimeter": 4, "coordinates": {(4, 7)}},
        {
            "letter": "E",
            "area": 13,
            "perimeter": 18,
            "coordinates": {
                (8, 8),
                (9, 7),
                (9, 9),
                (4, 9),
                (8, 7),
                (6, 8),
                (5, 8),
                (7, 9),
                (8, 9),
                (9, 8),
                (5, 9),
                (6, 9),
                (7, 8),
            },
        },
        {
            "letter": "I",
            "area": 14,
            "perimeter": 22,
            "coordinates": {
                (7, 4),
                (6, 2),
                (7, 1),
                (9, 3),
                (8, 1),
                (6, 4),
                (7, 3),
                (8, 3),
                (7, 2),
                (8, 2),
                (7, 5),
                (6, 3),
                (8, 5),
                (5, 2),
            },
        },
        {
            "letter": "M",
            "area": 5,
            "perimeter": 12,
            "coordinates": {(9, 0), (7, 0), (9, 2), (8, 0), (9, 1)},
        },
        {
            "letter": "S",
            "area": 3,
            "perimeter": 8,
            "coordinates": {(9, 5), (8, 4), (9, 4)},
        },
    ]
    assert price_regions(test_regions) == 1930
    
def price_regions(regions):
    price = 0
    for region in regions:
        price += region['area'] * region['perimeter']
    return price

def test_count_sides():
    testgrid = read_file_lines('day12-test.txt')

    tr = find_regions(testgrid)
    
    assert count_sides(tr[0]['coordinates']) == 10
    assert count_sides(tr[1]['coordinates']) == 4
    assert count_sides(tr[2]['coordinates']) == 22
    assert count_sides(tr[3]['coordinates']) == 12
    assert count_sides(tr[4]['coordinates']) == 10

       
def count_sides(coordinates):
          
    
    def count_neighbours(coord):
        # return count of how adjacent squares are NOT in the same region
        neighbour_pos = {'U':(-1, 0), 'D':(1, 0), 'L':(0, -1), 'R':(0, 1)}
        count = 0
        open_sides = []
        for dir in neighbour_pos:
            pos = neighbour_pos[dir]
            neighbour = tuple_add(coord, pos)
            if neighbour not in coordinates:
                open_sides.append(dir)
                count +=1
        return {'open':count,'dir':open_sides}
    
    sides = {}
    for coord in coordinates:
        open_neighbours = count_neighbours(coord)
        open_dir = open_neighbours['dir']
        for dir in open_dir:
            if dir in ['U','D']:
                if (dir,coord[0]) in sides.keys():
                    sides[(dir,coord[0])].append(coord[1])
                else:
                    sides[(dir,coord[0])] = [coord[1]]    
            elif dir in ['L','R']:
                if (dir,coord[1]) in sides.keys():
                    sides[(dir,coord[1])].append(coord[0])
                else:
                    sides[(dir,coord[1])] = [coord[0]]
    
    segment_count = 0 
    for list in sides.values():
        list.sort()
        def count_consecutive_segments(numbers):
            if numbers is None:
                return 0
            return sum(1 for i in range(1, len(numbers)) if numbers[i] - numbers[i-1] > 1) + 1
        segment_count += count_consecutive_segments(list)
        
    return segment_count

def test_count_all_sides():
    testgrid = read_file_lines('day12-test.txt')
    tr = find_regions(testgrid)
    assert price_with_sides(tr) == 1206

def price_with_sides(regions):
    price = 0
    for region in regions:
        sides = count_sides(region['coordinates'])
        price += sides * region['area']
    return price

grid = read_file_lines('day12-input.txt')
regions = find_regions(grid)
part1 = price_regions(regions)
print('part1:',part1)
part2 = price_with_sides(regions)
print('part2:',part2)