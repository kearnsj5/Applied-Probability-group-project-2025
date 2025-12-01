import os
import csv
import matplotlib.pyplot as plt
from datetime import datetime

print("Analyzing bike availability during morning peak (07:00–09:30)...")

# Define residential and commercial stations

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
}

commercial_stations = {
    "D'OLIER STREET",
    "ST. STEPHEN'S GREEN",
    "GEORGES QUAY",
    "GRAFTON STREET",
    "PEARSE STREET",
    "CUSTOM HOUSE",
    "TRINITY COLLEGE",
    "HATCH STREET",
    "HIGH STREET"
}

# Load data from CSV
# Build path to bikes.csv in the same folder as this script

script_dir = os.path.dirname(os.path.abspath(__file__))
csv_path = os.path.join(script_dir, 'bikes.csv')

print("Using CSV file:", csv_path)

with open(csv_path, 'r') as f:
    reader = csv.reader(f)
    header = next(reader)
    data = list(reader)

# Collect observations during the morning peak
residential_morning = []      # X | R
non_residential_morning = []  # X | C

for row in data:
    timestamp_str = row[1]
    station_name = row[8]
    num_bikes = int(row[3])

    # Parse timestamp
    timestamp = datetime.strptime(timestamp_str, "%Y-%m-%d %H:%M:%S")
    hour = timestamp.hour
    minute = timestamp.minute

    # Check if in morning peak: 07:00–09:30
    in_morning_peak = (
        (hour == 7) or
        (hour == 8) or
        (hour == 9 and minute <= 30)
    )

    if not in_morning_peak:
        continue

    # Residential or commercial?
    is_residential = station_name in residential_stations
    is_commercial = station_name in commercial_stations

    if is_residential:
        residential_morning.append(num_bikes)      # X | R
    elif is_commercial:
        non_residential_morning.append(num_bikes)  # X | C
    # else: ignore stations not in either list

print(f"Residential morning observations: {len(residential_morning)}")
print(f"Non-residential morning observations: {len(non_residential_morning)}")

#  functions for E[X] and Var(X)
def mean(values):
    if not values:
        return float('nan')
    return sum(values) / len(values)

def variance(values):
    if not values:
        return float('nan')
    n = len(values)
    sum_x = sum(values)
    sum_x2 = sum(x**2 for x in values)
    return (sum_x2 / n) - (sum_x / n) ** 2

# Compute E[X|R], Var(X|R], E[X|C], Var(X|C]
print("\n===== Morning Peak Results (07:00–09:30) =====")

if residential_morning:
    E_R = mean(residential_morning)
    Var_R = variance(residential_morning)
    print("\nResidential Stations (R)")
    print(f"Total observations: {len(residential_morning)}")
    print(f"E[X | R]       = {E_R:.2f} bikes")
    print(f"Var(X | R)     = {Var_R:.2f}")
else:
    print("\nNo residential morning data found.")

if non_residential_morning:
    E_C = mean(non_residential_morning)
    Var_C = variance(non_residential_morning)
    print("\nNon-Residential Stations (C)")
    print(f"Total observations: {len(non_residential_morning)}")
    print(f"E[X | C]       = {E_C:.2f} bikes")
    print(f"Var(X | C)     = {Var_C:.2f}")
else:
    print("\nNo non-residential morning data found.")

print("===============================================")

#  Boxplot: Residential vs Non-Residential during morning peak
plt.figure(figsize=(8, 5))
box = plt.boxplot(
    [residential_morning, non_residential_morning],
    labels=["Residential (R)", "Non-Residential (C)"],
    patch_artist=True,
    notch=True,
    showfliers=False,
    widths=0.5
)

# Colour the boxes
colors = ["#1f77b4", "#ff7f0e"]
for patch, color in zip(box['boxes'], colors):
    patch.set_facecolor(color)
    patch.set_alpha(0.4)
    patch.set_edgecolor("black")
    patch.set_linewidth(1.2)

# Style whiskers & caps
for whisker in box['whiskers']:
    whisker.set(color="black", linewidth=1.2)
for cap in box['caps']:
    cap.set(color="black", linewidth=1.2)

# Style medians
for median in box['medians']:
    median.set(color="black", linewidth=2)

plt.ylabel("Available Bikes", fontsize=12)
plt.title("Bike Availability at Morning Peak\nResidential vs Non-Residential Stations", fontsize=14)
plt.grid(axis='y', linestyle='--', alpha=0.4)
plt.tight_layout()
plt.show()

#   Bar chart of expected values: E[X|R] vs E[X|C]
plt.figure(figsize=(7, 5))
bars = plt.bar(
    ["Residential (R)", "Non-Residential (C)"],
    [E_R, E_C],
    color=["#1f77b4", "#ff7f0e"],
    edgecolor="black",
    linewidth=1.2
)

plt.ylabel("Expected Value E[X]", fontsize=12)
plt.title("Expected Bike Availability at Morning Peak\nE[X | R] vs E[X | C]", fontsize=14)

# Add grid
plt.grid(axis='y', linestyle='--', alpha=0.4)

# Y-axis ticks (small interval)
plt.yticks(range(0, int(max(E_R, E_C)) + 5, 1))

# Add value labels on top of bars
for bar in bars:
    height = bar.get_height()
    plt.text(
        bar.get_x() + bar.get_width()/2,
        height + 0.2,
        f"{height:.1f}",
        ha='center', va='bottom', fontsize=11
    )

plt.tight_layout()
plt.show()
