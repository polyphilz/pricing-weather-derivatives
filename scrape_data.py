import io
import requests
import pandas as pd
from dateutil import parser, rrule
from datetime import datetime, time, date
import time


def getRainfallData(station, day, month, year):
    """
    Function to return a data frame of minute-level weather data for a single Wunderground PWS station.

    Args:
        station (string): Station code from the Wunderground website
        day (int): Day of month for which data is requested
        month (int): Month for which data is requested
        year (int): Year for which data is requested

    Returns:
        Pandas Dataframe with weather data for specified station and date.
    """

    url = (
        "http://www.wunderground.com/weatherstation/WXDailyHistory.asp?ID={station}&day={day}&month={month}&year={year}&graphspan=day&format=1"
    )
    full_url = url.format(station=station, day=day, month=month, year=year)

    # Request data from wunderground data
    response = requests.get(full_url)
    data = response.text
    # remove the excess <br> from the text data
    data = data.replace("<br>", "")

    # Convert to pandas dataframe (fails if issues with weather station)
    try:
        dataframe = pd.read_csv(io.StringIO(data), index_col=False)
        dataframe["station"] = station
    except Exception as e:
        print(
            "Issue with date: {}-{}-{} for station {}".format(day, month, year, station)
        )
        return None

    return dataframe


def main():
    # Generate a list of all of the dates we want data for
    start_date = "2010-07-30"
    end_date = "2018-07-30"
    start = parser.parse(start_date)
    end = parser.parse(end_date)
    dates = list(rrule.rrule(rrule.DAILY, dtstart=start, until=end))

    # Create a list of stations here to download data for
    stations = ["KCASANFR49"]
    # Set a backoff time in seconds if a request fails
    backoff_time = 10
    data = {}

    # Gather data for each station in turn and save to CSV.
    for station in stations:
        print("Working on {}".format(station))
        data[station] = []
        for date in dates:
            # Print period status update messages
            if date.day % 10 == 0:
                print("Working on date: {} for station {}".format(date, station))
            done = False
            while done == False:
                try:
                    weather_data = getRainfallData(
                        station, date.day, date.month, date.year
                    )
                    done = True
                except ConnectionError as e:
                    # May get rate limited by Wunderground.com, backoff if so.
                    print("Got connection error on {}".format(date))
                    print("Will retry in {} seconds".format(backoff_time))
                    time.sleep(10)
            # Add each processed date to the overall data
            data[station].append(weather_data)
        # Finally combine all of the individual days and output to CSV for analysis.
        pd.concat(data[station]).to_csv("data_weather.csv".format(station))


if __name__ == "__main__":
    main()
