def convert(dictionary):
    renamed_dict = {}
    true_keys_list = []

    for index, key in enumerate(dictionary):
        # Renaming keys as "0", "1", "2", ...
        renamed_dict[index] = dictionary[key]

        # Appending true keys to the list
        if dictionary[key] == True:
            true_keys_list.append(str(index))
    new_list = [int(x) for x in true_keys_list]

    return new_list


def convert_usage_windows(input_dict):
    usage_windows = []
    start_time = None

    for window, active in input_dict.items():
        hour_range = window.split('-')
        if active:
            if start_time is None:
                start_time = int(hour_range[0])
        elif start_time is not None:
            end_time = int(hour_range[0])
            usage_windows.append([start_time, end_time])
            start_time = None
    if start_time is not None:
        # If there's an active window at the end of the day
        # assume it ends at midnight (24)
        usage_windows.append([start_time, 24])

    return usage_windows

def rename_keys(dictionary):
    new_dict = {}
    for i, key in enumerate(dictionary):
        new_dict[i] = dictionary[key]
    return new_dict

def set_values (dictionary, variable):
    new_dict = {}
    for key in dictionary:
        new_dict[key] = variable
    return new_dict

