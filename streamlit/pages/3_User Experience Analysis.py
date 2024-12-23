import streamlit as st

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

from sklearn.decomposition import PCA
from sklearn.preprocessing import StandardScaler
from sklearn.cluster import KMeans

import sys
sys.path.append("../scripts")

import data_preprocessing as dp
import data_cleaning      as dc
import data_visualization as dv
import data_extraction    as de
import task1
import task2
import task3

st.title("User Experience Analysis")

st.write("""
    **Objective**: Evaluate user experience based on network performance and device characteristics.

    - **Activities Completed**:
      - Aggregated data on TCP retransmission, RTT, throughput, and handset type.
      - Computed and listed top, bottom, and frequent values for TCP, RTT, and throughput.
      - Analyzed throughput and TCP retransmission by handset type.
      - Applied k-means clustering to segment users based on experience metrics.

    **Outcome**: Provided a detailed understanding of user experience and device performance, enabling targeted improvements in network quality.
    """)

st.write(""" ## Key Findings and Insights""")

# Load data from postgres database
query = 'select * from xdr_data;'
df = de.load_data_from_postgres(query)

#Split the data for analysis
df = task3.filter_data(df)

# The data skewed let's replace it with the median of the corresponding column
task3.replace_with_median(df)

# Drop other missing values
dc.drop_nan_values(df)

#Drop duplicates
dc.drop_duplicates(df)

# Aggregate the data for user experience analysis
df_experience_metrics = task3.experience_metrics(df)



df_sess = df_experience_metrics.nlargest(10,'total_TCP_vol').reset_index()
styled_df = df_sess[['MSISDN/Number','total_TCP_vol']].style.format({'MSISDN/Number': '{:.0f}'}) 

# Top 10 TCP values
st.write(""" ***Top 10 TCP values***""")
st.dataframe(styled_df)

df_sess1 = df_experience_metrics.nsmallest(10,'total_TCP_vol').reset_index()
styled_df1 = df_sess1[['MSISDN/Number','total_TCP_vol']].style.format({'MSISDN/Number': '{:.0f}'}) 

# Top 10 TCP values
st.write(""" ***Bottom 10 TCP values***""")
st.dataframe(styled_df1)

df_sess2 = df_experience_metrics['total_TCP_vol'].mode().reset_index()


# Top 10 TCP values
st.write(""" ***Mode***""")
st.dataframe(df_sess2)

# Average Throughput per handset type
df_throughput_average = df_experience_metrics.groupby('Handset Type')['total_throughput_speed'].mean()

# Plot Average Throughput distribution
fig, axes = plt.subplots(figsize=(12, 6))
plt.hist(df_throughput_average, bins=30, edgecolor='k', alpha=0.7)
plt.title('Average Throughput distribution per Handset Type')
plt.xlabel('Average Throughput Speed')
plt.ylabel('Frequency')
plt.grid(True)

st.write(""" ***Average throughput distribution*** """)
st.pyplot(fig)
st.write(""" 
        **The average throughput distribution shows:**
        - Most of the Handset Types experience a throughput speed beetween 0 - 25000 kbps
        - The most prevalent throughput range is between 0 - 5000 kbps
        - Eventhough larger througput speeds exist they're significantly small""")

# Average TCP volume per handset type
df_TCP_average = df_experience_metrics.groupby('Handset Type')['total_TCP_vol'].mean()

# Plot Average TCP distribution
fig1,axes = plt.subplots(figsize=(12, 6))
plt.hist(df_TCP_average, bins=30, edgecolor='k', alpha=0.7)
plt.title('Average TCP volume per Handset Type')
plt.xlabel('Average TCP volume')
plt.ylabel('Frequency')
plt.grid(True)

st.write(""" ***Average TCP retransmission distribution*** """)
st.pyplot(fig1)
st.write(""" **The TCP distribution shows:**
- The Average TCP volume for almost all device type is less than 100MB""")

st.write("""
        ## Recommendations
        - **To improve user experience:**
            -  Increase the throughput speed.
            -  Decrease the volume of TCP retransmission.
""")

