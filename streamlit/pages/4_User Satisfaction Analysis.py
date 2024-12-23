import streamlit as st

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

from sklearn.decomposition import PCA
from sklearn.preprocessing import StandardScaler
from sklearn.cluster import KMeans
from sklearn.metrics import euclidean_distances
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error, r2_score

import sys
sys.path.append("../scripts")

import data_preprocessing as dp
import data_cleaning      as dc
import data_visualization as dv
import data_extraction    as de
import task1
import task2
import task3
import task4

st.title("User Satisfaction Analysis")

st.write("""
    **Objective**: Measure and predict user satisfaction based on engagement and experience.

    - **Activities Completed**:
      - Assigned engagement and experience scores using Euclidean distance from clustering results.
      - Calculated satisfaction scores as the average of engagement and experience scores.
      - Built a regression model to predict satisfaction scores.
      - Applied k-means clustering to satisfaction and experience scores.
      - Exported the final dataset with scores to a local MySQL database.

    **Outcome**: Developed a comprehensive model to assess and predict user satisfaction, providing valuable insights into customer contentment and areas for improvement.
    """)

st.write(""" ## Key Findings and Insights""")

# Load data from postgres database
query = 'select * from xdr_data;'
df = de.load_data_from_postgres(query)

# Copy the data for manipulation
df_engagement = df.copy()

# Aggregate the engagement metrics
df_engagement_grouped = task1.aggregation(df_engagement)

# Filter the engagement metrics
df_engagement_metrics = task2.engagement_metrics(df_engagement_grouped)

# K means clustering
task2.kmeans_clustering(df_engagement_metrics)

#Cluster summary
df_cluster_summary = df_engagement_metrics.groupby('cluster').agg({'sessions_frequency': ['min','max','mean','sum'],
                                                  'session_duration': ['min','max','mean','sum'],
                                                  'total_traffic': ['min','max','mean','sum']})

centroids = task2.centroids(df_engagement_metrics)

# Calculate the engagement score as the euclidean distance between the user data points and the less engaged cluster
df_engagement_metrics['engagement_score'] = euclidean_distances(df_engagement_metrics[['sessions_frequency','session_duration','total_traffic']],
                                                                [centroids[1]])

# Copy the dataframe
df_experience = df.copy()

# Filter the data for analysis
df_experience = task3.filter_data(df_experience)

#Replace missing values
task3.replace_with_median(df_experience)

# Aggregate the data
df_experience_metrics = task3.experience_metrics(df_experience)

# K means clustering
task3.kmeans_clustering(df_experience_metrics)

#Cluster summary
df_cluster_summary = df_experience_metrics.groupby('cluster').agg({'total_TCP_vol': ['min','max','mean','sum'],
                                                  'total_RTT_vol': ['min','max','mean','sum'],
                                                  'total_throughput_speed': ['min','max','mean','sum']})

centroids_1 = task3.centroids(df_experience_metrics)

# Calculate the engagement score as the euclidean distance between the user data points and the less engaged cluster

df_experience_metrics['experience_score'] = euclidean_distances(df_experience_metrics[['total_TCP_vol','total_RTT_vol','total_throughput_speed']],
                                                                [centroids_1[1]])

df_experience_metrics['experience_score'] = euclidean_distances(df_experience_metrics[['total_TCP_vol','total_RTT_vol','total_throughput_speed']],
                                                                [centroids[1]])

# Merge
df_merged = pd.merge(df_engagement_metrics,df_experience_metrics,on='MSISDN/Number',how='inner')

#Filter only the required columns
df_final = df_merged[['MSISDN/Number','engagement_score','experience_score']]

#Calculate the satisfaction score as the mean of engagement and experience score
df_final['satisfaction_score'] = df_final[['engagement_score','experience_score']].mean(axis=1)

st.write(""" **Final data with Engagement, Experience and Satisfaction score** """)
st.dataframe(df_final)

st.write(""" **Correlation between Engagement, Experience and Satisfaction score** """)

#Correlation
columns =['engagement_score','experience_score','satisfaction_score']
correlation = df_final[columns].corr()
fig3, axes = plt.subplots(figsize=(12, 8))
sns.heatmap(correlation, annot=True, cmap='coolwarm', fmt=".2f")

st.pyplot(fig3)
st.write(""" 
        - Satisfaction is strongly related with engagement 
        - Satisfaction is postively related with experience
        - Both experience and engagement are postively related""")

st.write("""
        ## Recommendations
        -  Since user experience are paramount for user satisfaction work on improving user experience.
""")
