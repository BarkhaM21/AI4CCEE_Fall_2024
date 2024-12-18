import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
from scipy.stats import f_oneway  # For One-Way ANOVA
from sklearn.preprocessing import LabelEncoder
from scipy.stats import chi2_contingency

file_path = 'C:/Users/Sam/Desktop/Research/NHANES_Work/APHA/Data/Combined_PFAS_Demographics_New.xlsx'
excel_data = pd.ExcelFile(file_path)

# Load the first sheet (or specify a sheet if needed)
data = excel_data.parse(sheet_name=0)

# Identify categorical and numerical columns
categorical_cols = [
    "SDDSRVYR", "RIAGENDR", "RIDRETH3", "RIDEXMON", "DMQMILIZ", "DMDBORN4", "DMDCITZN", 
    "DMDEDUC2", "DMDMARTL", "SIALANG", "SIAPROXY", "SIAINTRP", "FIALANG", "FIAPROXY", 
    "FIAINTRP", "MIALANG", "MIAPROXY", "MIAINTRP", "AIALANGA", "DMDHRGND", "DMDHRAGZ", 
    "DMDHREDZ", "DMDHRMAZ", "INDHHIN2", "INDFMIN2"
]
numerical_cols = [
    "RIDAGEYR", "DMDHHSIZ", "DMDFMSIZ", "DMDHHSZA", "DMDHHSZB", "DMDHHSZE", "INDFMPIR"
]

from sklearn.impute import SimpleImputer

# For numerical data
imputer = SimpleImputer(strategy='most_frequent')  # Use 'mean' or 'most_frequent' for different strategies
data[numerical_cols] = imputer.fit_transform(data[numerical_cols])

# For categorical data
imputer_cat = SimpleImputer(strategy='most_frequent')
data[categorical_cols] = imputer_cat.fit_transform(data[categorical_cols])


# Function to calculate Cramér's V for categorical variables
def cramers_v(x, y):
    confusion_matrix = pd.crosstab(x, y)
    chi2 = chi2_contingency(confusion_matrix)[0]
    n = confusion_matrix.sum().sum()
    r, k = confusion_matrix.shape
    return np.sqrt(chi2 / (n * (min(r, k) - 1)))

# Function to calculate One-Way ANOVA for categorical-numerical pairs
def anova_corr(x, y):
    # If the categorical variable is non-binary (more than two categories)
    if len(np.unique(x)) > 2:
        # Perform One-Way ANOVA
        groups = [y[x == group] for group in np.unique(x)]
        f_stat, p_value = f_oneway(*groups)
        return f_stat  # Return the F-statistic from ANOVA
    else:
        return np.nan  # Not applicable for binary categorical variables

# Initialize the correlation matrices
numerical_corr_matrix = pd.DataFrame(np.zeros((len(numerical_cols), len(numerical_cols))),
                                     index=numerical_cols, columns=numerical_cols)
categorical_corr_matrix = pd.DataFrame(np.zeros((len(categorical_cols), len(categorical_cols))),
                                       index=categorical_cols, columns=categorical_cols)

# Calculate correlations

# 1. Pearson for numerical-numerical
for col1 in numerical_cols:
    for col2 in numerical_cols:
        if col1 != col2:
            numerical_corr_matrix.loc[col1, col2] = data[col1].corr(data[col2])

# 2. Cramer's V for categorical-categorical
for col1 in categorical_cols:
    for col2 in categorical_cols:
        if col1 != col2:
            categorical_corr_matrix.loc[col1, col2] = cramers_v(data[col1], data[col2])

# 3. ANOVA for categorical-numerical
for cat_col in categorical_cols:
    for num_col in numerical_cols:
        numerical_corr_matrix.loc[num_col, cat_col] = anova_corr(data[cat_col], data[num_col])

# # Save to new sheet in the Excel file
# with pd.ExcelWriter(file_path, engine='openpyxl', mode='a') as writer:
#     numerical_corr_matrix.to_excel(writer, sheet_name='numerical_correlation')
#     categorical_corr_matrix.to_excel(writer, sheet_name='categorical_correlation')

# Masking the upper triangle (or lower triangle) of the correlation matrices
numerical_mask = np.triu(np.ones_like(numerical_corr_matrix, dtype=bool))  # Upper triangle mask for numerical
categorical_mask = np.triu(np.ones_like(categorical_corr_matrix, dtype=bool))  # Upper triangle mask for categorical

# Plotting the correlation heatmaps with the masks

# Numerical-Numerical heatmap
plt.figure(figsize=(12, 10))
sns.heatmap(numerical_corr_matrix, annot=True, cmap='coolwarm', center=0, fmt=".2f", mask=numerical_mask)
plt.title('Numerical-Numerical Correlation Heatmap')
plt.show()

# Categorical-Categorical heatmap
plt.figure(figsize=(12, 10))
sns.heatmap(categorical_corr_matrix, annot=True, cmap='coolwarm', center=0, fmt=".2f", mask=categorical_mask)
plt.title('Categorical-Categorical Correlation Heatmap')
plt.show()
