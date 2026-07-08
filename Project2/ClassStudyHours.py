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
        high = float(row[1])
        participation.append(high)

# sampling distribution of attendance
# lets get a sample of 50 data points, 500 times, and plot them
sample_means = []
for i in range(500):
    random_sample = np.random.choice(participation, 50)
    ans = get_mean(random_sample)
    ans = np.ceil(ans)
    sample_means.append(ans)

mean_labels = []
mean_frequencies = []
for value in range(10, 30):
    mean_labels.append(value)
    frequency = sample_means.count(value)
    mean_frequencies.append(frequency)

mean_freq_table = pygal.Histogram(title="Mean Study Hours of Students Sampling Distribution", x_title='Sample Means', y_title='Frequency',xrange=(10, 30), yrange=(0, 200))
mean_freq_table.add("Study Hours", [(mean_frequencies[ct - 10], mean_labels[ct - 10], mean_labels[ct - 10] + 1) for ct in range(10, 30)])
mean_freq_table.render_to_file('histogramStudy.svg') 


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
