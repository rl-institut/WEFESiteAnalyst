#%%
from helpers.plotting import plotly_high_res_df

import pandas as pd
import numpy as np
from datetime import datetime, timedelta

# Get the current date and time
date_today = datetime.now()

# Generate a range of dates at minute intervals for the next 7 days
days = pd.date_range(date_today, date_today + timedelta(7), freq='T')

# Generate random data for the 'test' column
np.random.seed(seed=1111)
data = np.random.randint(1, high=100, size=len(days))

# Create the DataFrame
df = pd.DataFrame({'test': days, 'col2': data})

# Set the datetime index
df = df.set_index('test')

# Print the resulting DataFrame
df_resampled = df.resample('h').mean()
