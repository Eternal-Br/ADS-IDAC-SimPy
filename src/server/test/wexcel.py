import xlwt
import json
import csv


list1 = []

with open('./r1.txt', 'r') as f:
    for line in f:
        # line = f.readline()
        # print(line)
        data = json.loads(line)
        # print(data)
        GA = data['GoAhead']
        TL = data['TurnLeft']
        TR = data['TurnRight']
        list1.append([GA, TL, TR])
        print(list1)

with open('./r1.csv', 'a+') as fc:
    writer = csv.writer(fc)
    csv_head = ['GoAhead', 'TurnLeft', 'TurnRight']
    writer.writerow(csv_head)
    for item in list1:
        writer.writerow(item)