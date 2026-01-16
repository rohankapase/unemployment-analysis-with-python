import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px

# 1. Load the datasets
# We will use the more comprehensive dataset for regional and coordinate analysis
df = pd.read_csv('Unemployment_Rate_upto_11_2020.csv')

# 2. Data Cleaning
# Removing leading/trailing spaces from column names
df.columns = df.columns.str.strip()

# Convert 'Date' to datetime objects
df['Date'] = pd.to_datetime(df['Date'], dayfirst=True)

# Adding Month column for easier time-series analysis
df['Month'] = df['Date'].dt.month_name()

# 3. Exploratory Data Analysis (EDA)
print("Dataset Overview:")
print(df.info())
print("\nSummary Statistics:")
print(df.describe())

# 4. Visualizations

# A. Unemployment Rate Over Time
plt.figure(figsize=(12, 6))
sns.lineplot(data=df, x='Date', y='Estimated Unemployment Rate (%)')
plt.title('Trend of Unemployment Rate in India (2020)')
plt.xlabel('Date')
plt.ylabel('Unemployment Rate (%)')
plt.grid(True)
plt.show()

# B. Regional Analysis (Average Unemployment Rate per Region)
region_stats = df.groupby('Region')['Estimated Unemployment Rate (%)'].mean().reset_index()
fig = px.bar(region_stats, x='Region', y='Estimated Unemployment Rate (%)', 
             title='Average Unemployment Rate by State',
             color='Region')
fig.show()

# C. Impact of COVID-19 (Before vs During Lockdown)
# Identifying April-May 2020 as the peak lockdown period
lockdown_df = df[(df['Date'] >= '2020-04-01') & (df['Date'] <= '2020-07-01')]
before_lockdown_df = df[(df['Date'] < '2020-04-01')]

print(f"Avg Unemployment before lockdown: {before_lockdown_df['Estimated Unemployment Rate (%)'].mean():.2f}%")
print(f"Avg Unemployment during lockdown: {lockdown_df['Estimated Unemployment Rate (%)'].mean():.2f}%")

# D. Geospatial Analysis (Using Latitude and Longitude)
fig = px.scatter_geo(df, lat='latitude', lon='longitude', color="Region",
                     hover_name="Region", size="Estimated Unemployment Rate (%)",
                     animation_frame="Month",
                     scope='asia', title='Impact of Lockdown on Employment Across India')
fig.update_geos(lataxis_range=[5, 38], lonaxis_range=[65, 100])
fig.show()
