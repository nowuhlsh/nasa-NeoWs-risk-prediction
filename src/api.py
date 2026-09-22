from dotenv import load_dotenv
import os
import requests
import pandas as pd
from datetime import date, timedelta

load_dotenv()

#fetching API key
api_key = os.getenv("NASA_API_KEY")

if not api_key:
    raise ValueError("API key not found")

#NASA NeoWs API endpoint
url = "https://api.nasa.gov/neo/rest/v1/feed"

def fetch_dates_asteroids(date):
    params = {
        "start_date": date,
        "end_date": date,
        "api_key": api_key
        }

    #API request
    response = requests.get(
        url,
        params = params,
        timeout=30
    )

    #in case of error
    response.raise_for_status()

    #JSON to Python dict
    data = response.json()

    #handling missing days 
    if date in data["near_earth_objects"]:
        asteroids = data["near_earth_objects"][date]
    else:
        asteroids = []

    return asteroids

#function to extract data in nested JSON format into simple dict
def asteroid_data_extract(asteroids):
#1 asteroid can have many close approach events, want to extract all of them
    records = []
    for asteroid in asteroids:
        for approach in asteroid["close_approach_data"]:
            #keep certain features as documented in project notes
            record = {
                #adding unique key for each entry, so that SQL can handle dupes
                "event_id": f"{asteroid['id']}_{approach['close_approach_date_full']}",
                #asteroid specifics
                "asteroid_id": asteroid["id"],
                "name": asteroid["name"],
                "absolute_magnitude_h": asteroid["absolute_magnitude_h"],
                "diameter_min_km": 
                    asteroid["estimated_diameter"]["kilometers"]["estimated_diameter_min"]
                ,
                "diameter_max_km": 
                    asteroid["estimated_diameter"]["kilometers"]["estimated_diameter_max"],

                #NASA classifications
                "is_potentially_hazardous": asteroid["is_potentially_hazardous_asteroid"],
                "is_sentry_object": asteroid["is_sentry_object"],

                #close-approach info
                "close_approach_date": approach["close_approach_date"],
                "close_approach_date_full": approach["close_approach_date_full"],
                "relative_velocity_km_s": approach["relative_velocity"]["kilometers_per_second"],
                "miss_distance_au": approach["miss_distance"]["astronomical"],
                "orbiting_body": approach["orbiting_body"],
            }
            records.append(record)
    return records

#function to turn return records into panda DataFrame
def rec_to_df(records):
    df = pd.DataFrame(records)
    return df

#function to extract data over a time period, into a dataframe
def fetch_daterange_asteroids(start, end):
    all_records =[]
    current_date = date.fromisoformat(start)
    end_date = date.fromisoformat(end)

    #for progress markers
    total_days = (end_date - current_date).days + 1
    complete_days = 0
    empty_day_count = 0
    empty_days = []
    progress_markers = {25,50,75,100}

    while current_date <= end_date:
        date_string = current_date.isoformat()
        #on what day API req fails
        try:
            asteroids = fetch_dates_asteroids(date_string)
        except Exception as error:
            raise RuntimeError(
                f"API request failed for {date_string}"
            ) from error
        #want to be aware of days with no events: won't confuse them with missing data
        if asteroids == []:
            empty_day_count += 1
            empty_days.append(date_string)
        records = asteroid_data_extract(asteroids)
        all_records.extend(records)
        current_date += timedelta(days=1)
        #adding progress checker
        complete_days += 1
        percent = int((complete_days / total_days) * 100)
        for marker in progress_markers.copy():
            #once it crosses a marker, print marker and remove it. copy() ensures no errors whilst looping
            if percent >= marker:
                print(f"{marker}% complete...")
                progress_markers.remove(marker)
    print(f"{start} to {end}, Days processed: {complete_days} / {total_days}")
    return rec_to_df(all_records)
