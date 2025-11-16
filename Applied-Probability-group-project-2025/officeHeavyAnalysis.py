import csv
from datetime import datetime

print("Analyzing dock availability at commercial stations (morning peak vs off-peak)...")

 # office-heavy stations
commercial_stations = {
    "CITY QUAY",
    "PEARSE STREET",
    "GEORGES QUAY",
   
}

with open('pythonPorjects/dublin-bikes.csv', 'r') as f:
    reader = csv.reader(f)
    header = next(reader)  
    data = list(reader)

print(f"Total records: {len(data)}")

# lists for peak and off peak 
morning_peak_obs = []   # rows from 08:00–09:30 at commercial stations
off_peak_obs = []       # rows from 13:00–14:30 at commercial stations

for row in data:
    timeStamp = row[1]   
    stationName  = row[8]   
    numberOfDocks = int(row[4])  

    # Only grab office heavy stations listed earlier
    if stationName not in commercial_stations:
        continue

    # make datetime objects 
    timestamp = datetime.strptime(timeStamp, "%Y-%m-%d %H:%M:%S")
    hour = timestamp.hour
    minute = timestamp.minute

    # morning peak: 08:00-9:30
    is_morning_peak = (hour == 8) or (hour == 9 and minute <= 30)

    # off-peak: 13:00–14:30
    is_off_peak = (hour == 13) or (hour == 14 and minute <= 30)

    # observation dictionary 
    obs = {
        'station': stationName,
        'time': timestamp,
        'docks_available': numberOfDocks,
        'no_docks': (numberOfDocks == 0)  # is the staion full?
    }

    if is_morning_peak:
        morning_peak_obs.append(obs)

    if is_off_peak:
        off_peak_obs.append(obs)

# function to compute probability 
def probability_no_docks(observations):
    total = len(observations)
    if total == 0:
        return None  # avoid dividing by zero
    no_docks_count = sum(1 for obs in observations if obs['no_docks'])
    probability = no_docks_count / total
    return probability, no_docks_count, total

# 7. Compute probabilities for morning peak and off-peak
result_morning = probability_no_docks(morning_peak_obs)
result_offpeak = probability_no_docks(off_peak_obs)

print("\nRESULTS: Probability of NO docks available at commercial stations")
print("-----------------------------------------------------------------")

if result_morning is not None:
    probabilityMorning, noDocksMorning, totalMorning = result_morning
    print("\nMorning Peak (08:00–09:30)")
    print(f"Total observations: {totalMorning}")
    print(f"Times with NO docks (station full): {noDocksMorning}")
    print(f"P(B | M) = Probability of NO docks in morning peak: {probabilityMorning:.2%}")
else:
    print("\nMorning Peak: No observations found.")

if result_offpeak is not None:
    probabilityOffPeak, noDocksOffPeak, totalOffPeak = result_offpeak
    print("\nOff-Peak (13:00–14:30)")
    print(f"Total observations: {totalOffPeak}")
    print(f"Times with NO docks (station full): {noDocksOffPeak}")
    print(f"P(B | O) = Probability of NO docks in off-peak: {probabilityOffPeak:.2%}")
else:
    print("\nOff-Peak: No observations found.")

