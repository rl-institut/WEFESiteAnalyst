#%%
from kobo_api_access import load_kobo_data
import defaults
from copy import copy

# Load survey data from Kobo and get only dict (position 0)
survey_data = load_kobo_data("aCs4ygeFHN5jkb4endReWK")[0]

#%%
string = survey_data[0]['B_11/in_bulb_usage_wd']

usage_wd_dict = copy(defaults.usage_wd_defaults)

for window in usage_wd_dict:
    if window in string:
        usage_wd_dict[window] = True
    else:
        usage_wd_dict[window] = False

print(usage_wd_dict)