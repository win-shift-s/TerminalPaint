from pathlib import Path
from termpaint_lib import *
import curses.ascii

def move_cursor(w, canvas_dim, key, now_coord):
    """Move the cursor one position in a certain direction

    This function receives an ASCII value of a key pressed
    from the keyboard. It dictates where the cursor will be
    moved from `now_coord`. The resulting coordinate will be
    clipped to one less than the the canvas dimensions.

    :param w: the `Window` object
    :type w: `class Window`
    :param canvas_dim: canvas dimensions as a 2-ary tuple `(row, column)`
    :type canvas_dim: tuple
    :param key: the key pressed
    :type key: int
    :param now_coord: current coordinate as a 2-ary tuple `(row, column)`
    :type now_coord: tuple
    :return: resulting coordinate as a 2-ary tuple `(row, column)`
    """

    x_value = now_coord[1]
    y_value = now_coord[0]

    if key == curses.KEY_DOWN:
        if y_value == canvas_dim[0] - 1:
            pass
        else:
            y_value += 1
    elif key == curses.KEY_UP:
        if y_value == 0:
            pass
        else:
            y_value -= 1
    elif key == curses.KEY_LEFT:
        if x_value == 0:
            pass
        else:
            x_value -= 1
    elif key == curses.KEY_RIGHT:
        if x_value == canvas_dim[1] - 1:
            pass
        else:
            x_value += 1
    return w.move(y_value, x_value)

def color_input(color_return):
    if color_return == 'color input tuple':
        return (ord('r'), ord('g'), ord('b'), ord('c'), ord('m'), ord('y'), ord('w'), ord('x'))

    elif color_return == 'ordInput-idx dict':
        return {ord('r'): 3,
                ord('g'): 4,
                ord('b'): 5,
                ord('c'): 6,
                ord('m'): 7,
                ord('y'): 8,
                ord('w'): 9,
                ord('x'): 10}

    elif color_return == 'rawInput-idx dict':
        return {'r': 3,
                'g': 4,
                'b': 5,
                'c': 6,
                'm': 7,
                'y': 8,
                'w': 9,
                'x': 10}
    
    elif color_return == 'idx-rawInput dict':
        return {3: 'r',
                4: 'g',
                5: 'b',
                6: 'c',
                7: 'm',
                8: 'y',
                9: 'w',
                10: 'x',
                196608: 'r',
                262144: 'g',
                327680: 'b',
                393216: 'c',
                458752: 'm',
                524288: 'y',
                589824: 'w',
                655360: 'x'}

def pencil_canvas(w, canvas_dim, coord, color_pair_idx):
    """Color a single coordinate in the canvas

    This function accepts a `color_pair_idx` corresponding
    to the index of the color pair initialized from `init_color_pairs()`.

    :param w: the `Window` object
    :type w: `class Window`
    :param canvas_dim: canvas dimensions as a 2-ary tuple `(row, column)`
    :type canvas_dim: tuple
    :param coord: coordinate to color as a 2-ary tuple `(row, column)`
    :type coord: tuple
    :param color_pair_idx: index of the color-pair `coord` should be set to
    :type color_pair_idx: int
    """

    return color_cell_at(w, get_cursor_pos(), color_input('ordInput-idx dict')[color_pair_idx])

def valid_coord(canvas_dim, visited, coord):
    if coord[0] < 0 or coord[1] < 0 or coord[0] >= canvas_dim[0] or coord[1] >= canvas_dim[1] or coord in visited:
        return False
    return True

