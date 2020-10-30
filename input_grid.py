import time
from tkinter import *
from tkinter import messagebox
from rush_hour_solver import bfs
from validate_grid_dict_to_int import validate_dict
import pyautogui

# A simple colouring grid app, with load/save functionality.
# Christian Hill, August 2018.

# Maximum and default grid size
max_n, default_grid_size = 26, 6
# The "default" colour for an unfilled grid cell
unfilled = '#fff'

class GridApp:
    """The main class representing a grid of coloured cells."""

    # The colour palette
    colours = (unfilled, 'red', 'green', 'lightgreen', 'olive', 'lightblue', 'darkblue', 'blue', 'cyan', 'orange', 'yellow',
               'magenta', 'purple', 'pink', 'brown', 'black', '#f5f5dc')
    ncolours = len(colours)

    def __init__(self, master, n, width=600, height=600, pad=5):
        """Initialize a grid and the Tk Frame on which it is rendered."""

        # Number of cells in each dimension.
        self.n = n
        # Some dimensions for the App in pixels.
        self.width, self.height = width, height
        palette_height = 40
        # Padding stuff: xsize, ysize is the cell size in pixels (without pad).
        npad = n + 1
        self.pad = pad
        xsize = (width - npad*pad) / n
        ysize = (height - npad*pad) / n
        exit_cell_width = xsize / 2
        width += exit_cell_width
        # Canvas dimensions for the cell grid and the palette.
        c_width, c_height = width, height
        p_pad = 5
        p_width = p_height = palette_height - 2*p_pad

        # The main frame onto which we draw the App's elements.
        frame = Frame(master)
        frame.pack()

        # The palette for selecting colours.
        self.palette_canvas = Canvas(master, width=c_width,
                                     height=palette_height)
        self.palette_canvas.pack()

        # Add the colour selection rectangles to the palette canvas.
        self.palette_rects = []
        for i in range(self.ncolours):
            x, y = p_pad * (i+1) + i*p_width, p_pad
            rect = self.palette_canvas.create_rectangle(x, y,
                            x+p_width, y+p_height, fill=self.colours[i])
            self.palette_rects.append(rect)
        # ics is the index of the currently selected colour.
        self.ics = 0
        self.select_colour(self.ics)

        # The canvas onto which the grid is drawn.
        self.w = Canvas(master, width=c_width, height=c_height)
        self.w.pack()

        # Add the cell rectangles to the grid canvas.
        self.cells = []
        for iy in range(n):
            for ix in range(n):
                xpad, ypad = pad * (ix+1), pad * (iy+1)
                x, y = xpad + ix*xsize, ypad + iy*ysize
                rect = self.w.create_rectangle(x, y, x + xsize,
                                               y + ysize, fill=unfilled)
                self.cells.append(rect)
                if ix == 5 and iy == 2:
                    xpad = pad * (ix + 2)
                    x, y = xpad + (ix + 1) * xsize, ypad + iy * ysize
                    rect = self.w.create_rectangle(x, y, x + exit_cell_width,
                                                   y + ysize, fill='gold')
                    mylabel = self.w.create_text((x + exit_cell_width / 2, (y + ysize / 2)), text="Exit")

        # Solve button
        b_save = Button(frame, text='Solve', command=self.grid_to_dict)
        b_save.pack(side=RIGHT, padx=pad, pady=pad)

        def palette_click_callback(event):
            """Function called when someone clicks on the palette canvas."""
            x, y = event.x, event.y

            # Did the user click a colour from the palette?
            if p_pad < y < p_height + p_pad:
                # Index of the selected palette rectangle (plus padding)
                ic = x // (p_width + p_pad)
                # x-position with respect to the palette rectangle left edge
                xp = x - ic*(p_width + p_pad) - p_pad
                # Is the index valid and the click within the rectangle?
                if ic < self.ncolours and 0 < xp < p_width:
                    self.select_colour(ic)
        # Bind the palette click callback function to the left mouse button
        # press event on the palette canvas.
        self.palette_canvas.bind('<ButtonPress-1>', palette_click_callback)

        def w_click_callback(event):
            """Function called when someone clicks on the grid canvas."""
            x, y = event.x, event.y

            # Did the user click a cell in the grid?
            # Indexes into the grid of cells (including padding)
            ix = int(x // (xsize + pad))
            iy = int(y // (ysize + pad))
            xc = x - ix*(xsize + pad) - pad
            yc = y - iy*(ysize + pad) - pad
            if ix < n and iy < n and 0 < xc < xsize and 0 < yc < ysize:
                i = iy*n+ix
                self.w.itemconfig(self.cells[i], fill=self.colours[self.ics])
        # Bind the grid click callback function to the left mouse button
        # press event on the grid canvas.
        self.w.bind('<ButtonPress-1>', w_click_callback)

    def select_colour(self, i):
        """Select the colour indexed at i in the colours list."""

        self.palette_canvas.itemconfig(self.palette_rects[self.ics],
                                       outline='black', width=1)
        self.ics = i
        self.palette_canvas.itemconfig(self.palette_rects[self.ics],
                                       outline='black', width=5)

    def _get_cell_coords(self, i):
        """Get the <letter><number> coordinates of the cell indexed at i."""

        # The horizontal axis is labelled A, B, C, ... left-to-right;
        # the vertical axis is labelled 1, 2, 3, ... bottom-to-top.
        iy, ix = divmod(i, self.n)
        return '{}{}'.format(chr(ix+65), self.n-iy)

    def grid_to_dict(self):
        """Output a list of cell coordinates, sorted by cell colour."""

        # When we save the list of coordinates with each colour it looks
        # better if we limit the number of coordinates on each line of output.
        MAX_COORDS_PER_ROW = 12

        def _get_coloured_cells_dict():
            """Return a dictionary of cell coordinates and their colours."""

            coloured_cell_cmds = {}
            for i, rect in enumerate(self.cells):
                c = self.w.itemcget(rect, 'fill')
                if c == unfilled:
                    continue
                coloured_cell_cmds[self._get_cell_coords(i)] = c
            return coloured_cell_cmds

        # Create a dictionary of colours (the keys) and a list of cell
        # coordinates with that colour (the value).
        coloured_cell_cmds = _get_coloured_cells_dict()
        cell_colours = {}
        for k, v in coloured_cell_cmds.items():
            cell_colours.setdefault(v, []).append(k)
        self.solve(cell_colours)


    def dict_to_grid(self, num_dict):
        '''
        :param num_dict: keys are colours, values is a list of coordinates
        :return:
        '''
        unoccupied_coords = [(x, y) for x in range(1, 7) for y in range(1, 7)]
        for colour, coords_list in num_dict.items():
            for coord in coords_list:
                cell_num = (coord[0] - 1) + 6 * (coord[1] - 1)
                self.w.itemconfig(self.cells[cell_num], fill=colour)
                unoccupied_coords.remove(coord)

        for coord in unoccupied_coords:
            cell_num = (coord[0] - 1) + 6 * (coord[1] - 1)
            self.w.itemconfig(self.cells[cell_num], fill=unfilled)
        # update after all cells have been assigned colour
        self.w.update()

    def solve(self, test_dict):
        dict_valid = validate_dict(test_dict)
        if dict_valid:
            valid_dict = dict_valid
            list_of_moves = bfs(valid_dict)
            if list_of_moves:
                for index, grid_formation in enumerate(list_of_moves):
                    self.dict_to_grid(grid_formation)
                    time.sleep(1)
            else:
                messagebox.showerror("Error", "The board is not solvable")


# Get the grid size from the command line, if provided
try:
    n = int(sys.argv[1])
except IndexError:
    n = default_grid_size
except ValueError:
    print('Usage: {} <n>\nwhere n is the grid size.'.format(sys.argv[0]))
    sys.exit(1)
if n < 1 or n > max_n:
    print('Minimum n is 1, Maximum n is {}'.format(max_n))
    sys.exit(1)

# Set the whole thing running
root = Tk()
grid = GridApp(root, n, 600, 600, 5)
root.mainloop()
