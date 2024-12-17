import os
import pandas as pd
import matplotlib.pyplot as plt
plt.rcParams['font.family'] = 'Times New Roman'
# Directory containing the folders (2013, 2015, 2017)
base_dir = os.path.dirname(os.path.abspath(__file__))

# List of years to iterate through
years = ['2013', '2015', '2017']
compounds = ['PFOA', 'PFNA', 'PFDA', 'PFUnA', 'PFHxS', 'PFOS', 'NMeFOSAA']

# Custom colors for the compounds
custom_colors = {
    'PFOA': 'red',
    'PFNA': 'firebrick',
    'PFDA': 'maroon',
    'PFUnA': '#4C1C11',
    'PFHxS': 'darkturquoise',
    'PFOS': 'deepskyblue',
    'NMeFOSAA': 'steelblue'
}

# Initialize an empty list to store data for each year
dfs = []

# Loop through each year's folder and read the 'PFAS_totals' file
for year in years:
    file_path = os.path.join(base_dir, year, 'PFAS_totals.xlsx')
    if os.path.exists(file_path):
        df = pd.read_excel(file_path)
        df['Year'] = year  # Add a column for the year
        dfs.append(df)

# Combine all dataframes into one larger dataframe
combined_df = pd.concat(dfs)

# Group by year and compute the average of the compounds
average_df = combined_df.groupby('Year')[compounds].mean().reset_index()

# Create a dictionary for custom y-axis labels
custom_y_labels = {'2013': '2013-14', '2015': '2015-16', '2017': '2017-18'}

# Plot a horizontal stacked bar chart
fig, ax = plt.subplots(figsize=(12, 4))

# Get cumulative sums to create the stacked effect
cumulative_sums = pd.DataFrame()
for compound in compounds:
    if cumulative_sums.empty:
        cumulative_sums[compound] = average_df[compound]
    else:
        cumulative_sums[compound] = cumulative_sums.iloc[:, -1] + average_df[compound]

# Create the stacked bar chart with custom colors
for compound in compounds:
    ax.barh(average_df['Year'], average_df[compound], 
            left=cumulative_sums[compound] - average_df[compound], 
            color=custom_colors.get(compound, 'gray'),  # Apply custom color
            label=compound,
            height=0.5)  # Make the bars skinnier by adjusting the height

ax.invert_yaxis()


# Customize the plot
ax.set_xlabel('Average Concentration (ng/mL)', fontsize=16)
ax.set_ylabel('Data Release Cycle', fontsize=16)
ax.set_yticklabels([custom_y_labels.get(label, label) for label in average_df['Year']], fontsize=14)  # Change y-axis labels

# Remove the title
ax.set_title('Average Serum PFAS Concentration (ng/mL) by Year', fontsize=20)  # Remove the title

# Change font to Times New Roman
plt.rcParams['font.family'] = 'Times New Roman'

# Add legend
ax.legend(loc='lower right', fontsize=14)
ax.tick_params(axis='x', labelsize=14) 
# Save the plot as a PNG file
output_file = os.path.join(base_dir, 'average_PFAS_concentration_by_year_2013_top.png')
plt.savefig(output_file, dpi=1200, bbox_inches='tight')

# Display the plot
plt.tight_layout()
#plt.show()

print(f"Plot saved as {output_file}")