def fill_canvas(w, canvas_dim, start_coord, color_pair_idx):
    """Flood-fill a color starting at a coordinate in the canvas

    Given a `start_coord`, this function will try to fill this cell, its
    adjacent cells (north, east, west, south), the adjacent cells' adjacent
    cells, etc. with a similar color pair as itself to a new color pair until
    the color pair of the whole group of cells have been changed.

    :param w: the `Window` object
    :type w: `class Window`
    :param canvas_dim: canvas dimensions as a 2-ary tuple `(row, column)`
    :type canvas_dim: tuple
    :param start_coord: starting coordinate to color as a 2-ary tuple `(row, column)`
    :type start_coord: tuple
    :param color_pair_idx: index of the color-pair `start_coord` and its adjacent cells should be set to
    :type color_pair_idx: int
    """
    # HINT: Read on breadth-first search (BFS) on a grid.
    #       Make sure to keep track of the original color while doing the coloring.

    queue = []
    visited = []

    queue.append(start_coord)
    visited.append(start_coord)
    initial_color = get_color_pair_idx_at(w, start_coord)
    final_color = color_input('ordInput-idx dict')[color_pair_idx]
    color_cell_at(w, start_coord, final_color)

    while queue:
        current_coord = queue.pop(0)
        current_y_coord = current_coord[0]
        current_x_coord = current_coord[1]
        
        if valid_coord(canvas_dim, visited, (current_y_coord + 1, current_x_coord)) == True:
            coord_color = get_color_pair_idx_at(w, (current_y_coord + 1, current_x_coord))
            if coord_color == initial_color:
                color_cell_at(w, (current_y_coord + 1, current_x_coord), final_color)
                queue.append((current_y_coord + 1, current_x_coord))
                visited.append((current_y_coord + 1, current_x_coord))
        
        if valid_coord(canvas_dim, visited, (current_y_coord - 1, current_x_coord)) == True:
            coord_color = get_color_pair_idx_at(w, (current_y_coord - 1, current_x_coord))
            if coord_color == initial_color:
                color_cell_at(w, (current_y_coord - 1, current_x_coord), final_color)
                queue.append((current_y_coord - 1, current_x_coord))
                visited.append((current_y_coord - 1, current_x_coord))
        
        if valid_coord(canvas_dim, visited, (current_y_coord, current_x_coord + 1)) == True:
            coord_color = get_color_pair_idx_at(w, (current_y_coord, current_x_coord + 1))
            if coord_color == initial_color:
                color_cell_at(w, (current_y_coord, current_x_coord + 1), final_color)
                queue.append((current_y_coord, current_x_coord + 1))
                visited.append((current_y_coord, current_x_coord + 1))
        
        if valid_coord(canvas_dim, visited, (current_y_coord, current_x_coord - 1)) == True:
            coord_color = get_color_pair_idx_at(w, (current_y_coord, current_x_coord - 1))
            if coord_color == initial_color:
                color_cell_at(w, (current_y_coord, current_x_coord - 1), final_color)
                queue.append((current_y_coord, current_x_coord - 1))
                visited.append((current_y_coord, current_x_coord - 1))
        
    w.move(start_coord[0], start_coord[1])
    w.refresh()

def clear_canvas(w, term_dim, canvas_dim):
    """Clear canvas

    This function fills the whole of the canvas with color pair 0.
    After that, it will print a prompt.

    :param w: the `Window` object
    :type w: `class Window`
    :param canvas_dim: canvas dimensions as a 2-ary tuple `(row, column)`
    :type canvas_dim: tuple
    :param term_dim: terminal dimensions as a 2-ary tuple `(row, column)`
    :type term_dim: tuple
    """
    yn = None
    while yn != True:
        yn = show_yn_prompt(w, term_dim, (8, 40), msg= 'Clear the canvas?')
        if yn == False:
            break

    if yn == True:
        for y_value in range(canvas_dim[0]):
            color_cell_at(w, (y_value, 0), 10, True)
        print_status_bar(w, term_dim, msg='Canvas cleared!')
        w.move(0, 0)
        w.refresh()

def open_drawing(w, canvas_dim, fpath):
    """Open a drawing file

    Open a .paint file specified in `fpath`. `fpath` is specified
    relative to the current working directory.

    If successful, it will return a 2-ary tuple (`is_success`, `str_info`)
    relating to the result of the file open. If successful, `is_success` is
    `True` and `str_info` contains `fpath`. Otherwise, `is_success` is `False`
    and `str_info` will either return an error message as a string or `None`.
    
    In addition, this function will clear the canvas and draw the contents
    of the file on it if the file is found and reading is successful.

    :param w: the `Window` object
    :type w: `class Window`
    :param canvas_dim: canvas dimensions as a 2-ary tuple `(row, column)`
    :type canvas_dim: tuple
    :param fpath: path to the paint file relative to the current working directory
    :type fpath: string
    :return: `tuple` (`bool`, `str`) of the status of opening
    """
    # HINT: Read on the `with` construct and `open()` function somewhere to open a file
    
    file_suffix = Path(fpath).suffix
    try:
        if file_suffix == '.paint':
            with open(fpath, 'r') as open_file:
                magic_string = open_file.readline().strip()
                if magic_string == 'EEE111_PAINT1234':
                    for y_value in range(canvas_dim[0]):
                        color_cell_at(w, (y_value, 0), 0, True)
                    y_coord = 0
                    for line in open_file:
                        x_coord = 0
                        for pixel in line.strip():
                            color_cell_at(w, (y_coord, x_coord), color_input('rawInput-idx dict')[pixel])
                            x_coord += 1
                        y_coord += 1
                    return (True, fpath)
                else:
                    return (False, fpath)
        else:
            return (False, fpath)
    except:
        return (False, fpath)

