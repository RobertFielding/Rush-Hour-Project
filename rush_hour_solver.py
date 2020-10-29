from collections import namedtuple
Vehicle = namedtuple('Vehicle', 'coordinate orientation vehicle_length')

valid_dict = {'lightgreen': Vehicle(coordinate=(1, 6), orientation='lr', vehicle_length=2), 'yellow': Vehicle(coordinate=(6, 4), orientation='ud', vehicle_length=3), 'purple': Vehicle(coordinate=(1, 3), orientation='ud', vehicle_length=3), 'blue': Vehicle(coordinate=(4, 3), orientation='ud', vehicle_length=3), 'red': Vehicle(coordinate=(2, 4), orientation='lr', vehicle_length=2), 'orange': Vehicle(coordinate=(1, 1), orientation='ud', vehicle_length=2), 'cyan': Vehicle(coordinate=(5, 2), orientation='lr', vehicle_length=2), 'green': Vehicle(coordinate=(3, 1), orientation='lr', vehicle_length=3)}


def bfs(board):
    '''
    :param board: board is a dict
    :return:
    '''
    visited, queue = [], []
    visited.append(board)
    queue.append(board)
    while queue:
        s = queue.pop(0)

        coordinate, _, _ = s['red']
        if coordinate == (5, 4):
            return s

        for neighbour in valid_board_changes(s):
            if neighbour not in visited:
                visited.append(neighbour)
                queue.append(neighbour)
    return None

def valid_board_changes(valid_dict):
    spaces_occupied = spaces_occ(valid_dict)
    potential_boards = []
    for key, vehicle in valid_dict.items():
        nbhd_coords = neighbour_coords_changes(vehicle, spaces_occupied)
        if nbhd_coords:
            for updated_coord in nbhd_coords:
                new_board = valid_dict.copy()
                new_board[key] = updated_coord
                potential_boards.append(new_board)
        else:
            continue
    return potential_boards


def spaces_occ(valid_dict):
    spaces_occupied = set()
    for _, vehicle in valid_dict.items():
        coordinate, orientation, length = vehicle
        for i in range(length):
            if orientation == 'lr':
                spaces_occupied.add((coordinate[0]+i, coordinate[1]))
            else:
                spaces_occupied.add((coordinate[0], coordinate[1] + i))
    return spaces_occupied

def neighbour_coords_changes(vehicle, spaces_occupied):
    coordinate, orientation, length = vehicle
    updated_vehicle_pos = []
    if orientation == 'lr':
        if coordinate[0] != 1 and (coordinate[0]-1, coordinate[1]) not in spaces_occupied:
            updated_vehicle_pos.append(Vehicle((coordinate[0]-1, coordinate[1]), orientation, length))
        if coordinate[0] + (length - 1) != 6 and (coordinate[0] + length, coordinate[1]) not in spaces_occupied:
            updated_vehicle_pos.append(Vehicle((coordinate[0]+1, coordinate[1]), orientation, length))
    else:
        if coordinate[1] != 1 and (coordinate[0], coordinate[1]-1) not in spaces_occupied:
            updated_vehicle_pos.append(Vehicle((coordinate[0], coordinate[1]-1), orientation, length))
        if coordinate[1] + (length - 1) != 6 and (coordinate[0], coordinate[1]+length) not in spaces_occupied:
            updated_vehicle_pos.append(Vehicle((coordinate[0], coordinate[1]+1), orientation, length))
    if len(updated_vehicle_pos) > 0:
        return updated_vehicle_pos
    else:
        return None


print(bfs(valid_dict))