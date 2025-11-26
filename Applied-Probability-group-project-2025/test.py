import csv
import matplotlib.pyplot as plt
from datetime import datetime




print("Analyzing bike availability at residential stations during morning peak...")




# could filter these names further maybe we only want one or two?
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


commercial_station = {


   "City Quay",
   "Mater Hospital",
   "Georges Quay",
   "Pearse Street",


}




with open('pythonPorjects/dublin-bikes.csv', 'r') as f:
   reader = csv.reader(f)
   header = next(reader)  # Skip header
   data = list(reader)


print(f"Total records: {len(data)}")




# stored here
morning_peak_residential_observations = []


for row in data:
   timestamp_str = row[1]  # "last_reported" column
   station_name = row[8]   # "name" column
   num_bikes = int(row[3]) # "num_bikes_available" column
  
  
   # Parse timestamp
   timestamp = datetime.strptime(timestamp_str, "%Y-%m-%d %H:%M:%S")
   hour = timestamp.hour
   minute = timestamp.minute
  
  
   is_morning_peak = (hour == 7) or (hour == 9)
  
  
   is_residential = station_name in residential_stations
  
   if (is_morning_peak and is_residential) :
       morning_peak_residential_observations.append({
           'station': station_name,
           'time': timestamp,
           'bikes_available': num_bikes,
           'has_bikes': num_bikes > 0
       })


# Calculate probability
total_observations = len(morning_peak_residential_observations)
bikes_available_count = sum(1 for obs in morning_peak_residential_observations if obs['has_bikes'])


if total_observations > 0:
   probability = bikes_available_count / total_observations
  
  
   print("RESULTS: Morning Peak (7 and 9 am ) at Residential Stations")
  
   print(f"Total observations: {total_observations}")
   print(f"Times with bikes available: {bikes_available_count}")
   print(f"Times with NO bikes: {total_observations - bikes_available_count}")
   print(f"\nProbability of finding an available bike: {probability:.2%}")
  


else:
   print("No observations found for residential stations during morning peak hours.")




# Visulaziation:
if total_observations > 0:
   prob_bike = probability
   prob_no_bike = 1 - probability


   labels = ["Bike Available", "No Bike Available"]
   values = [prob_bike, prob_no_bike]


   plt.figure(figsize=(7,5))
   plt.bar(labels, values)
   plt.ylim(0, 1)
   plt.ylabel("Probability")
   plt.title("Finding a Bike at a Residential Station Given It is Morning Peak")
   plt.tight_layout()
   plt.show()
else:
   print("No observations available to plot probabilities.")

