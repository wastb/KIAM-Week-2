import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd



def correlation(df):
   columns =['total_social_media', 'total_youtube', 'total_Netflix',
       'total_Google', 'total_Email', 'total_Gaming', 'total_Other']
   correlation = df[columns].corr()

   sns.heatmap(correlation, annot=True, cmap='coolwarm', fmt=".2f")

   