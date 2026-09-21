import sqlite3
import calendar

c = sqlite3.connect("data/nasa_asteroids.db")
#creating close approach table
with open("sql/schema.sql") as file:
    schema = file.read()
    c.executescript(schema)
    c.commit()
    c.close()

#function for inserting events from panda df to sqlite db
def insert_events(df):
    copy = df.copy()
    #need to convert pandas Timestamp to text in correct format
    copy["close_approach_date"] = (copy["close_approach_date"].dt.strftime("%Y-%m-%d"))
    copy["close_approach_date_full"] = (copy["close_approach_date_full"].dt.strftime("%Y-%m-%d %H:%M"))
    #extracts column values for each row into a tuple (requires df order = schema order)
    data = copy.itertuples(index=False, name=None)
    with sqlite3.connect("data/nasa_asteroids.db") as c:
        c.executemany("""
            INSERT OR IGNORE INTO close_approaches (
                event_id, 
                asteroid_id,
                name,
                absolute_magnitude_h,
                diameter_min_km,
                diameter_max_km,
                is_potentially_hazardous,
                is_sentry_object,
                close_approach_date,
                close_approach_date_full,
                relative_velocity_km_s,
                miss_distance_au,
                orbiting_body
            )
            VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?)
            """, data
        )
    
#function for getting month dates for automating data intake
def get_dates(month, year):
    start_date = f"{year:04d}-{month:02d}-01"
    final_day = calendar.monthrange(year, month)[1]
    end_date = f"{year:04d}-{month:02d}-{final_day:02d}"
    return start_date, end_date

#gets start/end dates for months in a time period
def get_period_dates(start_month, start_year, end_month, end_year):
    dates = []
    for year in range(start_year, end_year + 1):
        #if first yr, starts at start month, else jan
        if year == start_year:
            first_month = start_month
        else:
            first_month = 1
        #if last year, ends at end month else dec
        if year == end_year:
            last_month = end_month
        else:
            last_month = 12

        for month in range(first_month, last_month + 1):
            start_date, end_date = get_dates(month, year)
            dates.append((start_date, end_date))
    return dates
