import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from pygal.style import Style
import pygal
import csv 

def get_mean(sample):
    sum = 0
    for x in sample:
        sum += x
    sum /= len(sample)
    return sum

def get_variance(sample):
    square_sum = 0
    mean = get_mean(sample)
    for x in sample:
        square_sum += (x - mean) * (x - mean)
    variance = square_sum/(len(sample) - 1)
    return variance

filename = 'student_performance.csv'

with open(filename) as f:
    reader = csv.reader(f)
    header_row = next(reader)
    participation = []
    for row in reader:
        high = float(row[6])
        participation.append(high)

# sampling distribution of attendance
# lets get a sample of 50 data points, 500 times, and plot them
sample_means = []
for i in range(500):
    random_sample = np.random.choice(participation, 50)
    ans = get_mean(random_sample)
    ans = np.ceil(ans * 8) / 8
    sample_means.append(ans)

mean_labels = []
mean_frequencies = []
for value in np.arange(4.5, 7.5, 0.125):
    mean_labels.append(value)
    frequency = sample_means.count(value)
    mean_frequencies.append(frequency)

mean_freq_table = pygal.Histogram(title="Mean Class Attendance Ratings of Students Sampling Distribution", x_title='Sample Means', y_title='Frequency',xrange=(0, 10), yrange=(0, 200))
mean_freq_table.add("Attendance Rating", [(mean_frequencies[ct], mean_labels[ct], mean_labels[ct] + 0.125) for ct in range(0, 24)])
mean_freq_table.render_to_file('histogram.svg') 


# point estimate of mean
real_mean = get_mean(participation)
random_sample = np.random.choice(participation, 50)
sample_mean = get_mean(random_sample)
sample_variance = get_variance(random_sample)

print(f"Real Mean: {real_mean}. Sample Mean: {sample_mean}")

#interval estimate of mean
# we can see that the sample means are roughly normally distributed 
t_value = 1.67655
interval_low = sample_mean - t_value * sample_variance / (7)
interval_high = sample_mean + t_value * sample_variance / (7)

print(f"90% Interval Estimate: [{interval_low}, {interval_high}]")
