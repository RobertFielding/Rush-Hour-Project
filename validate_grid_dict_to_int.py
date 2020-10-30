from collections import namedtuple
Vehicle = namedtuple('Vehicle', 'coordinate orientation vehicle_length')
from tkinter import messagebox


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
        vehicle_valid = validate_list(value_list, key)
        if vehicle_valid:
            cond_dict[key] = vehicle_valid
            continue
        else:
            return False
    return cond_dict

def validate_list(list_of_coords, colour_trialed):
    list_len = len(list_of_coords)
    if list_len < 2:
        messagebox.showerror("Error", f"Length of {colour_trialed} vehicle cannot be less than 2 squares.")
        return False

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
                messagebox.showerror("Error", f"You can only have one {colour_trialed} vehicle")
                return False

        if y_valid:
            y_list = [list_of_coords[i][0] for i in range(list_len)]
            minim, maxim = min(y_list), max(y_list)
            if maxim - minim != len(y_list) - 1:
                messagebox.showerror("Error", f"You can only have one {colour_trialed} vehicle")
                return False
        # Passed checks
        if x_valid:
            return Vehicle((x_coord, minim), 'ud', len(x_list))
        else:
            return Vehicle((minim, y_coord), 'lr', len(y_list))
    else:
        messagebox.showerror("Error", f"{colour_trialed} vehicles must be on a line")
        return False

