import json

from DAT_src.kobo_api_access import load_kobo_data

results = load_kobo_data(form_id="aAiiN4e2fEgrATGr3D69iQ")

first_survey = results[0][1]

with open("first_survey.json", "w") as file:
    json.dump(first_survey, file)

