import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from pygal.style import Style
import pygal
import csv 

filename = 'student_performance.csv'

with open(filename) as f:
    reader = csv.reader(f)
    header_row = next(reader)
    # print(header_row)
    # for index, column_header in enumerate(header_row):
    #     print(index, column_header)
    participation = []
    grades = []
    for row in reader:
        high = float(row[6])
        participation.append(high)
        grade = row[5].strip()[0]
        grades.append(grade)

#constructing the frequency table
labels = []
frequencies = []
for value in np.arange(0, 10.5, 0.5):
    labels.append(value)
    frequency = participation.count(value)
    frequencies.append(frequency)


table_data = [[label, freq] for label, freq in zip(labels, frequencies)]
fig, ax = plt.subplots(figsize=(6, len(labels) * 0.35))
ax.axis('off')

table = ax.table(
    cellText=table_data,
    colLabels=["Attendance Rating", "Frequency"],
    loc="center",
    cellLoc="center"
)

table.auto_set_font_size(False)
table.set_fontsize(10)
table.scale(1, 1.4)

plt.savefig("frequency_table.svg", bbox_inches="tight", dpi=200)
plt.close()

freq_table = pygal.Bar(width=800, height=400, explicit_size=True)
freq_table.title = "Class Attendance Ratings of Students"
freq_table.x_labels = map(str, np.arange(0, 10.5, 0.5))
freq_table.add('Attendance Rating', frequencies)
freq_table.render_to_file('bar_chart.svg') 

freq_table = pygal.Line(width=800, height=800, explicit_size=True)
freq_table.title = "Class Attendance Ratings of Students"
freq_table.x_labels = map(str, np.arange(0.25, 10.5, 0.5))
freq_table.add('Attendance Rating', frequencies)
freq_table.render_to_file('line_chart.svg') 

labels = ['A', 'B', 'C', 'D', 'F']
grade_freq = []
total = 0
for value in labels:
    frequency = grades.count(value)
    total += frequency
    grade_freq.append(frequency)

custom_style = Style(
    colors=(
        '#4e79a7',
        '#f28e2b',
        '#e15759',
        '#76b7b2',
        '#59a14f'
    )
)
pie_chart = pygal.Pie(width=800, height=800, explicit_size=True, style=custom_style)
pie_chart.title = "Grades Attained By Student"
for i in range(0, 5):
    pie_chart.add(labels[i], (grade_freq[i] * 100.00)/(total))
pie_chart.render_to_file('pie_chart.svg')
