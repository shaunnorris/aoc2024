from aoclib import read_file_lines, in_bounds, tuple_add,get_mapsize

def test_find_regions():
    lines = read_file_lines('day12-test.txt')
    assert find_regions(lines) == [
        (12, 18),
        (4, 8),
        (14, 28),
        (10, 18),
        (13, 20),
        (11, 20),
        (1, 4),
        (13, 18),
        (14, 22),
        (5, 12),
        (3, 8),
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
        
        while stack:
            cx, cy = stack.pop()
            area += 1
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
        return area, perimeter
    
    regions = []
    for r in range(r+1):
        for c in range(c+1):
            if not visited[r][c]:
                area, perimeter = flood_fill(r,c)
                regions.append((area,perimeter))
    print(regions)
    return regions


def test_price_regions():
    test_regions = [(12, 18), (4, 8), (14, 28), (10, 18), (13, 20), (11, 20), (1, 4), (13, 18), (14, 22), (5, 12), (3, 8)]    
    assert price_regions(test_regions) == 1930
    
def price_regions(regions):
    price = 0
    for region in regions:
        price += region[0] * region[1]
    return price

grid = read_file_lines('day12-input.txt')
regions = find_regions(grid)
part1 = price_regions(regions)
print('part1:',part1)