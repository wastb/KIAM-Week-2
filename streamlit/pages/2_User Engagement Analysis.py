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


st.title('User Engagement Analysis')

st.write("""
    **Objective**: Assess user engagement to optimize resource allocation.

    - **Activities Completed**:
      - Aggregated engagement metrics per customer: session frequency, duration, and total traffic.
      - Normalized metrics and applied k-means clustering to classify users into engagement groups.
      - Analyzed top engaged users and derived engagement clusters.
      - Plotted top used applications and optimized k-value for clustering.

    **Outcome**: Identified highly-engaged users and applications, aiding in effective network resource allocation and marketing strategies.
    """)

st.write(""" ## Key Findings and Insights""")
# Load data from postgres database
query = 'select * from xdr_data;'
df = de.load_data_from_postgres(query)

# Drop duplicates
dc.drop_duplicates(df)

# Drop rows with all missing values
dc.drop_missing_rows(df)

# Drop columns containing more than 25% missing values
dc.drop_columns(df)

# Since Both  ['Avg RTT DL (ms)', 'Avg RTT UL (ms)'] columns are very skewed use median to replace missing values
dc.numerical_columns(df)

# The remaining columns contain insignificant number of missing values 
dc.drop_nan_values(df)

# Summary statistics shows outliers
dc.handle_outliers(df)

# aggregated data
df_aggregated = task1.aggregation(df)

# Extract engagement metrics from df_aggregated
df_engagement_metrics = task2.engagement_metrics(df_aggregated)

df_sess = df_engagement_metrics.nlargest(10, 'sessions_frequency').reset_index()
styled_df = df_sess[['MSISDN/Number','sessions_frequency']].style.format({'MSISDN/Number': '{:.0f}'}) 

# Top 10 Customers per Engagement Metric
st.write(""" ***Top 10 Engaged Users per session freqeuncy***""")
st.dataframe(styled_df)

df_dur = df_engagement_metrics.nlargest(10, 'session_duration')
styled_df1 = df_dur[['MSISDN/Number','session_duration']].style.format({'MSISDN/Number': '{:.0f}'})

st.write(""" ***Top 10 Engaged Users per session duration***""")
st.dataframe(styled_df1)


df_traff = df_engagement_metrics.nlargest(10, 'total_traffic')
styled_df2 = df_traff[['MSISDN/Number','total_traffic']].style.format({'MSISDN/Number': '{:.0f}'})

st.write(""" ***Top 10 Engaged Users per session traffic***""")
st.dataframe(styled_df2)

# K-means Clustering (k=3)
task2.kmeans_clustering(df_engagement_metrics)

df_cluster_summary = df_engagement_metrics.groupby('cluster').agg({'sessions_frequency': ['min','max','mean','sum'],
                                                  'session_duration': ['min','max','mean','sum'],
                                                  'total_traffic': ['min','max','mean','sum']})

st.write(""" ***K means clustering result***""")
st.dataframe(df_cluster_summary)
st.write(""" 
         **Customer's are grouped into 3 clusters:**
         
         - **Users in cluster_0 are less engaged out of the 3 clusters**
         - **Users in cluster_1 are highly engaged**
         - **Users in cluster_2 are medium**""")

# Aggregate Total Traffic per Application
applications = ['social_media', 'Google', 'Email', 'youtube', 'Netflix', 'Gaming', 'Other']
application_traffic = {}
for app in applications:
    traffic_col = f'total_{app}'
    app_traffic = df_aggregated.groupby('MSISDN/Number')[traffic_col].sum()
    application_traffic[app] = app_traffic.sum()

top_3_apps = sorted(application_traffic.items(), key=lambda x: x[1], reverse=True)[:3]
top_3_apps_df = pd.DataFrame(top_3_apps, columns=['Application', 'Total Traffic'])

#Plot Top 3 Most Used Applications
fig, axes = plt.subplots(figsize=(12, 8))
plt.bar(top_3_apps_df['Application'], top_3_apps_df['Total Traffic'], color=['blue', 'green', 'red'])
plt.title('Top 3 Most Used Applications (Total Traffic)')
plt.ylabel('Total Traffic (Bytes)')
plt.xlabel('Application')
plt.xticks(rotation=45)
plt.tight_layout()

st.write("""***Top 3 most used applications***""")
st.pyplot(fig)

# Optimal Number of Clusters using Elbow Method
inertia = []
for k in range(1, 11):
    # Normalize
    scaler = StandardScaler()
    metrics_scaled = scaler.fit_transform(df_engagement_metrics)
    #Kmeans
    kmeans = KMeans(n_clusters=k, random_state=0)
    kmeans.fit(metrics_scaled)
    inertia.append(kmeans.inertia_)

fig1, axes = plt.subplots(figsize=(12, 8))
plt.plot(range(1, 11), inertia, marker='o')
plt.title('Elbow Method for Optimal k')
plt.xlabel('Number of Clusters (k)')
plt.ylabel('Inertia')
plt.xticks(range(1, 11))
plt.grid(True)

st.write(""" ***Elbow Plot Analysis*** """)
st.pyplot(fig1)
st.write(""" The elbow plot analysis suggests that it would be beneficial to cluster users into 6 groups for optimal analysis""")

st.write("""
        ## Recommendations
        -  Offer loyalty services for the most engaged users.
        -  Promote special packages for Gaming and Youtube Usage.
        -  Group customers into 6 groups to analyze customer behaviour better.
""")