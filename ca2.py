import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
%matplotlib inline
import matplotlib
# Load Excel data
df = pd.read_excel("C:/Users/Sachin/Downloads/dashbordchatgpt.xlsx")
# Display the first few rows
print(df.head())
# Show general info about columns and data types
df.info()

# Show number of unique values in each column
print("\nUnique values per column:")
print(df.nunique())
# Summary statistics
print("\nSummary statistics of numeric columns:")
print(df.describe())

# Replace spaces with underscores and remove parentheses for consistency
df.columns = df.columns.str.strip().str.replace(" ", "_").str.replace("(", "").str.replace(")", "")

# Show cleaned column info
df.info()
# Rename key columns for simplicity
#  Rename key columns for simplicity 
df.rename(columns={
    "Annual_GHG_Emissions_Reductions_MT_CO2e": "GHG_Reductions",
    "Annual_Petroleum_Reductions_gallons": "Petroleum_Reductions",
    "Rebate_Amount_USD": "Rebate_Amount"
}, inplace=True)
# Show final info
df.info()







# Check for missing values in all columns
missing_values = df.isnull().sum()

# Display columns with missing values only
missing_values = missing_values[missing_values > 0]
print("Missing values in columns:\n")
print(missing_values)



df.isnull().sum()




# Counting unique values
print("\nUnique values in categorical columns:\n")
for col in df.select_dtypes(include='object').columns:
    unique_count = df[col].nunique()
    print(f"{col}: {unique_count} unique value{'s' if unique_count > 1 else ''}")



print(df.columns)



# Correlation and Covariance Analysis of Rebate_Amount

# Drop rows with missing Rebate_Amount
df_cleaned = df.dropna(subset=['Rebate_Amount'])

# Select numeric columns
numeric_columns = df_cleaned.select_dtypes(include='number')

# Correlation with Rebate_Amount
print("Correlation with Rebate_Amount:\n")
print(numeric_columns.corr()['Rebate_Amount'].sort_values(ascending=False))

# Covariance with Rebate_Amount
print("\nCovariance with Rebate_Amount:\n")
print(numeric_columns.cov()['Rebate_Amount'].sort_values(ascending=False))


#Rebate Amount vs GHG Reductions by EV Type
plt.figure(figsize=(12, 6))

sns.scatterplot(
    data=df,
    x='Rebate_Amount',
    y='GHG_Reductions',
    hue='EV_Type',         # Color points by EV type
    style='EV_Type',       # Different marker styles
    palette='Set1',
    s=80,                  # Marker size
    edgecolor='black',     # Outline for points
    alpha=0.7              # Transparency
)

plt.title(' Rebate Amount vs GHG Reductions by EV Type', fontsize=14)
plt.xlabel('Rebate Amount (USD)', fontsize=12)
plt.ylabel('GHG Reductions (MT CO2e)', fontsize=12)
plt.grid(True, linestyle='--', alpha=0.5)
plt.xticks(fontsize=11)
plt.yticks(fontsize=11)
plt.tight_layout()
plt.show()

#rebate amount vs EV Type 

plt.figure(figsize=(10, 6))
sns.boxplot(
    data=df,
    x='EV_Type',
    y='Rebate_Amount',
    hue='EV_Type',             
    palette='coolwarm',
    linewidth=2.5,
    fliersize=4,
    dodge=False                 
)

#  Styling
plt.title('Rebate Amount Distribution by EV Type', fontsize=14)
plt.xlabel('EV Type', fontsize=12)
plt.ylabel('Rebate Amount (USD)', fontsize=12)
plt.grid(axis='y', linestyle='--', alpha=0.6)
plt.xticks(fontsize=11)
plt.legend([],[], frameon=False)  
plt.tight_layout()
plt.show()


plt.figure(figsize=(8, 6))
numeric_cols = ['GHG_Reductions', 'Petroleum_Reductions', 'Rebate_Amount']
corr = df[numeric_cols].corr()

sns.heatmap(corr, annot=True, cmap='YlGnBu', linewidths=0.5, linecolor='gray', square=True)
plt.title('Correlation Heatmap Between Key Numeric Features', fontsize=14)
plt.tight_layout()
plt.show()

