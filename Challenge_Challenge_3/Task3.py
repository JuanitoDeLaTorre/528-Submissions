import csv
import itertools


dates = []
year = []
month = []
values = []
spring = [3,4,5]
summer = [6,7,8]
fall = [9,10,11]
winter = [12,1,2]
seasons = [spring, summer, fall, winter]
seasonsStr = ["Spring","Summer","Fall","Winter"]

csvFile = open('co2-ppm-daily.csv')

csvreader = csv.reader(csvFile)

#append the two columns in csvFile to dates and values lists
for line in csvreader:
    dates.append(line[0])
    values.append(line[1])

#remove column names
dates.pop(0)
values.pop(0)

#split the dates into year and month (don't need day)
for i in dates:
    line = i.split('-')
    year.append(line[0])
    month.append(line[1])

#cast all month values to int
for i in range(len(month)):
    month[i] = int(month[i])

#get yearly averages by looping through years list and finding associated values
sum = 0
count = 0
yearsList = []
avgList = []
#loop through all available years
for k in range(int(min(year)),int(max(year))+1):
    yearsList.append(k)
    sum,count = 0,0

    #if the year in the list matches the year in the parent for loop, add the associated value to the running sum
    #then add the average to an averageList
    for i,j in zip(year,range(len(year))):
        if i == str(k):
            sum += float(values[j])
            count += 1
    avgList.append(sum/count)

print("~~~~~~~ Yearly Averages ~~~~~~~~\n")
for i,j in zip(yearsList,avgList):
    print(str(i) + ": " + str(j))

#seasonal average value calculation

monthlyAvg_Values = []
monthlyCount = []
sumSzn = 0.0
countSzn = 0

#months in order of seasons list (starting with spring)
m = [3,4,5,6,7,8,9,10,11,12,1,2]

#basically the same double for loop as for the years
for months in m:
    sumSzn = 0.0
    countSzn = 0
    for i, j in zip(month, range(len(month))):
        if i == months:
            sumSzn += float(values[j])
            countSzn += 1
    monthlyAvg_Values.append(sumSzn)
    monthlyCount.append(countSzn)

sznSum = 0.0
sznAve = 0.0
sznCount = 0

print("\n~~~~~~~ Seasonal Averages ~~~~~~~~\n")
for szn,sznStr in zip(seasons,seasonsStr):
    sznSum = 0.0
    sznAve = 0.0
    sznCount = 0
    for month in szn:
        #important to distinguish between index and month
        month = month - 1
        sznSum += monthlyAvg_Values[month]
        sznCount += monthlyCount[month]
    sznAve = sznSum / sznCount

    print(sznStr + " average: " + str(sznAve))

#get total for entire dataset
sumTotal = 0.0
for i in values:
    sumTotal += float(i)
averageTotal = sumTotal/len(values)

anomaly = []
for i in values:
    anomaly.append(float(i)-averageTotal)

print("\n~~~~~~~~ Entire Dataset Stats ~~~~~~~~\n")

print("The minimum for the entire dataset is: " + str(min(values)))
print("The maximum for the entire dataset is: " + str(max(values)))
print("The average for the entire dataset is: " + str(averageTotal))

check = input("\nCheck anomalies for all values? (Y/N): ")
if check == 'Y':
    print("Following are anomalies for each value:")
    for i, j in zip(anomaly, range(len(anomaly))):
        print(str(j + 1) + ": " + str(i))






