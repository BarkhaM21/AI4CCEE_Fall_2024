import os
import pandas as pd

# Set the working directory to the folder where the script is located
script_dir = os.path.dirname(os.path.abspath(__file__))
os.chdir(script_dir)

# Define the folders and demographic variable files
folders = ['2013', '2015', '2017']
demographic_files = {
    '2013': '2013 Demographic Variables.xlsx',
    '2015': '2015 Demographic Variables.xlsx',
    '2017': '2017 Demographic Variables.xlsx'
}

# Define columns to drop for each year
columns_to_drop = {
    '2013': [ 'DMDHRBR4'
    ],
    '2015': ['DMDHRBR4'
    ],
    '2017': [
    ]
}

# Initialize an empty list to store dataframes for merging later
dataframes = []

# Loop through each folder
for folder in folders:
    # Read PFAS_totals.xlsx and drop rows with missing values
    pfas_file = os.path.join(folder, 'PFAS_totals.xlsx')
    df_pfas = pd.read_excel(pfas_file).dropna()

    # Read the demographic variables file
    demographic_file = os.path.join(folder, demographic_files[folder])
    df_demo = pd.read_excel(demographic_file)

    # Drop specified columns
    df_demo.drop(columns=columns_to_drop[folder], inplace=True, errors='ignore')

    # Merge the entire PFAS dataframe with demographic variables on SEQN
    df_merged = pd.merge(df_demo, df_pfas, on='SEQN', how='inner')

    # Append the merged dataframe to the list
    dataframes.append(df_merged)

# Concatenate all dataframes into one giant dataframe
final_df = pd.concat(dataframes, ignore_index=True)

# Optionally, save the final dataframe to an Excel file
final_df.to_excel('Combined_PFAS_Demographics_New.xlsx', index=False)

print("Merged dataframe created and saved as 'Combined_PFAS_Demographics_New.xlsx'.")

