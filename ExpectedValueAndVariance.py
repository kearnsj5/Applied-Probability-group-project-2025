"""

Question 2: - Expected value and variance 
"Let X be the random variable for the number of available bikes at that same station. How do its Expected Value 
(E[X]) and Variance (Var(X)) compare between the 'morning peak' and the 'midday' (e.g., 1:00-2:30 PM)?"
Course Area: This directly uses Discrete Random Variables from Slides_part3.pdf.

"""

import csv
import matplotlib.pyplot as plt
from datetime import datetime


print("Analyzing bike availability at residential stations during morning peak...")

# RESIDENTIAL STATIONS  :
# I used the same stations that were in MY FILE (test.py) 
# We can change these as needed.
residential_stations = {
    "BLESSINGTON STREET",
    "CHARLEVILLE ROAD",
    "AVONDALE ROAD",
    "PHIBSBOROUGH ROAD",
    "MOUNTJOY SQUARE EAST",
    "NORTH CIRCULAR ROAD (O'CONNELL'S)",
    "BROADSTONE",
    "FENIAN STREET",
    "CABRA ROAD",
    # "BROOKFIELD ROAD",
    # "ROTHE ABBEY",
    # "GOLDEN LANE",
    # "DEVERELL PLACE",
    # "PARKGATE STREE",
}


with open('pythonPorjects/dublin-bikes.csv', 'r') as f:
    reader = csv.reader(f)
    header = next(reader)
    data = list(reader)

print(f"Total records: {len(data)}")


morning_peak_observations = []
midday_observations = []


for row in data:
    timestamp_str = row[1]
    station_name = row[8]
    num_bikes = int(row[3])
    
    timestamp = datetime.strptime(timestamp_str, "%Y-%m-%d %H:%M:%S")
    hour = timestamp.hour
    
    is_residential = station_name in residential_stations
    
    if is_residential:
        # MORNING
        if hour == 6 or hour == 8:
            morning_peak_observations.append(num_bikes)
        
        # MID DAY
        elif hour == 13 or (hour == 16):
            midday_observations.append(num_bikes)

# only bit of code that is diff to my test.py file really.

# Calculate Expected Value and Variance for morning peak
if len(morning_peak_observations) > 0:
    n_morning = len(morning_peak_observations)
    mean_morning = sum(morning_peak_observations) / n_morning
    
    # Variance: E[X^2] - (E[X])^2
    sum_squares_morning = sum(x**2 for x in morning_peak_observations)
    variance_morning = (sum_squares_morning / n_morning) - (mean_morning ** 2)
    
    print("\n ------- morning ----------")
    print(f"Total observations: {n_morning}")
    print(f"Expected Value E[X]: {mean_morning:.2f} bikes")
    print(f"Variance Var(X): {variance_morning:.2f}")
print("-------------------------------------------------")

if len(midday_observations) > 0:
    n_midday = len(midday_observations)
    mean_midday = sum(midday_observations) / n_midday
    
    sum_squares_midday = sum(x**2 for x in midday_observations)
    variance_midday = (sum_squares_midday / n_midday) - (mean_midday ** 2)
    
    print("\n --------- MIDDAY ---------")
    print(f"Total observations: {n_midday}")
    print(f"Expected Value E[X]: {mean_midday:.2f} bikes")
    print(f"Variance Var(X): {variance_midday:.2f}")
    print("-------------------------------------------------")

