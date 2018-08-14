import pandas as pd


def test_legitimacy(grouped):
    """
    Check if the max is higher than 100˚F for any given day.
    There are three situations where it is:

    Time                min  max   mean
    2011-05-04 00:00:00 53.6 101.8 68.46319444444441
    2017-09-01 00:00:00 66.6 107.5 84.26629629629628
    2017-09-02 00:00:00 73.4 104.4 86.59037037037035

    After looking up the dates, we can confirm data legitimacy.
    This is due to news stories that came out during these days citing high temperatures.
    """
    for index, row in grouped.iterrows():
        if row["max"] > 100:
            print(index, row["min"], row["max"], row["mean"])


def fill_nans(grouped):
    grouped.fillna(method="ffill", inplace=True)
    return grouped


def make_negatives_nans(grouped):
    grouped["min"] = grouped["min"].apply(lambda x: float("nan") if x < 0 else x)
    grouped["max"] = grouped["max"].apply(lambda x: float("nan") if x < 0 else x)
    grouped["mean"] = grouped["mean"].apply(lambda x: float("nan") if x < 12.46 else x)
    return grouped


def group_data(df):
    grouped = df.groupby(pd.Grouper(freq="D"))["TemperatureF"].agg(
        ["min", "max", "mean"]
    )
    return grouped


def process_data(df):
    grouped = group_data(df)
    grouped = make_negatives_nans(grouped)
    grouped = fill_nans(grouped)
    return grouped


def main():
    df = pd.read_csv("temp_data_raw.csv", index_col="Time", parse_dates=True)
    df.drop(df.columns[df.columns.str.contains("Unnamed")], axis=1, inplace=True)

    grouped = process_data(df)

    test_legitimacy(grouped)

    grouped.to_csv("temp_data_cleaned.csv")


if __name__ == "__main__":
    main()
