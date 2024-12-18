# Step 1: Import necessary libraries
import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error
import matplotlib.pyplot as plt
import os
from datetime import datetime
from matplotlib.lines import Line2D
from sklearn.inspection import PartialDependenceDisplay

# Set up the script directory
script_dir = os.path.dirname(os.path.abspath(__file__))
os.chdir(script_dir)

# Step 2: Load the combined PFAS demographics data
data_file = os.path.join(script_dir, 'Combined_PFAS_Demographics.xlsx')
combined_PFAS_Demographics = pd.read_excel(data_file)

# Define categorical and numerical variables
categorical_vars = ['SDDSRVYR','RIDRETH3','DMDEDUC2','DMDMARTL','INDHHIN2']

numerical_vars = ['RIDAGEYR','DMDHHSIZ','DMDHHSZA','DMDHHSZE','INDFMPIR']
# categorical_vars = [
#     "SDDSRVYR", "RIAGENDR", "RIDRETH3", "RIDEXMON", "DMQMILIZ", "DMDBORN4",
#     "DMDCITZN", "DMDEDUC2", "DMDMARTL", "SIALANG", "SIAPROXY", "SIAINTRP",
#     "FIALANG", "FIAPROXY", "FIAINTRP", "MIALANG", "MIAPROXY", "MIAINTRP",
#     "AIALANGA", "DMDHRGND", "INDHHIN2"#,
#     #"DMDHRAGZ","DMDHREDZ","DMDHRMAZ" removed for inconsistencies across years
#     #, "INDFMIN2" remove annual family income for correlation
# ]

# numerical_vars = [
#     'RIDAGEYR', 'DMDHHSIZ', 'DMDHHSZA', #'DMDFMSIZ' removed for correlation
#     'DMDHHSZB', 'DMDHHSZE', 'INDFMPIR'
# ]

# List of target variables
#target_variables = ['PFCAs', 'PFOA', 'PFNA', 'PFDA', 'PFUnA']

target_variables = ['PFDA', 'PFHxS', 'NMeFOSAA', 'PFNA', 'PFUnA', 'PFOA', 'PFOS', 'Total PFAS', 'PFCAs', 'PFSAs']

# Create a directory to save plots with the current date
date_str = datetime.now().strftime('%Y-%m-%d')
output_dir = os.path.join(script_dir, f'feature_importance_plots_{date_str}')
os.makedirs(output_dir, exist_ok=True)

# Dictionary for descriptive labels
descriptive_labels = {
    'SDDSRVYR': 'Data release cycle',
    'RIAGENDR': 'Gender',
    'RIDAGEYR': 'Age in years at screening',
    'RIDRETH3': 'Race/Hispanic origin w/ NH Asian',
    'RIDEXMON': 'Six month time period',
    'DMQMILIZ': 'Served active duty in US Armed Forces',
    'DMDBORN4': 'Country of birth',
    'DMDCITZN': 'Citizenship status',
    'DMDMARTL': 'Marital status',
    'DMDEDUC2':'Education level - Adults 20+',
    'SIALANG': 'Language of SP Interview',
    'SIAPROXY': 'Proxy used in SP Interview?',
    'SIAINTRP': 'Interpreter used in SP Interview?',
    'FIALANG': 'Language of Family Interview',
    'FIAPROXY': 'Proxy used in Family Interview?',
    'FIAINTRP': 'Interpreter used in Family Interview?',
    'MIALANG': 'Language of MEC Interview',
    'MIAPROXY': 'Proxy used in MEC Interview?',
    'MIAINTRP': 'Interpreter used in MEC Interview?',
    'AIALANGA': 'Language of ACASI Interview',
    'DMDHHSIZ': 'Total number of people in the Household',
    'DMDFMSIZ': 'Total number of people in the Family',
    'DMDHHSZA': '# of children 5 years or younger in HH',
    'DMDHHSZB': '# of children 6-17 years old in HH',
    'DMDHHSZE': '# of adults 60 years or older in HH',
    'DMDHRGND': 'HH ref person\'s gender',
    'INDHHIN2': 'Annual household income',
    'INDFMIN2': 'Annual family income',
    'INDFMPIR': 'Ratio of family income to poverty'
}

# Create a new Excel writer
output_excel_file = os.path.join(script_dir, 'feature_importance_rankings_top10.xlsx')
excel_writer = pd.ExcelWriter(output_excel_file, engine='openpyxl')

