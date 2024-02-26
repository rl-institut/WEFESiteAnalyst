#import your libraries
from koboextractor import KoboExtractor
import json
import pandas as pd

def load_kobo_data(form_id, api_token="ea290627972a055fd067e1efc02c803869b1747c"):
    kobo_dict = None

    kobo = KoboExtractor(api_token, 'https://kobo.humanitarianresponse.info/api/v2', debug=True)

    #access data submitted to a specific form using the form id
    data = kobo.get_data(form_id, query=None, start=None, limit=None, submitted_after=None)

    results_dict = data['results']  # get dict of survey results
    df = pd.json_normalize(data['results'])  # get df of survey results

    return results_dict, df


