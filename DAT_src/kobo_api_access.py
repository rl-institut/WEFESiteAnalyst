#import your libraries
from koboextractor import KoboExtractor
import json
import pandas as pd

#access your kobo account using your token
your_token = 'ea290627972a055fd067e1efc02c803869b1747c' #Replace by your token
kobo = KoboExtractor(your_token, 'https://kobo.humanitarianresponse.info/api/v2', debug=True)

assets = kobo.list_assets()
asset_uid = assets['results'][0]['uid']

#access data submitted to a specific form using the form id
form_id = 'aM4SL2TkbkMbs2s3sXLFGm' #Replace by your Form ID
data = kobo.get_data(form_id, query=None, start=None, limit=None, submitted_after=None)
# data = kobo.get_data(form_id, query=None, start=None, limit=None, submitted_after='2020-05-20T17:29:30')

#convert your data from json to a pd dataframe
results_dict = data['results']
df = pd.json_normalize(data['results'])
# preview your data -- this step is not compulsory
df.head()