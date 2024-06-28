import json

from preprocessing.kobo_api_access import load_kobo_data

results = load_kobo_data(form_id="a96v2rKzMbNRkxiiHKAU9b")

first_survey = results[0][4]

with open("first_survey.json", "w") as file:
    json.dump(first_survey, file)

