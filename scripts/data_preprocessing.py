import pandas as pd
import matplotlib.pyplot as plt


def load_data(path):

     #Load a CSV file

     try:
       return pd.read_csv(path)
     except:
         print("Please insert an apropriate CSV file path")
    
def information(df):
    
    # Print General information about the data

    print(f"Rows: {df.shape[0]}, Columns: {df.shape[1]}")
    print(df.info())
    
def check_for_missing_values(df):
    
    """ Check for missing values """
    
    return df.isnull().sum()

def statistical_summary(df):
    # Summary statistics
    return df.describe()

    
    
    

    