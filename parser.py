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
        process_scale(line, state)
    elif line == 'move':
        process_move(line, state)
    elif line == 'rotate':
        process_rotate(line, state)
    elif line == 'apply':
        process_apply(line, state)
    elif line == 'display':
        process_display(line, state)
    elif line == 'save':
        process_save(line, state)

def process_line(line, state):
    x0, y0, z0, x1, y1, z1 = [int(coord) for coord in line.strip().split(' ')]
    add_edge(state.points, x0, y0, z0, x1, y1, z1)
    state.index += 1

def process_ident(line, state):
    ident(state.transform)

def process_scale(line, state):
    x, y, z = [int(scl) for scl in line.strip().split(' ')]
    sclmat = new_matrix(rows=4, cols=4)
    ident(sclmat)
    sclmat[0][0] = x
    sclmat[1][1] = y
    sclmat[2][2] = z
    matrix_mult(sclmat, state.transform)
    state.index += 1

def process_move(line, state):
    tx, ty, tz = [int(t) for t in line.strip().split(' ')]
    tmat = new_matrix(rows=4, cols=4)
    ident(tmat)
    tmat[3][0] = tx
    tmat[3][1] = ty
    tmat[3][2] = tz
    matrix_mult(tmat, state.transform)
    state.index += 1

def process_rotate(line, state):
    axis, theta = line.strip().split(' ')
    theta = int(theta)

    rotmat = new_matrix(rows=4, cols=4)
    ident(rotmat)
    if axis == 'x':
        rotmat[1][1] = cos_deg(theta)
        rotmat[2][1] = -sin_deg(theta)
        rotmat[1][2] = sin_deg(theta)
        rotmat[2][2] = cos_deg(theta)
    elif axis == 'y':
        rotmat[0][0] = cos_deg(theta)
        rotmat[2][0] = -sin_deg(theta)
        rotmat[0][2] = sin_deg(theta)
        rotmat[2][2] = cos_deg(theta)
    elif axis == 'z':
        rotmat[0][0] = cos_deg(theta)
        rotmat[1][0] = -sin_deg(theta)
        rotmat[0][1] = sin_deg(theta)
        rotmat[1][1] = cos_deg(theta)

    matrix_mult(rotmat, state.transform)
    state.index += 1

def process_apply(line, state):
    matrix_mult(state.transform, state.points)

def process_display(line, state):
    scn = new_screen()
    draw_lines(state.points, scn, color=[255, 0, 0])
    display(scn)

def process_save(line, state):
    scn = new_screen()
    draw_lines(state.points, scn, color=[255, 0, 0])
    save_extension(scn, "output.png")
