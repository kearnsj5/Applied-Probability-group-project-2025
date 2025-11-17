import csv
import matplotlib.pyplot as plt
from datetime import datetime

print(
    "Analyzing bike availability at commercial stations (morning peak vs off-peak)..."
)

morning_peak_dict = {}
off_peak_dict = {}

# office-heavy stations
commercial_stations = {
    "BLESSINGTON STREET",
    "CHARLEVILLE ROAD",
    "AVONDALE ROAD",
    "PHIBSBOROUGH ROAD",
    "MOUNTJOY SQUARE EAST",
    "NORTH CIRCULAR ROAD (O'CONNELL'S)",
    "BROADSTONE",
    "FENIAN STREET",
    "CABRA ROAD",
}

with open('dublin-bikes.csv', 'r') as f:
    reader = csv.reader(f)
    header = next(reader)
    data = list(reader)

print(f"Total records: {len(data)}")

# lists for peak and off peak
morning_peak_obs = []  # rows from 08:00–09:30 at commercial stations
off_peak_obs = []  # rows from 13:00–14:30 at commercial stations

for row in data:
    timeStamp = row[1]
    stationName = row[8]
    numberOfBikes = int(row[3])

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
        'bikes_available': numberOfBikes,
        'no_bikes': (numberOfBikes == 0)  # is the staion full?
    }

    if is_morning_peak:
        morning_peak_dict[hour * 100 + minute] = morning_peak_dict.get(
            hour * 100 + minute, 0) + 1
        morning_peak_obs.append(obs)

    if is_off_peak:
        off_peak_dict[hour * 100 +
                      minute] = off_peak_dict.get(hour * 100 + minute, 0) + 1
        off_peak_obs.append(obs)


# function to compute probability
def probability_no_bikes(observations):
    total = len(observations)
    if total == 0:
        return None  # avoid dividing by zero
    no_bikes_count = sum(1 for obs in observations if obs['no_bikes'])
    probability = no_bikes_count / total
    return probability, no_bikes_count, total


# 7. Compute probabilities for morning peak and off-peak
result_morning = probability_no_bikes(morning_peak_obs)
result_offpeak = probability_no_bikes(off_peak_obs)

print("\nRESULTS: Probability of NO bikes available at commercial stations")
print("-----------------------------------------------------------------")

if result_morning is not None:
    probabilityMorning, noBikesMorning, totalMorning = result_morning
    print("\nMorning Peak (08:00–09:30)")
    print(f"Total observations: {totalMorning}")
    print(f"Times with NO bikes (station full): {noBikesMorning}")
    print(
        f"P(B | M) = Probability of NO bikes in morning peak: {probabilityMorning:.2%}"
    )
else:
    print("\nMorning Peak: No observations found.")

if result_offpeak is not None:
    probabilityOffPeak, noBikesOffPeak, totalOffPeak = result_offpeak
    print("\nOff-Peak (13:00–14:30)")
    print(f"Total observations: {totalOffPeak}")
    print(f"Times with NO bikes (station full): {noBikesOffPeak}")
    print(
        f"P(B | O) = Probability of NO bikes in off-peak: {probabilityOffPeak:.2%}"
    )
else:
    print("\nOff-Peak: No observations found.")

for key in morning_peak_dict:
    print(f"{key}: {morning_peak_dict[key]}")

for key in off_peak_dict:
    print(f"{key}: {off_peak_dict[key]}")

morningkeys = list(morning_peak_dict.keys())
morningvalues = list(morning_peak_dict.values())

x = range(len(morningkeys))

fig, ax = plt.subplots()
ax.plot(x, morningvalues)

# make nice time labels like "08:00", "08:05", ...
labels = [f"{k // 100:02d}:{k % 100:02d}" for k in morningkeys]
ax.set_xticks(x)
ax.set_xticklabels(labels, rotation=45)

ax.set_title('Morning Peak')
fig.tight_layout()
plt.savefig("morningPeak.png")
plt.close()

offkeys = list(off_peak_dict.keys())
offvalues = list(off_peak_dict.values())

x = range(len(offkeys))

fig, ax = plt.subplots()
ax.plot(x, offvalues)

# make nice time labels like "08:00", "08:05", ...
labels = [f"{k // 100:02d}:{k % 100:02d}" for k in offkeys]
ax.set_xticks(x)
ax.set_xticklabels(labels, rotation=45)

ax.set_title('Off Peak')
fig.tight_layout()
plt.savefig("offPeak.png")
plt.close()
