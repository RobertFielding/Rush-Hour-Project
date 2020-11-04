import time
from collections import defaultdict, deque
from tkinter import *
from tkinter import messagebox
from vehicle import Vehicle
from board import Board

grid_size = 6
# The "default" colour for unfilled grid cells
unfilled = '#fff'
colours = (unfilled, 'red', 'lightgreen', 'purple', 'orange', 'blue', 'cyan', 'yellow', '#4e2e53', 'black', 'pink',
           'darkgreen', 'olive', 'palegoldenrod', 'royalblue', 'brown')
colour_indices = {c: i for i, c in enumerate(colours[1:])}


def validate_vehicles(vehicle_dict):
    """
    :param vehicle_dict: dictionary with colours and list coordinates as keys and values respectively
    :return: A tuple of Vehicles ordered by colour
    """
    if 'red' not in vehicle_dict:
        messagebox.showerror("Error", f"There must be a red car on the row with the exit tile.")
        return None

    vehicles = []
    for colour in colours[1:]:
        coordinates = vehicle_dict.get(colour)
        vehicle = validate_vehicle(coordinates, colour) if coordinates else None
        vehicles.append(vehicle)
    return tuple(vehicles)


def validate_vehicle(vehicle, colour):
    """
    :param vehicle: A list of coordinates
    :param colour:
    :return: Vehicle class Vehicle(root, orientation, length, colour)
    """

    if len(vehicle) < 2:
        messagebox.showerror("Error", f"Length of {colour} vehicle cannot be less than 2 squares.")
        return None

    set_x, set_y = set(), set()
    min_x, max_x, min_y, max_y = float("nan"), float("nan"), float("nan"), float("nan")
    for x, y in vehicle:
        set_x.add(x)
        set_y.add(y)
        min_x = min(x, min_x)
        max_x = max(x, max_x)
        min_y = min(y, min_y)
        max_y = max(y, max_y)

    # checks red is on line with exit
    if colour == "red" and (min_y != 2 or max_y != 2):
        messagebox.showerror("Error", f"The {colour} vehicle must be horizontal to the exit cell.")
        return None

    valid_vertical = len(set_x) == 1 and max_y - min_y + 1 == len(set_y)
    valid_horizontal = len(set_y) == 1 and max_x - min_x + 1 == len(set_x)
    if not (valid_horizontal or valid_vertical):
        messagebox.showerror("Error", f"{colour} vehicle is invalid")
        return None
    orientation = "ud" if valid_vertical else "lr"
    return Vehicle((min_x, min_y), orientation, len(vehicle), colour)


