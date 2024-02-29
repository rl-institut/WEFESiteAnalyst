st = "B11/indoor_light_power"

app_name = st.replace("B11/","", 1).replace("_power", "", 1)

# Get the parameters


app_dict = {}
app_dict[app_name] = {
    "power": float(data['B11/'+app_name+"_power"]),
    "usage_wds": {
        '0-7': True,
        '7-10': False,
    }

}

