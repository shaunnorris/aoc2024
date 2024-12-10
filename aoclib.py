import os

def read_file_lines(filepath):
    if os.path.exists(filepath):
        with open(filepath, 'r') as file:
            lines = file.readlines()
        return [line.strip() for line in lines]
    else:
        print("no input file found")
        return False

def test_read_file_lines(tmp_path):
    # Create a temporary file and write some content to it
    test_file = tmp_path / "test_file.txt"
    with open(test_file, 'w') as f:
        f.write("Line 1\nLine 2\nLine 3")

    # Use the function to read the file's content
    result = read_file_lines(test_file)
    assert result == ["Line 1", "Line 2", "Line 3"]
    badresult = read_file_lines('should_not_exist.txt')
    assert badresult == False
    
def transpose(strings):
    zipped = zip(*strings)
    transposed = [''.join(group) for group in zipped]
    return transposed

def get_mapsize(grid):
    return (len(grid)-1, len(grid[0])-1)

def in_bounds(coord,mapsize):
    return coord[0] >= 0 and coord[0] <= mapsize[0] and coord[1] >= 0 and coord[1] <= mapsize[1]

def tuple_add(t1,t2):
    return tuple(a + b for a, b in zip(t1, t2))