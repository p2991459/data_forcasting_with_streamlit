# Python
import pandas as pd
from prophet import Prophet

# Python
df = pd.read_csv('gitrepo/data/acm_car_inv_googletrends.csv')
print(df.head())

#applying model
m = Prophet()
m.fit(df)
future = m.make_future_dataframe(periods=365)
future.tail()
