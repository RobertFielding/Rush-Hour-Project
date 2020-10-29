import json
from collections import namedtuple
Vehicle = namedtuple('Vehicle', 'coordinate orientation vehicle_length')

with open('grid_dict.json') as f:
    test_dict = json.load(f)

def convert_dict_to_int(dict):
    result_dict = {}
    for key, value_list in dict.items():
        result_list = []
        for value in value_list:
            coords = (ord(value[0]) - 64, int(value[1]))
            result_list.append(coords)
        result_dict[key] = result_list
    return result_dict


def validate_dict(alphabet_dict):
    num_dict = convert_dict_to_int(alphabet_dict)
    cond_dict = dict()
    for key, value_list in num_dict.items():
        valid_list, vehicle_or_error = validate_list(value_list)
        if valid_list:
            cond_dict[key] = vehicle_or_error
            continue
        else:
            return False, TypeError(f"There is an error with colour {key}. {vehicle_or_error}")
    return True, cond_dict

def validate_list(list_of_coords):
    list_len = len(list_of_coords)
    if list_len < 2:
        return False, ValueError("Length of vehicles cannot be less than 2 squares.")

    # test if the vehicles are on a line
    test_index = 1
    x_coord = list_of_coords[0][0]
    y_coord = list_of_coords[0][1]
    x_valid, y_valid = True, True
    while (x_valid or y_valid) and test_index < list_len:
        if x_valid:
            if x_coord != list_of_coords[test_index][0]:
                x_valid = False
        if y_valid:
            if y_coord != list_of_coords[test_index][1]:
                y_valid = False

        test_index += 1

    # if vehicles along a line, are they connected
    if x_valid or y_valid:
        if x_valid:
            x_list = [list_of_coords[i][1] for i in range(list_len)]
            minim, maxim = min(x_list), max(x_list)
            if maxim - minim != len(x_list) - 1:
                return False, TypeError("You can only have one vehicle of a single colour")

        if y_valid:
            y_list = [list_of_coords[i][0] for i in range(list_len)]
            minim, maxim = min(y_list), max(y_list)
            if maxim - minim != len(y_list) - 1:
                return False, TypeError("You can only have one vehicle of a single colour")
        # Passed checks
        if x_valid:
            return True, Vehicle((x_coord, minim), 'ud', len(x_list))
        else:
            return True, Vehicle((minim, y_coord), 'lr', len(y_list))
    else:
        return False, TypeError("Vehicles must be on a line")




# Input valid_dict into solver

