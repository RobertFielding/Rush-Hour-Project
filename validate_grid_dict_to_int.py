from collections import namedtuple
Vehicle = namedtuple('Vehicle', 'coordinate orientation vehicle_length')
from tkinter import messagebox



def validate_dict(coord_dict):
    # Receive dictionary as {'red': (1, 1), (1, 2), ...}
    cond_dict = dict()
    for key, value_list in coord_dict.items():
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

    if colour_trialed == "red":
        if y_coord != 4:
            messagebox.showerror("Error", f"The {colour_trialed} vehicle must be horizontal to the exit cell.")
            return False

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
        # Cannot be both x and y valid, as the cars must be greater than 2 in length
        if x_valid:
            index = 1
        else:
            index = 0

        list_of_coord = [list_of_coords[i][index] for i in range(list_len)]
        minim, maxim = min(list_of_coord), max(list_of_coord)
        if maxim - minim != len(list_of_coord) - 1:
            messagebox.showerror("Error", f"You can only have one {colour_trialed} vehicle")
            return False

        # Passed checks
        if x_valid:
            return Vehicle((x_coord, minim), 'ud', len(list_of_coord))
        else:
            return Vehicle((minim, y_coord), 'lr', len(list_of_coord))
    else:
        messagebox.showerror("Error", f"{colour_trialed} vehicles must be on a line")
        return False