def save_drawing(w, canvas_dim, fpath):
    """Save a drawing file

    Save the drawing on the canvas to the file path specified in `fpath`.
    `fpath` is specified relative to the current working directory. If
    the file exists, it will be overwritten. If `fpath` does not end with
    `.paint`, the function will append `.paint` to the path before saving.

    If successful, it will return a 2-ary tuple (`is_success`, `str_info`)
    relating to the result of the file open. If successful, `is_success` is
    `True` and `str_info` contains `fpath`. Otherwise, `is_success` is `False`
    and `str_info` will either return an error message as a string or `None`.
    
    In addition, this function will clear the canvas and draw the contents
    of the file on it if the file is found and reading is successful.

    :param w: the `Window` object
    :type w: `class Window`
    :param canvas_dim: canvas dimensions as a 2-ary tuple `(row, column)`
    :type canvas_dim: tuple
    :param fpath: path to the paint file relative to the current working directory
    :type fpath: string
    :return: `tuple` (`bool`, `str`) of the status of opening
    """
    # HINT: Read on the `with` construct and `open()` function somewhere to open a file
    
    try:
        if Path(fpath).suffix != '.paint':
            fpath += '.paint'
        
        with open(fpath, 'w') as save_file:
            save_file.write('EEE111_PAINT1234\n')
            y_coord = 0
            for line in range(canvas_dim[0]):
                x_coord = 0
                for pixel in range(canvas_dim[1]):
                    pixel_color = get_color_pair_idx_at(w, (y_coord, x_coord))
                    save_file.write(color_input('idx-rawInput dict')[pixel_color])
                    x_coord += 1
                save_file.write('\n')
                y_coord += 1
            return (True, fpath)
    except:
        return (False, fpath)

def constant_commands(w, term_dim, canvas_dim, key, now_paint_mode):
    if key in (curses.KEY_UP, curses.KEY_DOWN, curses.KEY_LEFT, curses.KEY_RIGHT):
        move_cursor(w, canvas_dim, key, get_cursor_pos())
        w.refresh()

    elif key == curses.ascii.ctrl(ord('p')):
        now_paint_mode = 'Pencil'
        print_status_bar(w, term_dim, msg=f'> {now_paint_mode} Mode')
        return now_paint_mode

    elif key == curses.ascii.ctrl(ord('f')):
        now_paint_mode = 'Fill'
        print_status_bar(w, term_dim, msg=f'> {now_paint_mode} Mode')
        return now_paint_mode

    elif key == curses.ascii.ctrl(ord('x')):    # ^X (clear canvas)
        clear_canvas(w, term_dim, canvas_dim)

    elif key == curses.ascii.ctrl(ord('o')):    # ^O (open drawing)
        success = open_drawing(w, canvas_dim, collect_text_prompt(w, term_dim, lines_from_end=2, msg='Enter drawing to open: '))
        if success[0] == True:
            print_status_bar(w, term_dim, msg='Drawing opened!')
        
        elif success[0] == False:
            print_status_bar(w, term_dim, msg='Drawing NOT opened!')

    elif key == curses.ascii.ctrl(ord('s')):    # ^S (save drawing)
        success = save_drawing(w, canvas_dim, collect_text_prompt(w, term_dim, lines_from_end=2, msg='Enter path to save drawing: '))
        if success[0] == True:
            print_status_bar(w, term_dim, msg='Drawing saved!')
        
        elif success[0] == False:
            print_status_bar(w, term_dim, msg='Drawing NOT saved!')

def ui_main(w):
    # Initialize color pairs
    init_ui(w)

    term_dim = get_term_dim()
    canvas_dim = get_canvas_dim()
    for y_value in range(canvas_dim[0]):
            color_cell_at(w, (y_value, 0), 10, True)
    now_paint_mode = 'Pencil'
    print_status_bar(w, term_dim, msg=f'> {now_paint_mode} Mode')
    print_command_cheatsheet(w, term_dim)
    
    while True:
        now_coord = get_cursor_pos()
        if now_paint_mode == 'Pencil':
            key = w.getch()

            if key in color_input('color input tuple'):
                pencil_canvas(w, canvas_dim, now_coord, key)
                            
            elif key == curses.ascii.ctrl(ord('q')):    # ^Q (quit TerminalPaint)
                yn = None
                while yn != True:
                    yn = show_yn_prompt(w, term_dim, (8, 40), msg='Exit TerminalPaint?')
                    if yn == False:
                        break
                if yn == True:
                    break
            else:
                command = constant_commands(w, term_dim, canvas_dim, key, now_paint_mode)
                if command == 'Fill':
                    now_paint_mode = 'Fill'
                
        elif now_paint_mode == 'Fill':
            key = w.getch()
                            
            if key in color_input('color input tuple'):
                fill_canvas(w, canvas_dim, now_coord, key)
            
            elif key == curses.ascii.ctrl(ord('q')):    # ^Q (quit TerminalPaint)
                yn = None
                while yn != True:
                    yn = show_yn_prompt(w, term_dim, (8, 40), msg='Exit TerminalPaint?')
                    if yn == False:
                        break
                if yn == True:
                    break
            else:
                command = constant_commands(w, term_dim, canvas_dim, key, now_paint_mode)
                if command == 'Pencil':
                    now_paint_mode = 'Pencil'

def main():
    curses.wrapper(ui_main)

if __name__ == '__main__':
    main()