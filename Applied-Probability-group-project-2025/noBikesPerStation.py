import csv
import matplotlib.pyplot as plt
from datetime import datetime

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

morning_dict = {}
allDay_dict = {}
m_s_d = {}
a_s_d = {}
newtenmin = True

with open('dublin-bikes.csv', 'r') as db:
  reader = csv.reader(db)
  header = next(reader)
  data = list(reader)

for row in data:
  timeStamp = row[1]
  stationName = row[8]
  numberOfBikes = int(row[3])

  if stationName not in commercial_stations:
    continue

  timestamp = datetime.strptime(timeStamp, "%Y-%m-%d %H:%M:%S")
  hour = timestamp.hour
  minute = timestamp.minute

  # morning: 08:00-9:35
  is_morning = (hour == 5) or (hour == 6) or (hour == 7) or (hour == 8) or (
      hour == 9) or (hour == 10) or (hour == 11) or (hour == 12
                                                     and minute <= 5)

  # afternnon: 13:00–14:35
  is_allDay = True  #(hour == 13) or (hour == 14 and minute <= 35)

  if minute % 10 != 0:
    newtenmin = True
  if newtenmin:
    if minute % 10 == 0:
      m_s_d.clear()
      a_s_d.clear()
      newtenmin = False

  if is_morning and numberOfBikes == 0:
    fixedminute = minute - (minute % 10)
    if (hour * 100 + fixedminute in m_s_d) and (stationName in m_s_d.get(
        hour * 100 + fixedminute, "")):
      pass
    elif (hour * 100 + fixedminute not in m_s_d):
      morning_dict[hour * 100 + fixedminute] = morning_dict.get(
          hour * 100 + fixedminute, 0) + 1
      m_s_d[hour * 100 + fixedminute] = [stationName]
    else:
      morning_dict[hour * 100 + fixedminute] = morning_dict.get(
          hour * 100 + fixedminute, 0) + 1
      m_s_d[hour * 100 + fixedminute].append(stationName)

  if is_allDay and numberOfBikes == 0:
    fixedminute = minute - (minute % 10)
    if (hour * 100 + fixedminute in a_s_d) and (stationName in a_s_d.get(
        hour * 100 + fixedminute, "")):
      pass
    elif (hour * 100 + fixedminute not in a_s_d):
      allDay_dict[hour * 100 + fixedminute] = allDay_dict.get(
          hour * 100 + fixedminute, 0) + 1
      a_s_d[hour * 100 + fixedminute] = [stationName]
    else:
      allDay_dict[hour * 100 + fixedminute] = allDay_dict.get(
          hour * 100 + fixedminute, 0) + 1
      a_s_d[hour * 100 + fixedminute].append(stationName)

morningkeys = []
morningvalues = []

for key in sorted(morning_dict):
  morningkeys.append(key)
  morningvalues.append(morning_dict[key])
  print(f"{key}: {morning_dict[key]}")

x = range(len(morningkeys))

fig, ax = plt.subplots()
ax.plot(x, morningvalues)

# show ticks every 30 minutes (00 and 30), but keep all data points
tick_positions = [i for i, k in enumerate(morningkeys) if k % 100 in (0, 30)]
tick_labels = [
    f"{k // 100:02d}:{k % 100:02d}" for k in morningkeys if k % 100 in (0, 30)
]

ax.set_xticks(tick_positions)
ax.set_xticklabels(tick_labels, rotation=45)

ax.set_title('Morning')
ax.set_xlabel('Time')
ax.set_ylabel('Number of empty commercial stations')

fig.tight_layout()
plt.savefig("Morning.png")
plt.close()

allDaykeys = []
allDayvalues = []

for key in sorted(allDay_dict):
  allDaykeys.append(key)
  allDayvalues.append(allDay_dict[key])
  print(f"{key}: {allDay_dict[key]}")

x = range(len(allDaykeys))

fig, ax = plt.subplots()
ax.plot(x, allDayvalues)

# ticks every hour (minutes == 00)
tick_positions = [i for i, k in enumerate(allDaykeys) if k % 100 == 0]
tick_labels = [
    f"{k // 100:02d}:{k % 100:02d}" for k in allDaykeys if k % 100 == 0
]

ax.set_xticks(tick_positions)
ax.set_xticklabels(tick_labels, rotation=45)

ax.set_title('All Day')
ax.set_xlabel('Time')
ax.set_ylabel('Number of empty commercial stations')

fig.tight_layout()
plt.savefig("allDay.png")
plt.close()