class GridApp:
    """The main class representing a grid of coloured cells."""
    ncolours = len(colours)

    def __init__(self, master, grid_size, width=550, height=550, pad=5):
        """Initialize a grid and the Tk Frame on which it is rendered."""
        self.grid_size = grid_size
        self.width, self.height = width, height
        palette_height = 42.2
        # Padding between cells; x_size, y_size are cell width and length in pixels
        n_pad = grid_size + 1
        self.pad = pad
        x_size = (width - n_pad*pad) / grid_size
        y_size = (height - n_pad*pad) / grid_size
        # Extra width due to exit cell
        exit_cell_width = x_size / 2
        width += exit_cell_width
        # Canvas dimensions
        canvas_width, canvas_height = width, height
        # Palette padding and width of colour selection tiles
        pal_pad = 5
        p_width = p_height = palette_height - 2*pal_pad

        # The main frame onto which we draw the App's elements.
        frame = Frame(master)
        frame.pack()

        # Create palette canvas
        self.palette_canvas = Canvas(master, width=canvas_width, height=palette_height)
        self.palette_canvas.pack()

        # Add colour selection tiles to the palette canvas.
        self.palette_rects = []
        for i in range(self.ncolours):
            x, y = pal_pad * (i+1) + i*p_width, pal_pad
            rect = self.palette_canvas.create_rectangle(x, y, x+p_width, y+p_height, fill=colours[i])
            self.palette_rects.append(rect)
        # colour_index is currently selected colour
        self.colour_index = 0
        self.select_colour(self.colour_index)

        # Create canvas of grid
        self.canvas = Canvas(master, width=canvas_width, height=canvas_height)
        self.canvas.pack()

        # Add cell rectangles to grid canvas.
        self.cells = []
        for iy in range(grid_size):
            for ix in range(grid_size):
                pad_in_x, pad_in_y = pad * (ix+1), pad * (iy+1)
                x, y = pad_in_x + ix*x_size, pad_in_y + iy*y_size
                rect = self.canvas.create_rectangle(x, y, x + x_size, y + y_size, fill=unfilled)
                self.cells.append(rect)

        # Create exit cell
        ix, iy = 6, 2
        pad_in_x, pad_in_y = pad * (ix + 1), pad * (iy + 1)
        x, y = pad_in_x + ix*x_size, pad_in_y + iy*y_size
        self.canvas.create_rectangle(x, y, x + exit_cell_width, y + y_size, fill='gold')
        self.canvas.create_text((x + exit_cell_width / 2, y + y_size / 2), text="Exit")

        # Solve button
        b_save = Button(frame, text='Solve', command=self.grid_to_tuple)
        b_save.pack(side=RIGHT, padx=pad, pady=pad)

        def palette_click_callback(event):
            """Function called when someone clicks on the palette canvas."""
            x, y = event.x, event.y

            # Checks if user clicks in horizontal space of palette
            if pal_pad < y < p_height + pal_pad:
                # Index of the selected palette rectangle (plus padding)
                ic = int(x // (p_width + pal_pad))
                # x-position of left-side of palette tile
                xp = x - ic*(p_width + pal_pad) - pal_pad
                # Is the click on the palette, and is it on a tile
                if ic < self.ncolours and 0 < xp < p_width:
                    self.select_colour(ic)
        # Palette click callback checks each time the left mouse button is pressed
        self.palette_canvas.bind('<ButtonPress-1>', palette_click_callback)

        def w_click_callback(event):
            """Function called when someone clicks on the grid canvas."""
            x, y = event.x, event.y

            # Checks if user clicks on grid
            # Indexes into the grid of cells (including padding)
            ix = int(x // (x_size + pad))
            iy = int(y // (y_size + pad))
            xc = x - ix*(x_size + pad) - pad
            yc = y - iy*(y_size + pad) - pad
            if ix < grid_size and iy < grid_size and 0 < xc < x_size and 0 < yc < y_size:
                cell_index = iy * grid_size + ix
                self.canvas.itemconfig(self.cells[cell_index], fill=colours[self.colour_index])
        # Grid click callback triggers each time the left mouse key is pressed
        self.canvas.bind('<ButtonPress-1>', w_click_callback)

    def select_colour(self, updated_colour):
        """Select the colour indexed at i in the colours list."""

        self.palette_canvas.itemconfig(self.palette_rects[self.colour_index],
                                       outline='black', width=1)
        self.colour_index = updated_colour
        self.palette_canvas.itemconfig(self.palette_rects[self.colour_index],
                                       outline='black', width=5)

    def _get_cell_coords(self, rect_index):
        """Given a cell number on the grid, it returns the coordinates"""

        # The horizontal axis is labelled 0, 1, 2, ... left-to-right;
        # the vertical axis is labelled 0, 1, 2, ... top-to-bottom.
        y, x = divmod(rect_index, self.grid_size)
        return (x, y)

    def grid_to_tuple(self):
        """Converts the cells to a dictionary with cell colour as keys, and a list of coordinates as values.
           Then triggers the board to be solved."""

        vehicles = defaultdict(list)
        for i, cell in enumerate(self.cells):
            colour = self.canvas.itemcget(cell, 'fill')
            if colour == unfilled:
                continue
            vehicles[colour].append(self._get_cell_coords(i))

        self.solve(vehicles)

    def gridify(self, board):
        """
        :param board: Board Class, tuple of class Vehicles ordered by colour
        :return:
        """
        unoccupied_cell_indices = [index for index in range(grid_size ** 2)]
        for vehicle in board.vehicles:
            if vehicle:
                multiplier = 1 if vehicle.orientation == 'lr' else 6
                for index in range(vehicle.length):
                    cell_num = vehicle.root[0] + 6 * vehicle.root[1] + multiplier * index
                    self.canvas.itemconfig(self.cells[cell_num], fill=vehicle.colour)
                    unoccupied_cell_indices.remove(cell_num)

        for index in unoccupied_cell_indices:
            self.canvas.itemconfig(self.cells[index], fill=unfilled)
        self.canvas.update()

    def bfs(self, board):
        red_car = board.get_car("red")
        if red_car.root == (4, 2):
            messagebox.showerror("Error", "The board is already solved")
            return [board]

        visited = {board}
        queue = deque()
        queue.append([board])
        while queue:
            move_history = queue.popleft()
            board = move_history[-1]
            red_car = board.get_car("red")
            if red_car.root == (4, 2):
                return move_history
            for neighbour in board.possible_moves():
                if neighbour not in visited:
                    visited.add(neighbour)
                    queue.append(move_history + [neighbour])
        return None

    def solve(self, vehicle_dict):
        vehicles = validate_vehicles(vehicle_dict)
        board = Board(grid_size, vehicles, colour_indices)
        moves = self.bfs(board)
        if moves:
            for board in moves:
                self.gridify(board)
                time.sleep(0.75)
        else:
            messagebox.showerror("Error", "The board is not solvable")

# Set the whole thing running
root = Tk()
grid = GridApp(root, grid_size, 600, 600, 5)
root.mainloop()
