import os
import pandas as pd

import os

script_dir = os.path.dirname(os.path.abspath(__file__))

# Set the working directory to the script's directory
os.chdir(script_dir)

# Define the folders to process
folders = ['2013', '2015', '2017']

# Loop through each folder
for folder in folders:
    # Define the path to the original Excel file
    file_path = os.path.join(folder, f'{folder} PFAS.xlsx')

    # Read the Excel file
    df = pd.read_excel(file_path)

    # Add the new columns while ignoring NaN values (default behavior of sum)
    df['Total PFAS'] = df[['PFDA', 'PFHxS', 'NMeFOSAA', 'PFNA', 'PFUnA', 'PFOA', 'PFOS']].sum(axis=1)
    df['PFCAs'] = df[['PFDA', 'PFNA', 'PFOA', 'PFUnA']].sum(axis=1)
    df['PFSAs'] = df[['PFHxS', 'NMeFOSAA', 'PFOS']].sum(axis=1)

    # Define the new file name and path
    output_file = os.path.join(folder, 'PFAS_totals.xlsx')

    # Save the updated DataFrame to a new Excel file
    df.to_excel(output_file, index=False)

    print(f"Processed {folder}, saved updated file to {output_file}")
