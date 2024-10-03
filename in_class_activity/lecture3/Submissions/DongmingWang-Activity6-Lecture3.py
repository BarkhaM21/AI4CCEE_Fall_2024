# -*- coding: utf-8 -*-
"""Untitled4.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/19SypA0sweEVRoIY-KYD0vXAmBelZXyK4
"""

# prompt: creat new folder

!mkdir activity6

cd activity6

# prompt: Import the Pandas library

import pandas as pd

# prompt: Load the dataset into a Pandas DataFrame and inspect the first few rows

import pandas as pd
df = pd.read_csv('/content/235-Nov (1).csv')
print(df.head())

import pandas as pd
df['datetime'] = pd.to_datetime(df['date'], format='%Y%m%d')

def convert_to_hours(time_str):
    try:
        hours = int(time_str[:2])
        minutes = int(time_str[2:4])
        seconds = int(time_str[4:6])
        total_hours = hours + minutes / 60 + seconds / 3600
        return total_hours
    except:
        return None

df['time_in_hours'] = df['time'].apply(convert_to_hours)

print(df.head())

import pandas as pd
df['datetime'] = pd.to_datetime(df['date'], format='%Y%m%d')

def convert_to_hours(time_str):
    try:
        hours = int(time_str[:2])
        minutes = int(time_str[2:4])
        seconds = int(time_str[4:6])
        total_hours = hours + minutes / 60 + seconds / 3600
        return total_hours
    except:
        return None

df['time_in_hours'] = df['time'].apply(convert_to_hours)

import pandas as pd

# Assuming df is your DataFrame and it has columns named 'date' and 'lane_occupancy'
# If your DataFrame has different column names, replace them accordingly

for date in df['date'].unique():
  date_df = df[df['date'] == date]
  avg_occupancy = date_df['lane-occupancy'].mean()
  print(f"Average lane occupancy for {date}: {avg_occupancy}")

# prompt: Visualize the total lane counts based on status, create a pie chart

import matplotlib.pyplot as plt

# Assuming 'status' is the column containing the status information
lane_counts = df['status'].value_counts()

# Create a pie chart
plt.figure(figsize=(8, 8))
plt.pie(lane_counts, labels=lane_counts.index, autopct='%1.1f%%', startangle=90)
plt.title('Total Lane Counts by Status')
plt.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.
plt.show()

# prompt: Create Scatter Plot of Lane-Occupancy vs. Lane-Count.

import matplotlib.pyplot as plt
plt.figure(figsize=(10, 6))
plt.scatter(df['lane-occupancy'], df['lane-count'])
plt.xlabel('Lane Occupancy')
plt.ylabel('Lane Count')
plt.title('Scatter Plot of Lane Occupancy vs. Lane Count')
plt.grid(True)
plt.show()