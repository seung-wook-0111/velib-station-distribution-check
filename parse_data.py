import csv
import copy
dataset = []
processedSet = {}
formattedSet = []
def parseData():
    with open('put_target_file_name_here.csv', newline='') as csvfile:
        csvreader = csv.reader(csvfile)
        for row in csvreader:
            dataset.append(row)
def gatherData():
    for cnt, row in enumerate(dataset):
        if row[0] != 'Timer':
            stationId = row[3]
            tf = getTimeframe(row[0])
            coord = getCoord(row[8])
            if stationId in processedSet:
                processedSet[stationId][tf].append([row[4], row[5], row[6]])
            else:
                a = [[row[2], int(row[7]), coord[0], coord[1]], [], [], [], [], [], []]
                a[tf].append([row[4], row[5], row[6]])
                processedSet[stationId] = a
def processData():
    for key, value in processedSet.items():
        for i in range(1, 7):
            ebike = 0
            mech = 0
            dock = 0
            cnt = 0
            for item in value[i]:
                cnt += 1
                ebike += int(item[0])
                mech += int(item[1])
                dock += int(item[2])
            value[i] = [round(ebike/cnt), round(mech/cnt), round(dock/cnt)]
def formatData():
    formattedSet.append(["Station ID", "Station", "Capacity", "X Coordinate", "Y Coordinate", 
                         "Data Type", "Time", "Value"])
    t = ["E-Bike", "Mechanical", "Dock"]
    for key, value in processedSet.items():
        a = [key]
        for item in value[0]:
            a.append(item)
        for i, type in enumerate(t):
            b = copy.deepcopy(a)
            b.append(type)
            for cnt, item in enumerate(value[1:]):
                c = copy.deepcopy(b)
                c.append(cnt+1)
                c.append(item[i])
                formattedSet.append(c)

def writeData():
    with open('put_output_file_name_here.csv', 'w', newline='') as wfile:
        csvwriter = csv.writer(wfile)
        for row in formattedSet:
            csvwriter.writerow(row)
        
def getCoord(coordStr):
    a = coordStr.strip("][").split(',')
    b = [float(a[0]), float(a[1])]
    return b
def getTimeframe(timeStr):
    tf = int(timeStr.split()[1].split(":")[0])
    if tf >= 6 and tf < 7:
        return 1 # before rush hour
    elif tf >= 7 and tf < 11:
        return 2 # morning rush hour
    elif tf >= 11 and tf < 15:
        return 3 # lunch time
    elif tf >= 15 and tf < 17:
        return 4 # afternoon
    elif tf >= 17 and tf < 21:
        return 5 # night rush hour
    else:
        return 6 # night time

parseData()
gatherData()
processData()
formatData()
writeData()
print(formattedSet[100])