import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

import statsmodels.tsa.arima_model as arima
import statsmodels.api as sm

def main():
    pass

if __name__ == "__main__":
    main()

df = pd.read_csv('data_weather copy.csv', index_col='Time', parse_dates=True)

df.drop(labels=['index'], axis=1, inplace=True)
df.head()

grouped = df.groupby(pd.TimeGrouper('D'))['TemperatureF'].agg(['min', 'max', 'mean'])
grouped.head()

grouped['min'].fillna((grouped['min'].mean()), inplace=True)
grouped['max'].fillna((grouped['max'].mean()), inplace=True)
grouped['mean'].fillna((grouped['mean'].mean()), inplace=True)

grouped.head()

grouped['min'] = grouped['min'].apply(lambda x: grouped['min'].mean() if x < 0 else x)
grouped['max'] = grouped['max'].apply(lambda x: grouped['max'].mean() if x < 0 else x)
grouped['mean'] = grouped['mean'].apply(lambda x: grouped['mean'].mean() if x < 12.46 else x)

for index, row in grouped.iterrows():
    if row['mean'] < 20:
        print(index, row['min'], row['max'], row['mean'])
    if row['max'] > 100:
        print(index, row['min'], row['max'], row['mean'])

grouped.head()

grouped.plot(figsize=(16,8), xlim=('2010-07-30', '2011-07-30'))
fig = plt.figure(figsize=(16,8))
ax1 = fig.add_subplot(211)
acf = sm.graphics.tsa.plot_acf(grouped['mean'].values, lags=30, ax=ax1)
arma = arima.ARMA(grouped['mean'], (4,1), dates=grouped.index).fit()