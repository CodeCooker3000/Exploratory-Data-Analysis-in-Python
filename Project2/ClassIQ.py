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

filename = 'college_student_placement_dataset.csv'

with open(filename) as f:
    reader = csv.reader(f)
    header_row = next(reader)
    iq = []
    for row in reader:
        curr_iq = int(row[1])
        iq.append(curr_iq)

# sampling distribution of attendance
# lets get a sample of 50 data points, 500 times, and plot them
sample_means = []
for i in range(500):
    random_sample = np.random.choice(iq, 50)
    ans = get_mean(random_sample)
    ans = np.ceil(ans)
    sample_means.append(ans)

mean_labels = []
mean_frequencies = []
for value in range(80, 130, 1):
    mean_labels.append(value)
    frequency = sample_means.count(value)
    mean_frequencies.append(frequency)

mean_freq_table = pygal.Histogram(title="Mean Class IQ of Students Sampling Distribution", x_title='Sample Means', y_title='Frequency',xrange=(80, 130), yrange=(0, 100))
mean_freq_table.add("Mean Student IQ", [(mean_frequencies[ct], mean_labels[ct], mean_labels[ct] + 1) for ct in range(0, 50)])
mean_freq_table.render_to_file('histogramIQ.svg') 


# point estimate of mean
real_mean = get_mean(iq)
random_sample = np.random.choice(iq, 50)
sample_mean = get_mean(random_sample)
sample_variance = get_variance(random_sample)

print(f"Real Mean: {real_mean}. Sample Mean: {sample_mean}")
print(f"Sample Variance: {sample_variance}")

#interval estimate of mean
# we can see that the sample means are roughly normally distributed 
t_value = 2.00958
interval_low = sample_mean - t_value * sample_variance / (7)
interval_high = sample_mean + t_value * sample_variance / (7)

print(f"95% Interval Estimate: [{interval_low}, {interval_high}]")
