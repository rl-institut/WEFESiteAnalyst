usage_wd_defaults = {
    '0-7' : None,
    '7-10' : None,
    '10-12' : None,
    '12-18' : None,
    '18-22' : None,
    '22-24' : None
}

months_present_defaults = {
    'January' : None,
    'February' : None,
    'March' : None,
    'April' : None,
    'May' : None,
    'June' : None,
    'July' : None,
    'August' : None,
    'September' : None,
    'October' : None,
    'November' : None,
    'December' : None
}

working_day_default = {
    'monday' : None,
    'tuesday' : None,
    'wednesday' : None,
    'thursday' : None,
    'friday' : None,
    'saturday' : None,
    'sunday' : None
}

months_defaults_1 = {
    '1' : None,
    '2' : None,
    '3' : None,
    '4' : None,
    '5' : None,
    '6' : None,
    '7' : None,
    '8' : None,
    '9' : None,
    '10' : None,
    '11' : None,
    '12' : None
}

months_defaults = {
    1 : None,
    2 : None,
    3 : None,
    4 : None,
    5 : None,
    6 : None,
    7 : None,
    8 : None,
    9 : None,
    10 : None,
    11 : None,
    12 : None
}

months_of_presence = {
    'January' : 1,
    'February' : 2,
    'March' : 3,
    'April' : 4,
    'May' : 5,
    'June' : 6,
    'July' : 7,
    'August' : 8,
    'September' : 9,
    'October' : 10,
    'November' : 11,
    'December' : 12
}

working_day = {
    'monday' : 0,
    'tuesday' : 1,
    'wednesday' : 2,
    'thursday' : 3,
    'friday' : 4,
    'saturday' : 5,
    'sunday' : 6
}

exc_rate = 0.05334           #$/ZAR exchange rate

large_buck = 10
medium_buck = 5
small_buck = 1

density_dict = {
    'g/biogas_density' : 0.0012,
    'h/biofuel_density' : 0.9,
    'i/kerosene_density' : 0.8,
    'j/LPG_density' : 0.55,
    'k/eth_alc_density' : 0.789
}

fuel_units_conversion = {"kilogram":1, "bag":None, "liter":None, "cylinder": None}
time_units_conversion = {"daily":1, "weekly":7, "monthly":30}


suffix = {"household": "_H","service": "_S","large_scale_farm": "_AP","business": "","local_aut": ""}
prefix = {"household":
            {
             "working_days": None,
             "cooking": "H_18", 
             "meal":"H_18l",
             "electric":"H_16",
             "drinking_water":"H_8",
             "service_water":
                 {
                 "animal_water":"H_11",
                 "irrigation_water":"H_10"
                 },
             "agro_machine": None
             },
          "service":
            {
             "working_days": "S_2",
             "cooking": "S_5",
             "meal": "S_5l",
             "electric": "S_3",
             "drinking_water": "S_4",
             "service_water": "S_4",
             "agro_machine":None
             },
          "large_scale_farm":
            {
             "working_days": "AP_2c",
             "cooking": "AP_9",  
             "meal": "AP_9l", 
             "electric": "AP_8", 
             "drinking_water": "AP_3",
             "service_water":
                 {  
                 "animal_water": "AP_6", 
                 "irrigation_water": "AP_5"
                 }, 
             "agro_machine": "AP_10"
             },
          "business":
            {
             "working_days": "B_2a",
             "cooking": "B_13",  
             "meal": "B_13_meal", 
             "electric": "B_11", 
             "drinking_water": "B_7",
             "service_water": "B_7",
             "agro_machine": "B_14"
             },
          "local_aut":
            {
             }
         }