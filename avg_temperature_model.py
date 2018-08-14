import pandas as pd
import matplotlib.pyplot as plt
import matplotlib
import statsmodels.api as sm
import statsmodels.tsa.arima_model as arima

def initial_plot(df):
    plt.plot(df['mean'], color='#3D9970', linewidth=0.5)
    plt.title('Mean Temperature in Fahrenheit from 2010-2018')
    plt.xlabel('Time (Days)')
    plt.ylabel('Mean Temperature (˚F)')
    plt.savefig('plots/initial_plot.svg', dpi=200)
    plt.savefig('plots/initial_plot.png', dpi=200)

def stuff():
    # df.plot(figsize=(16,8), xlim=('2010-07-30', '2011-07-30'))
    # fig = plt.figure(figsize=(16,8))
    # ax1 = fig.add_subplot(211)
    # acf = sm.graphics.tsa.plot_acf(df['mean'].values, lags=30, ax=ax1)
    # arma = arima.ARMA(df['mean'], (4,1), dates=df.index).fit()
    pass

def main():
    df = pd.read_csv('temp_data_cleaned.csv', index_col='Time', parse_dates=True)

    initial_plot(df)

if __name__ == "__main__":
    main()