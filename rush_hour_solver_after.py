from collections import namedtuple

Vehicle = namedtuple('Vehicle', 'coordinate orientation vehicle_length')


def bfs(board):
    visited, queue = [], []
    visited.append(board)
    queue.append(board)
    first_iteration = True
    while queue:
        s = queue.pop(0)

        if not first_iteration:
            s, previous_boards_copy = s[-1], s.copy()

        coordinate, _, _ = s['red']
        if coordinate == (5, 4):
            board_history = []
            for board in previous_boards:
                board_history.append(convert_num_dict_to_grid_format(board))

            return board_history

        for neighbour in valid_board_changes(s):
            if neighbour not in visited:
                visited.append(neighbour)

                if first_iteration:
                    previous_boards_copy = [s]
                    first_iteration = False
                previous_boards = previous_boards_copy.copy()
                previous_boards.append(neighbour)

                queue.append(previous_boards)

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


def convert_num_dict_to_grid_format(num_dict):
    result_dict = {}
    for key, vehicle in num_dict.items():
        coordinate, orientiation, vehicle_length = vehicle
        coord_list = []
        if orientiation == 'lr':
            for i in range(vehicle_length):
                coord_list.append((coordinate[0]+i, 7-coordinate[1]))
            result_dict[key] = coord_list
        else:
            for i in range(vehicle_length):
                coord_list.append((coordinate[0], 7 - coordinate[1] - i))
            result_dict[key] = coord_list
    return result_dict


# with open('grid_dict.json') as f:
#     test_dict = json.load(f)
#
# dict_valid, dict_or_error = validate_dict(test_dict)
# if dict_valid:
#     valid_dict = dict_or_error
#     print("valid_dict", valid_dict)
# else:
#     raise dict_or_error
#
#
# if bfs(valid_dict):
#     list_of_moves = bfs(valid_dict)
#     print("list_of_moves", list_of_moves)

#     for grid_formation in list_of_moves:
#         print("here")
#         GridApp.dict_to_grid(grid_formation)
#         time.sleep(1)
#
