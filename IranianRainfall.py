import matplotlib.pyplot as plt
import pygal
import csv

filename = 'Rainfall_Iran_19012022.csv'

c1 = []
c2 = []
c3 = []
c4 = []
c5 = []
c6 = []
c7 = []

with open(filename) as f:
    reader = csv.reader(f)
    header_row = next(reader)
    # print(header_row)
    # for index, column_header in enumerate(header_row):
    #     print(index, column_header)
    for row in reader:
        high = float(row[1])
        c1.append(high)
        high = float(row[2])
        c2.append(high)
        high = float(row[3])
        c3.append(high)
        high = float(row[4])
        c4.append(high)
        high = float(row[5])
        c5.append(high)
        high = float(row[6])
        c6.append(high)
        high = float(row[7])
        c7.append(high)
        
labels = ["Ahvaz", "Arak", "Ardabil", "Bandar `Abbas", "Bandar-e Bushehr", "Birjand", "Esfahan"]

box_plot = pygal.Box(width=800, height=800, explicit_size=True)
box_plot.title = 'Rainfall in Iranian Cities'
box_plot.add(labels[0], c1)
box_plot.add(labels[1], c2)
box_plot.add(labels[2], c3)
box_plot.add(labels[3], c4)
box_plot.add(labels[4], c5)
box_plot.add(labels[5], c6)
box_plot.add(labels[6], c7)
box_plot.render()
box_plot.render_to_file('box_plot.svg') 
