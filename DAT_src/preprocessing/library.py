import json

from preprocessing.kobo_api_access import load_kobo_data

results = load_kobo_data(form_id="aFhz5xWryVk68Mn7y978hn")

first_survey = results[0][0]

with open("first_survey.json", "w") as file:
    json.dump(first_survey, file)

