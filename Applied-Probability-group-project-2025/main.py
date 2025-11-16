import csv

print("Hello World")

bikes = open('dublin-bikes.csv', 'r')
bikefile_reader = csv.reader(bikes)
bikefile = list(bikefile_reader)

myList = []
passFirst = False

for row in bikefile:
  #print(row[8])
  if passFirst is False:
    myList.append(row)
    passFirst = True
  else:
    date = row[1]
    #print(date)
    newTime = date[11:16]
    #print(newTime)
    newww = newTime.replace(":", "")
    #print(newww + " after replace")
    newww = int(newww)

    if row[8] == "CLARENDON ROW" and newww >= 800 and newww <= 930:
      myList.append(row)
      myList[-1][1] = newww

    #print(newTime)

for  row in myList:
  print(row)