# top 10 car brands
top_brands = df.groupby('Make')['GHG_Reductions'].mean().sort_values(ascending=False).head(10)
top_brands_df = top_brands.reset_index()
top_brands_df.columns = ['Make', 'Avg_GHG_Reductions']

plt.figure(figsize=(10, 6))
sns.barplot(
    data=top_brands_df,
    x='Avg_GHG_Reductions',
    y='Make',
    hue='Make',
    palette='dark:blue',
    edgecolor='black',
    legend=False  # Hide redundant legend
)

plt.title('Top 10 Car Brands by Avg GHG Reductions', fontsize=14)
plt.xlabel('Avg GHG Reductions (MT CO2e)', fontsize=12)
plt.ylabel('Car Brand', fontsize=12)
plt.grid(axis='x', linestyle='--', alpha=0.6)
plt.xticks(fontsize=11)
plt.yticks(fontsize=11)
plt.tight_layout()
plt.show()




# Select relevant numeric columns
corr_data = df[['Rebate_Amount', 'GHG_Reductions', 'Petroleum_Reductions']]

# Compute correlation matrix
correlation_matrix = corr_data.corr()

# Plotting the heatmap
plt.figure(figsize=(8, 6))
sns.heatmap(
    correlation_matrix,
    annot=True,
    cmap='PuBuGn',
    linewidths=0.6,
    linecolor='black',
    square=True,
    cbar_kws={"shrink": 0.8}
)

plt.title('Correlation Heatmap: Rebates, GHG & Petroleum Reduction', fontsize=14)
plt.tight_layout()
plt.show()


#top Ev model by rebate amount


# Assuming `top_models` is a Series with index as model names and values as counts
top_models = df['Model'].value_counts().head(10)
top_models_df = top_models.reset_index()
top_models_df.columns = ['Model', 'Count']

plt.figure(figsize=(12, 6))
sns.barplot(
    data=top_models_df,
    x='Model',
    y='Count',
    hue='Model',  
    palette='dark:#5A9_r',
    edgecolor='black',
    dodge=False  
)

plt.legend([], [], frameon=False)  
plt.title('Top EV Models by Number of Rebates', fontsize=14)
plt.xlabel('EV Model', fontsize=12)
plt.ylabel('Number of Rebates', fontsize=12)
plt.xticks(rotation=45, fontsize=11)
plt.grid(axis='y', linestyle='--', alpha=0.5)
plt.tight_layout()
plt.show()



#Distribution of Rebate Amount (KDE)

plt.figure(figsize=(10, 6))

sns.kdeplot(
    data=df,
    x='Rebate_Amount',
    fill=True,
    color='darkblue',
    linewidth=2,
    alpha=0.6
)

plt.title('Distribution of Rebate Amount (KDE)', fontsize=14)
plt.xlabel('Rebate Amount (USD)', fontsize=12)
plt.ylabel('Density', fontsize=12)
plt.grid(True, linestyle='--', alpha=0.5)
plt.xticks(fontsize=11)
plt.yticks(fontsize=11)
plt.tight_layout()
plt.show()

#Top 10 Counties by Number of EV Rebates

plt.figure(figsize=(10, 6))

# Get top 10 counties
top_counties = df['County'].value_counts().nlargest(10).reset_index()
top_counties.columns = ['County', 'Rebate_Count']

# Plot
sns.barplot(
    data=top_counties,
    y='County',
    x='Rebate_Count',
    hue='County',  # Needed to use palette
    palette='dark:#FF5733',
    edgecolor='black',
    legend=False   # Hide redundant legend
)


plt.title('Top 10 Counties by Number of EV Rebates', fontsize=14)
plt.ylabel('County', fontsize=12)
plt.xlabel('Number of Rebates', fontsize=12)
plt.grid(axis='x', linestyle='--', alpha=0.5)
plt.yticks(fontsize=11)
plt.tight_layout()
plt.show()

#Distribution of Rebate Amounts with histogram and KDE 
plt.figure(figsize=(10, 6))
sns.histplot(
    data=df,
    x='Rebate_Amount',
    kde=True,  # Adds a smoothed line
    bins=20,
    color='skyblue',
    edgecolor='black'
)
plt.title('Distribution of Rebate Amounts (Histogram + KDE)')
plt.xlabel('Rebate Amount (USD)')
plt.ylabel('Frequency')
plt.grid(axis='y', linestyle='--', alpha=0.6)
plt.show()








