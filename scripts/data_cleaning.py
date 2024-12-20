import pandas as pd
import numpy as np

def drop_duplicates(df):
        # Drop duplicates if there's any
        df.drop_duplicates(inplace=True)
        print("Duplicate values removed")


def drop_missing_rows(df):
        
        # Drop rows where all values are missing
        df.dropna(how='all', inplace=True)
        print("Rows with all missing values dropped.")
    
def drop_columns(df):

        # Calculate the percentage of missing values
        missing_percentage = df.isnull().sum() * 100 / len(df)
        threshold = 25

        # Drop columns with missing percentage greater than the threshold
        columns_to_drop = [col for col in df.columns if missing_percentage[col] > threshold]
        df.drop(columns=columns_to_drop, axis=1, inplace=True)
        print(f"Columns dropped due to high percentage of missing values: {columns_to_drop}")

def numerical_columns(df):  
        #Replace missing values with mean
        numerical_cols = ['Avg RTT DL (ms)', 'Avg RTT UL (ms)']
        df[numerical_cols] = df[numerical_cols].fillna(df[numerical_cols].median())
        print(f"Numerical columns: {numerical_cols} replaced with the median value")

def drop_nan_values(df):
       #Drop all missing values in every row
       df.dropna(axis=0, inplace=True)
       print(f"Missing rows droped")

def handle_outliers(df):
        
    #Handles outliers in a DataFrame using the IQR method by capping them.

    df = df.copy()  # Create a copy to avoid modifying the original DataFrame
    columns = ['Dur. (ms)', 'Avg RTT DL (ms)',
       'Avg RTT UL (ms)', 'Avg Bearer TP DL (kbps)', 'Avg Bearer TP UL (kbps)',
       'DL TP < 50 Kbps (%)', '50 Kbps < DL TP < 250 Kbps (%)',
       '250 Kbps < DL TP < 1 Mbps (%)', 'DL TP > 1 Mbps (%)',
       'UL TP < 10 Kbps (%)', '10 Kbps < UL TP < 50 Kbps (%)',
       '50 Kbps < UL TP < 300 Kbps (%)', 'UL TP > 300 Kbps (%)',
       'Activity Duration DL (ms)', 'Activity Duration UL (ms)', 'Dur. (ms).1',
       'Nb of sec with Vol DL < 6250B',
       'Nb of sec with Vol UL < 1250B', 'Social Media DL (Bytes)',
       'Social Media UL (Bytes)', 'Google DL (Bytes)', 'Google UL (Bytes)',
       'Email DL (Bytes)', 'Email UL (Bytes)', 'Youtube DL (Bytes)',
       'Youtube UL (Bytes)', 'Netflix DL (Bytes)', 'Netflix UL (Bytes)',
       'Gaming DL (Bytes)', 'Gaming UL (Bytes)', 'Other DL (Bytes)',
       'Other UL (Bytes)', 'Total UL (Bytes)', 'Total DL (Bytes)']
    
    for col in columns:
        # Calculate Q1, Q3, and IQR
        Q1 = df[col].quantile(0.25)
        Q3 = df[col].quantile(0.75)
        IQR = Q3 - Q1
        
        # Determine the lower and upper bounds
        lower_bound = Q1 - 1.5 * IQR
        upper_bound = Q3 + 1.5 * IQR
        
        # Cap the outliers
        df[col] = np.where(df[col] < lower_bound, lower_bound, df[col])
        df[col] = np.where(df[col] > upper_bound, upper_bound, df[col])
    
    
