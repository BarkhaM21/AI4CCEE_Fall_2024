import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from math import pi
import os
plt.rcParams['font.family'] = 'Times New Roman'
# Ensure we're looking in the same directory as the script
current_dir = os.path.dirname(os.path.abspath(__file__))
file_path = os.path.join(current_dir, 'feature_importance_rankings_top10.xlsx')

# Step 1: Load the Excel file
try:
    excel_data = pd.read_excel(file_path, sheet_name=None)  # Load all sheets
except FileNotFoundError:
    print(f"Error: The file 'feature_importance_rankings.xlsx' was not found in {current_dir}.")
    exit()

# Step 2: Sum Importance for each Descriptive across all sheets
importance_sums = pd.Series(dtype=float)

# Iterate through each sheet (target analyte)
for analyte in excel_data.keys():
    df = excel_data[analyte]
    
    # Sum Importance for each Descriptive
    temp_sums = df.groupby('Descriptive')['Importance'].sum()
    
    # Add to the overall importance sums
    importance_sums = importance_sums.add(temp_sums, fill_value=0)

# Identify the top 10 features by summed Importance
top_10_features = importance_sums.nlargest(10).index

# Step 3: Create radar plots for all analytes in one figure
def create_radar_chart(ax, df, analyte_name, feature_numbers, max_value):
    # Number of variables (features)
    num_vars = len(df)
    
    # Compute the angle for each feature (in radians)
    angles = [n / float(num_vars) * 2 * pi for n in range(num_vars)]
    angles += angles[:1]  # Close the radar chart loop

    # Draw one axis per feature + add labels as numbers
    ax.set_theta_offset(pi / 2)
    ax.set_theta_direction(-1)
    ax.set_xticks(angles[:-1])
    ax.set_xticklabels(feature_numbers, fontsize=8)  # Use numbers as labels

    # Set the same scale for all radar plots based on the max value for the analyte
    ax.set_ylim(0, max_value)

    # Align the scale with the centerline
    ax.yaxis.set_tick_params(labelsize=8)
    ax.yaxis.set_ticks_position('right')  # Set ticks on the centerline

    # Plot data
    values = df['Importance'].values.flatten().tolist()
    values += values[:1]  # Complete the loop
    ax.plot(angles, values, linewidth=2, linestyle='solid', label=analyte_name)
    ax.fill(angles, values, alpha=0.25)

    # Set title for each subplot
    ax.set_title(analyte_name, size=12, color='blue', y=1.1)

# Define the target analytes in the desired order
analyte_order = ["Total PFAS", "PFCAs", "PFSAs", "PFOA", "PFNA", "PFDA", "PFUnA", "PFHxS", "PFOS", "NMeFOSAA"]

# Create a figure with subplots (2 rows, 5 columns)
fig, axs = plt.subplots(2, 5, figsize=(20, 10), subplot_kw=dict(polar=True))

# Flatten the axes array for easier iteration
axs = axs.flatten()

# Store the top 10 feature names and assign numbers to them
feature_names_to_numbers = {feature: str(i+1) for i, feature in enumerate(top_10_features)}

# List of numbers for the radar chart labels
feature_numbers = list(feature_names_to_numbers.values())

# Iterate over the target analytes and plot radar charts
for i, analyte in enumerate(analyte_order):
    if analyte in excel_data:
        # Filter to include only the top 10 features
        df = excel_data[analyte].set_index('Descriptive')
        df = df.loc[top_10_features]

        # Set max importance for this specific analyte
        max_importance_value = df['Importance'].max()

        # Create the radar chart
        create_radar_chart(axs[i], df, analyte, feature_numbers, max_importance_value)

# Create a legend that maps the numbers to feature names
legend_labels = [f"{num}: {feature}" for feature, num in feature_names_to_numbers.items()]

# Add a legend to the figure without lines or boxes
fig.legend(legend_labels, loc='upper center', fontsize=16, ncol=2, bbox_to_anchor=(0.5, 0.2),
           handlelength=0, frameon=False)

# Adjust the space to accommodate the legend and spacing between subplots
plt.subplots_adjust(top=0.85, bottom=0.2, hspace=0.3, wspace=0.3)

# Save the figure as a file (e.g., PNG)
#output_file = os.path.join(current_dir, 'radar_plots_justPFCAs.png')
#plt.savefig(output_file, bbox_inches='tight', dpi=300)

# Show the plot (optional)
plt.show()

