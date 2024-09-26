# -*- coding: utf-8 -*-
"""Untitled2.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1w7cbjipmq-V-XkuuzCz7DSL5DNeK7Ecc
"""

# prompt: creat folder in linux

!mkdir my_new_folder

!mkdir act_2

cd act_2

from pathlib import PureWindowsPath
PureWindowsPath

cd act_2



!echo $PATH

pwd

# prompt: how to creat a file

!touch my_new_file.txt

# Commented out IPython magic to ensure Python compatibility.
# # prompt: creat shell script
# 
# %%writefile my_script.sh
# #!/bin/bash
# 
# echo "This is a shell script."
# echo "Current directory: $(pwd)"
# echo "List of files:"
# ls -l
#

print('Hello, world')

my_name="Dongming"
my_age="27"

print(f"My name is {my_name} and I am {my_age} years old.")

sentence="This is a trial"
print(sentence.upper())

print(sentence.lower())

my_hobby="playing basketball"
print(f"My name is {my_name}")
print(f"My hobby is {my_hobby}")

print(f"My name is {my_name} and my hobby is {my_hobby}")

road_length = 200
road_width = 30
layer_thick = 0.2
convert = 0.76
asphalt_price = 120
costs= road_width*road_length*layer_thick*convert*asphalt_price
print(costs)

print(f"the costs for asphalt is {costs} dollars")

labor_price=50

laber_number=200

laber_costs= labor_price*laber_number

concrete_price=100

concrete_quantity=2000

concrete_costs=concrete_price*concrete_quantity

total_costs=costs+laber_costs+concrete_costs

print(f"the costs for concrete is {concrete_costs} dollars")
print(f"the costs for laber is {laber_costs} dollars")
print(f"the costs for asphalt is {costs} dollars")
print(f"the total need is {total_costs} dollars")

Required=total_costs

bugdet=50000

print(Required<=bugdet)

# prompt: read CSV file

import pandas as pd

# Replace 'your_file.csv' with the actual path to your CSV file
df = pd.read_csv('/content/example.csv')

# Now you can work with the data in the DataFrame 'df'
print(df.head())  # Print the first few rows of the DataFrame

print(df.describe())

print(df.info())

# prompt: read csv

import pandas as pd

# Replace 'your_file.csv' with the actual path to your CSV file
df = pd.read_csv('/content/235-Nov.csv')

# Now you can work with the data in the DataFrame 'df'
print(df.head())  # Print the first few rows of the DataFrame

# prompt: examine data types of each column

print(df.dtypes)

# prompt: check missing values

print(df.isnull().sum())

# prompt: get mean value of database specific column

# Assuming 'df' is your DataFrame and 'column_name' is the name of the column you want to calculate the mean for
column_name = 'time'  # Replace with the actual column name

if column_name in df.columns:
  mean_value = df[column_name].mean()
  print(f"The mean value of the '{column_name}' column is: {mean_value}")
else:
  print(f"The column '{column_name}' does not exist in the DataFrame.")

# prompt: get median value of database specific column

# Assuming 'df' is your DataFrame and 'column_name' is the name of the column you want to calculate the median for
column_name = 'time'  # Replace with the actual column name

if column_name in df.columns:
  median_value = df[column_name].median()
  print(f"The median value of the '{column_name}' column is: {median_value}")
else:
  print(f"The column '{column_name}' does not exist in the DataFrame.")

# prompt: convert units of specific column in database

# Assuming 'df' is your DataFrame and 'column_name' is the name of the column you want to convert
column_name = 'time'  # Replace with the actual column name
new_unit_column_name = 'time_in_hours'

# Define the conversion factor (e.g., convert from minutes to seconds)
conversion_factor = 60

if column_name in df.columns:
  # Create a new column with the converted values
  df[new_unit_column_name] = df[column_name] / conversion_factor
  print(df.head())  # Print the first few rows of the DataFrame with the new column
else:
  print(f"The column '{column_name}' does not exist in the DataFrame.")