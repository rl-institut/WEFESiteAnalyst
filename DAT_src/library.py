import json

from DAT_src.kobo_api_access import load_kobo_data

# results = load_kobo_data(form_id="aCs4ygeFHN5jkb4endReWK")

# first_survey = results[0][0]

# with open("first_survey.json", "w") as file:
#    json.dump(first_survey, file)

def in_bulb_daily_usage_time_wd(x):
    return 60 * x

def in_bulb_daily_usage_time_hd(x):
    return 60 * x

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

substring_1 = "night_0-7"
substring_2 = "morning_7-10"
substring_3 = "morning_10-12"
substring_4 = "afternoon_12-18"
substring_5 = "evening_18-22"
substring_6 = "evening_22-24"
string = first_survey["B_11/in_bulb_usage_wd"]

'''
#time window_1
if (substring_1 in string) == True:
    in_bulb_start_1_wd = 0
    if (substring_2 in string) != True:
        in_bulb_end_1_wd = 7
    elif (substring_3 in string) != True:
        in_bulb_end_1_wd = 10
    elif (substring_4 in string) != True:
        in_bulb_end_1_wd = 12
    elif (substring_5 in string) != True:
        in_bulb_end_1_wd = 18
    elif (substring_6 in string) != True:
        in_bulb_end_1_wd = 22
    else:
        in_bulb_end_1_wd = 24

elif (substring_2 in string) == True:
    in_bulb_start_1_wd = 7
    if (substring_3 in string) != True:
        in_bulb_end_1_wd = 10
    elif (substring_4 in string) != True:
        in_bulb_end_1_wd = 12
    elif (substring_5 in string) != True:
        in_bulb_end_1_wd = 18
    elif (substring_6 in string) != True:
        in_bulb_end_1_wd = 22
    else:
        in_bulb_end_1_wd = 24
elif (substring_3 in string) == True:
    in_bulb_start_1_wd = 10
    if (substring_4 in string) != True:
        in_bulb_end_1_wd = 12
    elif (substring_5 in string) != True:
        in_bulb_end_1_wd = 18
    elif (substring_6 in string) != True:
        in_bulb_end_1_wd = 22
    else:
        in_bulb_end_1_wd = 24
elif (substring_4 in string) == True:
    in_bulb_start_1_wd = 12
    if (substring_5 in string) != True:
        in_bulb_end_1_wd = 18
    elif (substring_6 in string) != True:
        in_bulb_end_1_wd = 22
    else:
        in_bulb_end_1_wd = 24
elif (substring_5 in string) == True:
    in_bulb_start_1_wd = 18
    if (substring_6 in string) != True:
        in_bulb_end_1_wd = 22
    else:
        in_bulb_end_1_wd = 24
elif (substring_6 in string) == True:
    in_bulb_start_1_wd = 22
    in_bulb_end_1_wd = 24

#time window_2
if in_bulb_end_1_wd == 7 and (substring_3 in string) == True:
        in_bulb_start_2_wd = 10
        if (substring_4 in string) != True:
            in_bulb_end_2_wd = 12
        elif (substring_5 in string) != True:
            in_bulb_end_2_wd = 18
        elif (substring_6 in string) != True:
            in_bulb_end_2_wd = 22
        else:
            in_bulb_end_2_wd = 24
elif in_bulb_end_1_wd == 10 and (substring_4 in string) == True:
        in_bulb_start_2_wd = 12
        if (substring_5 in string) != True:
            in_bulb_end_2_wd = 18
        elif (substring_6 in string) != True:
            in_bulb_end_2_wd = 22
        else:
            in_bulb_end_2_wd = 24
elif in_bulb_end_1_wd == 12 and (substring_5 in string) == True:
        in_bulb_start_2_wd = 18
        if (substring_6 in string) != True:
            in_bulb_end_2_wd = 22
        else:
            in_bulb_end_2_wd = 24
elif in_bulb_end_1_wd == 18 and (substring_6 in string) == True:
        in_bulb_start_2_wd = 22
        in_bulb_end_2_wd = 24
else:
    in_bulb_start_2_wd = 0
    in_bulb_end_2_wd = 0

#time window_3
if in_bulb_end_2_wd < 18 and in_bulb_end_2_wd > 0 and (substring_5 in string) == True:
        in_bulb_start_3_wd = 18
        if (substring_6 in string) != True:
            in_bulb_end_3_wd = 22
        else:
            in_bulb_end_3_wd = 24
elif in_bulb_end_2_wd == 18 and (substring_6 in string) == True:
        in_bulb_start_3_wd = 22
        in_bulb_end_3_wd = 24
else:
    in_bulb_start_3_wd = 0
    in_bulb_end_3_wd = 0
    
    
print("start_1 = ", in_bulb_start_1_wd)
print("end_1 = ", in_bulb_end_1_wd)
print("start_2 = ",in_bulb_start_2_wd)
print("end_2 = ",in_bulb_end_2_wd)
print("start_3 = ",in_bulb_start_3_wd)
print("end_3 = ",in_bulb_end_3_wd)
'''

for x in substrings:
    if (x in substrings) == True:
        if x == substrings[0]:
            start_1 = 0
        elif x == substrings[1]
            start_1 = 7
        elif x == substrings[2]
            start_1 = 10
        elif x == substrings[3]
            start_1 = 12
        elif x == substrings[4]
            start_1 = 18
print(start_1)
