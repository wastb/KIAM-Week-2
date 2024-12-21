import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

from sklearn.preprocessing import StandardScaler
from sklearn.cluster import KMeans

def engagement_metrics(df_aggregated):
    # Extract engagement metrics from df_aggregated
    df_engagement_metrics = pd.DataFrame()

    df_engagement_metrics['MSISDN/Number'] =df_aggregated['MSISDN/Number']
    df_engagement_metrics['sessions_frequency'] = df_aggregated['xDR_sessions']
    df_engagement_metrics['session_duration'] = df_aggregated['session_duration']
    df_engagement_metrics['total_traffic'] = df_aggregated['total_data']
 
    return df_engagement_metrics

def top_10_customers(df_engagement_metrics):
    # Top 10 Customers per Engagement Metric

    top_10_session_frequency = df_engagement_metrics.nlargest(10, 'sessions_frequency')
    top_10_session_duration = df_engagement_metrics.nlargest(10, 'session_duration')
    top_10_total_traffic = df_engagement_metrics.nlargest(10, 'total_traffic')
    print("Top 10 Customers by Session Frequency:\n", top_10_session_frequency)
    print("Top 10 Customers by Session Duration:\n", top_10_session_duration)
    print("Top 10 Customers by Total Download:\n", top_10_total_traffic)

def kmeans_clustering(df_engagement_metrics):

    #Normalizarion
    scaler = StandardScaler()
    metrics_scaled = scaler.fit_transform(df_engagement_metrics)

    # K-means Clustering (k=3)
    kmeans = KMeans(n_clusters=3, random_state=0)
    df_engagement_metrics['cluster'] = kmeans.fit_predict(metrics_scaled)

    return df_engagement_metrics
