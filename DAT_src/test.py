import json

def detect_ramp_windows(survey):
    ramp_windows = []

    if len(survey) == 1:  # only one window given
        ramp_windows.append(survey[0])
        return ramp_windows
    else:  # more than one window given
        i = 0
        merged_window = survey[i]  # set first window to first merged window
        for window in survey:
            if merged_window[1] == survey[i+1][0]:  # Windows are neighbors
                merged_window = [merged_window[0], survey[i+1][1]]
            else:  # Windows are not neighbors
                ramp_windows.append(merged_window)
                merged_window = survey[i+1]
            i += 1

            if i+1 == len(survey):  # all windows were checked
                ramp_windows.append(merged_window)
                return ramp_windows


with open("first_survey.json", "r") as file:
    first_survey = json.load(file)

#hours of operation of appliances
data_1 = first_survey["B_11/in_bulb_hour_wd"]
data_1 = float(data_1)

data_2 = first_survey["B_11/in_bulb_hour_hd"]
data_2 = float(data_2)

in_bulb_usage_time_wd = in_bulb_daily_usage_time_wd(data_1)
in_bulb_usage_time_hd = in_bulb_daily_usage_time_hd(data_2)

# time windows
substrings = ["night_0-7","morning_7-10","morning_10-12","afternoon_12-18","evening_18-22","evening_22-24"]


windows = [
    [0, 7],
    [7, 10],
    [10, 12],
    [12, 18],
    [18, 22],
    [22, 24]
]


ramp_windows = detect_ramp_windows(survey)
print('Survey => Ramp:')
print(survey)
print("=>")
print(ramp_windows)