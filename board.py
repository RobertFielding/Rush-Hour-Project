class Board:
    def __init__(self, grid_size, vehicles, colour_indices):
        self.grid_size = grid_size
        self.vehicles = vehicles  # vehicles is a tuple of length # colours
        self.colour_indices = colour_indices

    def __eq__(self, other):
        if self.__class__ != other.__class__:
            return False
        return self.vehicles == other.vehicles

    def get_car(self, colour):
        i = self.colour_indices[colour]
        return self.vehicles[i]

    def possible_moves(self):
        occupied_cells = set()
        for vehicle in self.vehicles:
            if vehicle:
                occupied_cells.update(vehicle.co_ordinates())
        potential_boards = []
        for i, vehicle in enumerate(self.vehicles):
            if vehicle:
                for shift in [-1, 1]:
                    shifted_vehicle = vehicle.create_shifted(shift)
                    new_cell = shifted_vehicle.co_ordinates()[0 if shift == -1 else -1]
                    on_grid = new_cell[0] in range(self.grid_size) and new_cell[1] in range(self.grid_size)
                    unoccupied = new_cell not in occupied_cells
                    if on_grid and unoccupied:
                        moved_vehicles = self.vehicles[:i] + (shifted_vehicle,) + self.vehicles[i+1:]
                        potential_boards.append(Board(self.grid_size, moved_vehicles, self.colour_indices))
        return potential_boards

    def __hash__(self):
        return hash(self.vehicles)
