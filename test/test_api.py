import datetime
import pandas as pd
from src.api.open_weather import get_weather_forecast  # replace with the actual module name


def test_get_weather_forecast():
    latitude = 40.7128  # New York City latitude
    longitude = -74.0060  # New York City longitude
    start_time = datetime.datetime.now().replace(minute=0, second=0, microsecond=0)
    end_time = start_time + datetime.timedelta(days=1)
    start_hour = start_time.strftime("%Y-%m-%dT%H:%M")
    end_hour = end_time.strftime("%Y-%m-%dT%H:%M")

    result_df = get_weather_forecast(latitude, longitude, start_hour, end_hour)

    # Check if the result is a DataFrame
    assert isinstance(result_df, pd.DataFrame), "The result should be a pandas DataFrame"

    # Check if the DataFrame has the expected columns
    expected_columns = ["timestamp", "temp_air", "wind_speed", "ghi", "dhi", "dni"]
    assert list(result_df.columns) == expected_columns, "DataFrame columns do not match expected columns"

    # Check if the DataFrame is not empty
    assert not result_df.empty, "The DataFrame should not be empty"

    # Check if the number of rows corresponds to the forecast period (e.g., 72 + 1 hours for 3 days)
    expected_row_count = 25
    assert len(result_df) == expected_row_count, f"The DataFrame should have {expected_row_count} rows, got {len(result_df)}"

