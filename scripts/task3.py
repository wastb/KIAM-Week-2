import pandas as pd
import numpy as np

def replacce_with_medain(df):  
        #Replace missing values with mean
        numerical_cols = ['TCP UL Retrans. Vol (Bytes)','TCP DL Retrans. Vol (Bytes)', 'Avg RTT DL (ms)',
                          'Avg RTT UL (ms)','Avg Bearer TP DL (kbps)','Avg Bearer TP UL (kbps)']
        
        df[numerical_cols] = df[numerical_cols].fillna(df[numerical_cols].median())
        print(f"Numerical columns: {numerical_cols} replaced with the median value")