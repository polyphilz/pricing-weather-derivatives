import sys
import pandas as pd
from pandas.tseries.offsets import DateOffset
import matplotlib.pyplot as plt
import matplotlib
import statsmodels.api as sm
from statsmodels.tsa.stattools import adfuller
from statsmodels.graphics.tsaplots import plot_acf, plot_pacf


def initial_plot(df):
    initial_plot = plt.figure(num=1, figsize=(12, 6))
    plt.plot(df["mean"], color="#3D9970", linewidth=0.5, figure=initial_plot)
    plt.title("Mean Temperature in Fahrenheit from 2010-2018", figure=initial_plot)
    plt.xlabel("Time", figure=initial_plot)
    plt.ylabel("Mean Temperature (˚F)", figure=initial_plot)
    plt.savefig("plots/initial_plot.svg", dpi=200, figure=initial_plot)
    plt.savefig("plots/initial_plot.png", dpi=200, figure=initial_plot)


def acf_pacf_plot(df):
    acf_pacf_plot = plt.figure(figsize=(12, 6))
    ax1 = acf_pacf_plot.add_subplot(211)
    acf_pacf_plot = plot_acf(df["mean"].dropna(), lags=30, color="#3D9970", ax=ax1)
    ax2 = acf_pacf_plot.add_subplot(212)
    acf_pacf_plot = plot_pacf(df["mean"].dropna(), lags=30, color="#3D9970", ax=ax2)
    plt.savefig("plots/sfd_acf_pacf.svg", dpi=200, figure=acf_pacf_plot)
    plt.savefig("plots/sfd_acf_pacf.png", dpi=200, figure=acf_pacf_plot)


def stationarity_check(df):
    """
    Checks Dickey-Fuller test for raw mean data as well as seasonal first difference.
    Appends new 'Seasonal First Difference' info. as a column to original DataFrame and returns it.
    """

    def adf_check(time_series):
        """
        Input: Time series data in the form of a pandas Series
        Output: Augmented Dickey-Fuller Unit Root Test report
        """
        result = adfuller(time_series)
        print()
        print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
        print("Augmented Dickey-Fuller Unit Root Test:")
        labels = [
            "ADF Test Statistic",
            "p-value",
            "#Lags Used",
            "Number of Observations Used",
        ]

        for value, label in zip(result, labels):
            print(label + " : " + str(value))

        if result[1] <= 0.05:
            print(
                "Strong evidence against the null hypothesis - reject the null hypothesis. Data has no unit root and is stationary."
            )
        else:
            print(
                "Weak evidence against null hypothesis - do not reject the null hypothesis. Data has a unit root and is non-stationary."
            )
        print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
        print()

    adf_check(df["mean"])
    df["Temp. First Difference"] = df["mean"] - df["mean"].shift(1)
    df["Seasonal Difference"] = df["mean"] - df["mean"].shift(365)
    df["Seasonal First Difference"] = df["Temp. First Difference"] - df[
        "Temp. First Difference"
    ].shift(365)
    adf_check(df["Seasonal First Difference"].dropna())

    return df


def model(df):
    model = sm.tsa.statespace.SARIMAX(
        df["mean"], order=(1, 1, 2), seasonal_order=(0, 1, 0, 365)
    )
    results = model.fit()
    print(results.summary())
    return results


def resids_plot(results):
    resids_plot1 = plt.figure(figsize=(12, 6))
    plt.plot(results.resid, color="#3D9970", linewidth=0.5, figure=resids_plot1)
    plt.title("Residuals", figure=resids_plot1)
    plt.xlabel("Time", figure=resids_plot1)
    plt.ylabel("Residual", figure=resids_plot1)
    plt.savefig("plots/resids_plot1.png", dpi=200, figure=resids_plot1)
    plt.savefig("plots/resids_plot1.svg", dpi=200, figure=resids_plot1)

    resids_plot2 = plt.figure(figsize=(12, 6))
    ax = resids_plot2.add_subplot(111)
    plt.title("Residuals (Kernel Density Estimation)", figure=resids_plot2)
    plt.xlabel("Time", figure=resids_plot2)
    results.resid.plot(kind="kde", color="#3D9970", linewidth=0.5, ax=ax)
    resids_plot2.savefig("plots/resids_plot2.png", dpi=200)
    resids_plot2.savefig("plots/resids_plot2.svg", dpi=200)


def validate_model(df, results):
    past_days = 50

    df["forecast"] = results.predict(start=len(df) - past_days, end=len(df), dynamic=True)

    predict_existing_values_plot = plt.figure(figsize=(12, 6))
    ax = predict_existing_values_plot.add_subplot(111)
    plt.title(
        f"Forecast of Temperature For Past {str(past_days)} Days", figure=predict_existing_values_plot
    )
    plt.xlabel("Time", figure=predict_existing_values_plot)
    plt.ylabel("Mean Temperature (˚F)", figure=predict_existing_values_plot)
    df[["mean", "forecast"]].plot(color=["#3D9970", "#ff6666"], linewidth=0.5, ax=ax)
    predict_existing_values_plot.savefig(
        "plots/predict_existing_values_plot.png", dpi=200
    )
    predict_existing_values_plot.savefig(
        "plots/predict_existing_values_plot.svg", dpi=200
    )


def forecast(df, results):
    future_days = 50

    future_dates = [df.index[-1] + DateOffset(days=x) for x in range(0, future_days)]
    future_dates_df = pd.DataFrame(index=future_dates[1:], columns=df.columns)
    future_df = pd.concat([df, future_dates_df])

    future_df["forecast"] = results.predict(
        start=len(df), end=len(future_df), dynamic=True
    )

    predict_unknown_values_plot = plt.figure(figsize=(12, 6))
    ax = predict_unknown_values_plot.add_subplot(111)
    plt.title(
        f"Forecast of Temperature For Next {future_days} Days", figure=predict_unknown_values_plot
    )
    plt.xlabel("Time", figure=predict_unknown_values_plot)
    plt.ylabel("Mean Temperature (˚F)", figure=predict_unknown_values_plot)
    future_df[["mean", "forecast"]].plot(
        color=["#3D9970", "#ff6666"], linewidth=0.5, ax=ax
    )
    predict_unknown_values_plot.savefig(
        "plots/predict_unknown_values_plot.png", dpi=200
    )
    predict_unknown_values_plot.savefig(
        "plots/predict_unknown_values_plot.svg", dpi=200
    )


def main():
    # Loading the dataset
    try:
        df = pd.read_csv("temp_data_cleaned.csv", index_col="Time", parse_dates=True)
    except:
        print(
            "Please run `scrape_data.py` and `clean_data.py` in that order to generate the necessary data first."
        )
        sys.exit(0)

    # Initial plot / lay of the land to see what we're dealing with
    initial_plot(df)

    # ARIMA
    df = stationarity_check(df)
    acf_pacf_plot(df)
    results = model(df)
    resids_plot(results)

    # Forecasting
    validate_model(df, results)
    forecast(df, results)

    # Completion
    print("~ COMPLETION ~")
    print("All plots saved to `plots` folder")


if __name__ == "__main__":
    main()
