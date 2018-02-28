from display import *
from matrix import *
from draw import *

class ParseState(object):
    def __init__(self, line_index, points, transform, screen, color):
        self.line_index = line_index
        self.points = points
        self.transform = transform
        self.screen = screen
        self.color = color

"""
Goes through the file named filename and performs all of the actions listed in that file.
The file follows the following format:
     Every command is a single character that takes up a line
     Any command that requires arguments must have those arguments in the second line.
     The commands are as follows:
         line: add a line to the edge matrix - 
	    takes 6 arguemnts (x0, y0, z0, x1, y1, z1)
	 ident: set the transform matrix to the identity matrix - 
	 scale: create a scale matrix, 
	    then multiply the transform matrix by the scale matrix - 
	    takes 3 arguments (sx, sy, sz)
	 move: create a translation matrix, 
	    then multiply the transform matrix by the translation matrix - 
	    takes 3 arguments (tx, ty, tz)
	 rotate: create a rotation matrix,
	    then multiply the transform matrix by the rotation matrix -
	    takes 2 arguments (axis, theta) axis should be x, y or z
	 apply: apply the current transformation matrix to the 
	    edge matrix
	 display: draw the lines of the edge matrix to the screen
	    display the screen
	 save: draw the lines of the edge matrix to the screen
	    save the screen to a file -
	    takes 1 argument (file name)
	 quit: end parsing

See the file script for an example of the file format
"""
def parse_file( fname, points, transform, screen, color ):
    with open(fname, 'r') as file:
        lines = file.readlines()

        iterator = range(len(lines))
        state = ParseState(index=0, points=points, transform=transform, screen=screen, color=color)
        while state.index < len(lines):
            process_batch(lines, state)

def process_batch(lines, state):
    CMDS = ('line', 'ident', 'scale', 'move', 'rotate', 'apply', 'display', 'save')

    index = state.index
    line = lines[index].strip()
    if line not in CMDS:
        raise ValueError("%s is an invalid command" % line)

    state.index += 1
    line = lines[state.index].strip()
    
    if line == 'line':
        process_line(line, state)
    elif line == 'ident':
        process_ident(line, points, transform, screen, color)
    elif line == 'scale':
        process_scale(line, points, transform, screen, color)
    elif line == 'move':
        process_move(line, points, transform, screen, color)
    elif line == 'rotate':
        process_rotate(line, points, transform, screen, color)
    elif line == 'apply':
        process_apply(line, points, transform, screen, color)
    elif line == 'display':
        process_display(line, points, transform, screen, color)
    elif line == 'save':
        process_save(line, points, transform, screen, color)

    state.index += 1

def process_line(line, points, transform, screen, color):
    x0, y0, z0, x1, y1, z1 = [int(coord) for coord in line.strip().split(' ')]
    add_edge(points, x0, y0, z0, x1, y1, z1)

