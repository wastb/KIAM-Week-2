import pandas as pd
import numpy as np

from sklearn.preprocessing import StandardScaler
from sklearn.cluster import KMeans

def replace_with_median(df):  
        #Replace missing values with mean
        numerical_cols = ['TCP UL Retrans. Vol (Bytes)','TCP DL Retrans. Vol (Bytes)', 'Avg RTT DL (ms)',
                          'Avg RTT UL (ms)','Avg Bearer TP DL (kbps)','Avg Bearer TP UL (kbps)']
        
        df[numerical_cols] = df[numerical_cols].fillna(df[numerical_cols].median())
        print(f"Numerical columns: {numerical_cols} replaced with the median value")
        

def filter_data(df):
        df = df[['MSISDN/Number', 'TCP UL Retrans. Vol (Bytes)','TCP DL Retrans. Vol (Bytes)', 
        'Avg RTT DL (ms)', 'Avg RTT UL (ms)','Avg Bearer TP DL (kbps)','Avg Bearer TP UL (kbps)','Handset Type']]

        return df

def experience_metrics(df):
        # Aggregate the data for experience anlysis
        df['total_TCP'] = df['TCP DL Retrans. Vol (Bytes)'] + df['TCP UL Retrans. Vol (Bytes)']
        df['total_RTT'] = df['Avg RTT DL (ms)'] + df['Avg RTT UL (ms)']
        df['total_throughput'] = df['Avg Bearer TP DL (kbps)'] + df['Avg Bearer TP UL (kbps)']

        df_experience_metrics = df.groupby(['MSISDN/Number','Handset Type']).agg(total_TCP_vol = ('total_TCP','sum'), 
                                                                                    total_RTT_vol = ('total_RTT','sum'),
                                                                                    total_throughput_speed = ('total_throughput','sum')
                                                                                ).reset_index()
        return df_experience_metrics  


def kmeans_clustering(df_experience_metrics):
        # K means clustering
        #Normalizarion
        features = df_experience_metrics[['total_TCP_vol','total_RTT_vol','total_throughput_speed']]
        scaler = StandardScaler()
        metrics_scaled = scaler.fit_transform(features)

        # K-means Clustering (k=3)
        kmeans = KMeans(n_clusters=3, random_state=0)
        df_experience_metrics['cluster'] = kmeans.fit_predict(metrics_scaled)