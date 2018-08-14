import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

import statsmodels.tsa.arima_model as arima
import statsmodels.api as sm

def main():
    df = pd.read_csv('data_weather copy.csv', index_col='Time', parse_dates=True)

    grouped.plot(figsize=(16,8), xlim=('2010-07-30', '2011-07-30'))
    fig = plt.figure(figsize=(16,8))
    ax1 = fig.add_subplot(211)
    acf = sm.graphics.tsa.plot_acf(grouped['mean'].values, lags=30, ax=ax1)
    arma = arima.ARMA(grouped['mean'], (4,1), dates=grouped.index).fit()

if __name__ == "__main__":
    main()