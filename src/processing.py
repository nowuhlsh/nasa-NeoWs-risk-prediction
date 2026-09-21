import pandas as pd

def standardise_asteroid_data(df):
    s_df = df.copy()
    #str to numeric
    s_df["relative_velocity_km_s"] = pd.to_numeric(s_df["relative_velocity_km_s"], errors = "coerce")
    s_df["miss_distance_au"] = pd.to_numeric(s_df["miss_distance_au"], errors = "coerce")
    #str to pd datetime 
    s_df["close_approach_date"] = pd.to_datetime(s_df["close_approach_date"], errors = "coerce")
    s_df["close_approach_date_full"] = pd.to_datetime(s_df["close_approach_date_full"], errors = "coerce")
    return s_df

def asteroid_data_report(df):
    #creates a report on data to validate before adding to db
    report = { 
        "No. of missing values": df.isna().sum(),
        "Negative relative velocity": (df["relative_velocity_km_s"] < 0).sum(),
        "Negative miss distance" : (df['miss_distance_au'] < 0).sum(),
        "Negative min. diameter": (df['diameter_min_km'] < 0).sum(),
        "Negative max. diameter": (df['diameter_max_km'] < 0).sum()
    }
    return report







