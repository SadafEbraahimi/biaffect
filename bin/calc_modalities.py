#Code for calculating BiAffect Sensor Modalities from Raw Data
#2019

import csv
import math


#############################################################################
#
# Load Data
#
#####################

accelerations = list(csv.reader(open("accelerations.csv", "r")))
gonogo = list(csv.reader(open("gonogo.csv", "r")))
keylogs = list(csv.reader(open("keylogsTimestamp.csv", "r")))
trailmaking = list(csv.reader(open("trailmaking.csv", "r")))


#############################################################################
#
# Useful Functions
#
#####################

def motion(readCSV):
    square = 0
    sum = 0
    for row in readCSV[1:]:
        for column in row:
            square += float(column)**2
        sum += math.sqrt(square)
        square = 0
    return sum/(len(readCSV)-1)


def avg_interkey_delay(readCSV):
    data = []
    diff = []
    sum = 0
    avr = 0
    for row in readCSV[1:]:
        data.append(row[5])
    for i in range(len(data) - 1):
        diff.append(float(data[i+1])-float(data[i]))
    for i in range(len(diff)):
        sum += float(diff[i])
    return sum/len(diff)


#Calculating rates
def rate(readCSV, value):
    count = 0

    #Backspace rate
    if value == 'backspace':
        attribute = 6

    #Autocorrect rate
    if value == 'autocorrection':
        attribute = 6

    #GoNoGo error rate
    if value == "False":
        attribute = 2

    #Trailmaking Taps error rate
    if value == "True":
        attribute = 0

    #Go thru each row of file
    for row in readCSV:
        if (row[attribute] == value):
            count += 1
    return count/(len(readCSV)-1) * 100                                                     #Rate is count of row with value, divided by total number of rows


#############################################################################
#
# Main Program
#
#####################

if __name__ == "__main__":                                                                  #!!!Eventually prob convert this to a function that can be imported and called

    #!!!The below commented out lines will eventually need to be replaced with some code
    #that slices out parts of each file into "moving windows" for analysis based on timestamp,
    #we will also then to setup a for loop

    '''accelerations = list(csv.reader(open("accelerations.csv", "r")))
    gonogo = list(csv.reader(open("gonogo.csv", "r")))
    keylogs = list(csv.reader(open("keylogsTimestamp.csv", "r")))
    trailmaking = list(csv.reader(open("trailmaking.csv", "r")))'''

    header = ["Number of keystrokes", "Number of accelerometer readings", "Motion", "Backspace rate",
              "Autocorrect rate", "GoNoGo error rate", "Trailmaking Taps error rate", "Average interkey delay"]
    analysisData = []

    #Number of keystrokes (prob the number of rows in keylog)
    analysisData.append(len(keylogs)-1)

    #Number of accelerometer readings
    analysisData.append(len(accelerations)-1)

    #motion (accelerometer displacement in absolute terms, i.e. square root of x^2+y^2+z^2)
    analysisData.append(motion(accelerations))

    #Backspace rate (% of backspace presses divided by total key presses)
    analysisData.append(rate(keylogs, 'backspace'))

    #Autocorrect rate
    analysisData.append(rate(keylogs, 'autocorrection'))

    #GoNoGo error rate (% of results_incorrect=True divided by total rows)
    analysisData.append(rate(gonogo, "False"))

    #Trailmaking Taps error rate (% of taps_incorrect=True divided by total rows)
    analysisData.append(rate(trailmaking, "True"))
    
    #Avg interkey delay (average time between key presses)
    analysisData.append(avg_interkey_delay(keylogs))

    with open("analysisData.csv", "w") as output:
        writer = csv.writer(output, lineterminator='\n')
        writer.writerow(header)
        writer.writerow(analysisData)







