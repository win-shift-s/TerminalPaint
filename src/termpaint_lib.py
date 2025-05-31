import curses
import curses.ascii

def get_term_dim():
    """Get terminal dimensions

    :return: 2-ary tuple of the dimensions in `(rows, columns)`
    """
    return (curses.LINES, curses.COLS)

def get_canvas_dim():
    """Get canvas dimensions

    The canvas dimensions are dependent on the output of `get_term_dim()`.
    It is guaranteed that each of the dimensions is smaller than the
    terminal dimensions.

    :return: 2-ary tuple of the dimensions in `(rows, columns)`
    """
    return tuple([x - y for x, y in zip(get_term_dim(), [3, 0])])

def get_cursor_pos():
    """Get current cursor position

    This returns the cursor position relative to the terminal dimensions.

    :return: 2-ary tuple of the position in `(row, column)`
    """
    return curses.getsyx()

def create_center_win(win_dim, term_dim):
    """Create a new window with the given dimensions

    When this function is called, the window is immediately shown.

    :param win_dim: window dimensions as a 2-ary tuple `(row, column)`
    :type win_dim: tuple
    :param term_dim: terminal dimensions as a 2-ary tuple `(row, column)`
    :type term_dim: tuple
    :return: the `Window` object created
    """
    center_dim = ((term_dim[0] - win_dim[0]) // 2, (term_dim[1] - win_dim[1]) // 2)
    return curses.newwin(win_dim[0], win_dim[1], center_dim[0], center_dim[1]), center_dim

def show_yn_prompt(w, term_dim, size=(8, 40), msg='Are you sure?'):
    """Create a new yes/no window with the given dimensions and prompt

    When this function is called, the window is immediately shown containing
    the provided prompt and two options - yes and no. The user will then be
    given a choice to select either "Yes" or "No" by moving the left and
    right arrow keys. Pressing enter on the choice will select it, and the
    window will be dismissed.

    The minimum dimensions for the prompt should be `(7, 14)`

    If the message length exceeds the column dimension in `size`, the message
    gets chopped off to fit the window (to 4 minus the column in `size`).

    :param w: the `Window` object
    :type w: `class Window`
    :param term_dim: terminal dimensions as a 2-ary tuple `(row, column)`
    :type term_dim: tuple
    :param size: size of the prompt as a 2-ary tuple `(row, column)`
    :type size: tuple
    :param msg: message to show in the prompt window
    :type msg: string
    :return: `bool` - `True` if the user chose "Yes"
    """
    if len(msg) >= size[1]:
        # Chop off message if it overflows
        msg = msg[:size[1] - 4]
    
    if size[0] < 7 or size[1] < 14:
        raise Exception('Prompt dimensions are too small - minimum is (7, 14)')

    no_loc = (size[1] - len(msg)) // 2
    yes_loc = no_loc + (len(msg) - 5)

    current_cur = get_cursor_pos()
    curses.curs_set(1)

    prompt_w, prompt_w_dims = create_center_win(size, term_dim)
    prompt_w.bkgd(curses.color_pair(1))
    prompt_w.box()
    prompt_w.addstr(2, no_loc, msg)
    prompt_w.addstr(size[0] - 3, no_loc, 'No', curses.color_pair(2)) # Selected
    prompt_w.addstr(size[0] - 3, yes_loc, 'Yes')
    w.move(size[0] - 3 + prompt_w_dims[0], no_loc + prompt_w_dims[1])
    prompt_w.refresh()
    
    is_yes = False

    while True:
        prompt_ch = w.getch()

        if prompt_ch == curses.KEY_LEFT and is_yes:
            prompt_w.addstr(size[0] - 3, no_loc, 'No', curses.color_pair(2)) # Selected
            prompt_w.addstr(size[0] - 3, yes_loc, 'Yes')
            w.move(size[0] - 3 + prompt_w_dims[0], no_loc + prompt_w_dims[1])

            is_yes = not is_yes
        elif prompt_ch == curses.KEY_RIGHT and not is_yes:
            prompt_w.addstr(size[0] - 3, no_loc, 'No')
            prompt_w.addstr(size[0] - 3, yes_loc, 'Yes', curses.color_pair(2)) # Selected
            w.move(size[0] - 3 + prompt_w_dims[0], yes_loc + prompt_w_dims[1])

            is_yes = not is_yes
        elif prompt_ch == curses.KEY_ENTER or prompt_ch == ord('\n') or prompt_ch == ord('\r'):
            break

        prompt_w.refresh()

    curses.curs_set(2)

    if not is_yes:
        w.move(current_cur[0], current_cur[1])

        del prompt_w
        w.touchwin()
        w.refresh()
    
    return is_yes

def collect_text_prompt(w, term_dim, lines_from_end=2, msg='Input: '):
    """Collect text prompt

    When this function is called, a prompt is printed on the screen
    at the specified line counting from the end of the terminal. The
    user is given an opportunity to type some text and press `ENTER`
    to finish the input.

    :param w: the `Window` object
    :type w: `class Window`
    :param term_dim: terminal dimensions as a 2-ary tuple `(row, column)`
    :type term_dim: tuple
    :param lines_from_end: number of lines from the end where the text prompt will be printed
    :type size: int
    :param msg: message to show in the text prompt
    :type msg: string
    :return: `string` of the input received
    """
    cur_coord = get_cursor_pos()
    curses.curs_set(1)

    w.addstr(term_dim[0] - lines_from_end - 1, 0, ' ' * (term_dim[1] - 1))
    w.addstr(term_dim[0] - lines_from_end - 1, 0, msg)

    curses.echo()
    prompt = w.getstr().decode()
    curses.noecho()

    curses.curs_set(2)
    w.move(cur_coord[0], cur_coord[1])
    w.refresh()

    return prompt

def print_status_bar(w, term_dim, msg):
    """Print to the status bar

    Note that the whole line will be erased to accommodate the prompt.

    :param w: the `Window` object
    :type w: `class Window`
    :param term_dim: terminal dimensions as a 2-ary tuple `(row, column)`
    :type term_dim: tuple
    :param msg: message to show in the text prompt
    :type msg: string
    """
    cur_coord = get_cursor_pos()

    w.addstr(term_dim[0] - 3, 0, ' ' * (term_dim[1] - 1))
    w.addstr(term_dim[0] - 3, 0, msg)

    w.move(cur_coord[0], cur_coord[1])
    w.refresh()

def print_command_cheatsheet(w, term_dim):
    """Print the command cheatsheet

    When this function is called, the command cheatsheet will be printed
    starting from the second to the last line in the terminal.

    :param w: the `Window` object
    :type w: `class Window`
    :param term_dim: terminal dimensions as a 2-ary tuple `(row, column)`
    :type term_dim: tuple
    """
    cmds = [
        ('^P', 'Pencil'),
        ('^F', 'Fill'),
        ('^X', 'Clear'),
        ('^O', 'Open'),
        ('^S', 'Save'),
        ('^Q', 'Quit'),
    ]
    
    current_cur = get_cursor_pos()

    str_idx = [1, 0]
    for each_cmd in cmds:
        if str_idx[0] < 0:
            break

        w.addstr(term_dim[0] - str_idx[0] - 1, str_idx[1], each_cmd[0], curses.color_pair(2))
        str_idx[1] += len(each_cmd[0]) + 1

        w.addstr(term_dim[0] - str_idx[0] - 1, str_idx[1], each_cmd[1])
        str_idx[1] += len(each_cmd[1]) + 1

        if str_idx[1] >= term_dim[1]:
            str_idx[0] -= 1
    
    w.move(current_cur[0], current_cur[1])

    w.refresh()

def init_color_pairs():
    """Initialize and save some color pairs

    This function generates 10 pairs of colors. The indices
    and corresponding colors are as follows:

    ```
        FG       BG
    ------------------
    0   WHITE    BLACK
    1   WHITE    GREEN
    2   BLACK    WHITE
    3   BLACK    RED
    4   BLACK    GREEN
    5   BLACK    BLUE
    6   BLACK    CYAN
    7   BLACK    MAGENTA
    8   BLACK    YELLOW
    9   BLACK    WHITE
    10  BLACK    BLACK
    ```

    The color pairs can be used as an attribute in `curses` methods
    by using `curses.color_pair(idx)`.
    """
    color_map = [
        curses.COLOR_RED, curses.COLOR_GREEN, curses.COLOR_BLUE,
        curses.COLOR_CYAN, curses.COLOR_MAGENTA, curses.COLOR_YELLOW,
        curses.COLOR_WHITE, curses.COLOR_BLACK,
    ]

    # Fixed color pairs
    curses.init_pair(1, curses.COLOR_WHITE, curses.COLOR_GREEN)
    curses.init_pair(2, curses.COLOR_BLACK, curses.COLOR_WHITE)

    # Color pairs for drawing
    for i, color_seq in enumerate(color_map):
        curses.init_pair(3 + i, curses.COLOR_BLACK, color_seq)

def get_color_pair_idx_at(w, coord):
    """Get color pair index at coordinate

    This function returns the color pair index at `coord`. This index
    is the same as the corresponding one generated from `init_color_pairs()`.

    :param w: the `Window` object
    :type w: `class Window`
    :param coord: coordinate as a 2-ary tuple `(row, column)`
    :type coord: tuple
    :return: `int` color pair index
    """
    return curses.pair_number(w.inch(coord[0], coord[1]) & curses.A_COLOR)

def color_cell_at(w, coord, color_pair_idx, until_end=False):
    """Color a cell at the specified coordinate

    This function returns the color pair index at `coord`. This index
    is the same as the corresponding one generated from `init_color_pairs()`.

    :param w: the `Window` object
    :type w: `class Window`
    :param coord: coordinate as a 2-ary tuple `(row, column)`
    :type coord: tuple
    :param color_pair_idx: index of the color-pair `coord` should be set to
    :type color_pair_idx: int
    :param until_end: `True` if all columns from `coord[1]` and right of it should be colored with the new color-pair
    :type until_end: bool
    """
    if until_end:
        w.chgat(coord[0], coord[1], curses.color_pair(color_pair_idx))
    else:
        w.chgat(coord[0], coord[1], 1, curses.color_pair(color_pair_idx))

def init_ui(w):
    """Initialize the UI

    This should be called once `curses` has been initialized.
    """
    init_color_pairs()
    curses.curs_set(2)
    w.move(0, 0)