# Iterate through each target variable
for target_variable in target_variables:
    # Prepare the data for modeling
    X = combined_PFAS_Demographics[categorical_vars + numerical_vars]
    y = combined_PFAS_Demographics[target_variable]

    # One-hot encode categorical variables
    X_encoded = pd.get_dummies(X, columns=categorical_vars, drop_first=True)

    # Split the data into training and test sets
    X_train, X_test, y_train, y_test = train_test_split(X_encoded, y, test_size=0.2, random_state=42)

    # Initialize and fit the Random Forest model
    model = RandomForestRegressor(n_estimators=200, random_state=42)
    model.fit(X_train, y_train)

    # Make predictions
    y_pred = model.predict(X_test)

    # Calculate RMSE
    rmse = np.sqrt(mean_squared_error(y_test, y_pred))
    print(f'Root Mean Squared Error for {target_variable}: {rmse:.2f}')

    # Feature importance
    importance = model.feature_importances_
    feature_names = X_encoded.columns
    importance_df = pd.DataFrame({'Feature': feature_names, 'Importance': importance})
    importance_df = importance_df.sort_values(by='Importance', ascending=False)

    # Create a mapping of encoded features to their original categorical variable
    encoded_to_original = {}
    for original_var in categorical_vars:
        # Get the one-hot encoded feature names corresponding to the original variable
        encoded_features = [col for col in X_encoded.columns if col.startswith(f"{original_var}_")]
        for feature in encoded_features:
            encoded_to_original[feature] = original_var

    # Aggregate the importance by original variable including numerical variables
    importance_df['Original'] = importance_df['Feature'].map(encoded_to_original).fillna(importance_df['Feature'])

    # Aggregate by original variable
    aggregated_importance = importance_df.groupby('Original')['Importance'].sum().reset_index()

    # Sort the aggregated importance
    aggregated_importance = aggregated_importance.sort_values(by='Importance', ascending=False)

    # Replace original feature names with descriptive labels
    aggregated_importance['Descriptive'] = aggregated_importance['Original'].map(descriptive_labels).fillna(aggregated_importance['Original'])

    # Save the aggregated importance to the corresponding sheet
    aggregated_importance.to_excel(excel_writer, sheet_name=target_variable, index=False)

    # Plot the aggregated feature importance with descriptive labels
# Plot the aggregated feature importance with descriptive labels
    plt.figure(figsize=(12, 8))

    # Create a list of colors: darker blue for categorical, lighter blue for numerical
    colors = ['#1f77b4' if var in categorical_vars else '#87CEEB' for var in aggregated_importance['Original']]

    plt.barh(aggregated_importance['Descriptive'], aggregated_importance['Importance'], color=colors)
    plt.xlabel('Importance')

    # Update the title to include RMSE
    plt.title(f'Aggregated Feature Importance for {target_variable} (RMSE: {rmse:.2f})')
    plt.gca().invert_yaxis()  # To display the highest importance at the top
    
    

    # Create a custom legend
    legend_elements = [
        Line2D([0], [0], color='#1f77b4', lw=4, label='Categorical Variables'),
        Line2D([0], [0], color='#87CEEB', lw=4, label='Numerical Variables')
    ]

    plt.legend(handles=legend_elements, loc='lower right')

    
    # Save the plot
    plot_file_path = os.path.join(output_dir, f'feature_importance_{target_variable}.png')
    plt.savefig(plot_file_path, bbox_inches='tight')
    plt.close()  # Close the plot to free memory

    # # Create Partial Dependence Plots for  'INDFMPIR'
    # if target_variable == 'PFCAs':
    #     import matplotlib.pyplot as plt
    #     from sklearn.inspection import PartialDependenceDisplay

    #     # Feature to plot (continuous numerical variable)
    #     feature = 'INDFMPIR'

    #     # Get the index of the feature in the encoded dataset
    #     feature_index = X_encoded.columns.get_loc(feature)
    #     print(X_encoded['INDFMPIR'].min(), X_encoded['INDFMPIR'].max())
    #     # Generate and plot the Partial Dependence Plot using the new API
    #     fig, ax = plt.subplots(figsize=(10, 6))

    #     # Generate PDP using the new function
    #     PartialDependenceDisplay.from_estimator(
    #         model, X_train, features=[feature_index], 
    #         feature_names=X_encoded.columns, grid_resolution=50, ax=ax
    #     )

    #     # Title and formatting
    #     plt.suptitle(f'Partial Dependence Plot for {feature}')
    #     plt.subplots_adjust(top=0.9)

    #     # Show the plot
    #     plt.show()

    #     # Save the PDP plot
    #     pdp_plot_file_path = os.path.join(output_dir, f'PDP_{feature}.png')
    #     plt.savefig(pdp_plot_file_path, bbox_inches='tight')
    #     plt.close() 

# Save the Excel file
excel_writer.close()

print(f'Feature importance rankings saved to {output_excel_file}')
