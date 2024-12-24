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


st.title('User Overview Analysis')

st.write("""
    **Objective**: Understand user behavior and device preferences.

    - **Activities Completed**:
      - Identified the top 10 handsets used by customers.
      - Determined the top 3 handset manufacturers and the top 5 handsets for each manufacturers.
      - Aggregated user data on session frequency, duration, and total data usage.
      - Conducted exploratory data analysis, including descriptive statistics, variable transformations, and graphical univariate analysis.
      - Performed bivariate and correlation analysis and dimensionality reduction using principal component analysis.

    **Outcome**: Provided insights into device popularity and user behavior, helping to understand user preferences and potential areas for targeted marketing.
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

# Top 10 handset Type
st.write(""" ***Top 10 Handset Types*** """)
st.table(df['Handset Type'].value_counts().nlargest(10).reset_index())

## Top 3 Handset manufacturer's

st.write(""" ***Top 3 Handset Manufacturers*** """)
st.table(df['Handset Manufacturer'].value_counts().nlargest(3).reset_index())

## task 1

# aggregated data
df_aggregated = task1.aggregation(df)

# Scatter Plot
st.write("""***Relationship between each application & the total (DL+UL) data*** """)
fig, axes = plt.subplots(2, 2, figsize=(12, 8))
sns.scatterplot(data=df_aggregated, y=df['total_data'], x= df_aggregated['total_social_media'],ax=axes[0, 0])
sns.scatterplot(data=df_aggregated, y=df_aggregated['total_data'], x= df_aggregated['total_youtube'],ax=axes[0, 1])
sns.scatterplot(data=df_aggregated, y=df_aggregated['total_data'], x= df_aggregated['total_Netflix'],ax=axes[1, 0])
sns.scatterplot(data=df_aggregated, y=df_aggregated['total_data'], x= df_aggregated['total_Google'],ax=axes[1, 1])
st.pyplot(fig)

fig2, axes = plt.subplots(2, 2, figsize=(12, 8))
sns.scatterplot(data=df_aggregated, y=df_aggregated['total_data'], x= df_aggregated['total_Email'],ax=axes[0, 0])
sns.scatterplot(data=df_aggregated, y=df_aggregated['total_data'], x= df_aggregated['total_Gaming'],ax=axes[0, 1])
sns.scatterplot(data=df_aggregated, y=df_aggregated['total_data'], x= df_aggregated['total_Other'],ax=axes[1, 0])

st.pyplot(fig2)

st.write(""" The scatter plot shows a postive relationship between application data and total data volume.""")

#Correlation
columns =['total_social_media', 'total_youtube', 'total_Netflix',
       'total_Google', 'total_Email', 'total_Gaming', 'total_Other']
correlation = df_aggregated[columns].corr()
fig3, axes = plt.subplots(figsize=(12, 8))
sns.heatmap(correlation, annot=True, cmap='coolwarm', fmt=".2f")

st.write(""" ***Correlation matrix*** """)
st.pyplot(fig3)
st.write(""" There is a positive relationship between each application data usage, customers are likely to use multiple applications at the same time""")


# PCA analysis
# Dimensionality Reduction - PCA
columns = ['total_social_media', 'total_youtube', 'total_Netflix',
               'total_Google', 'total_Email', 'total_Gaming', 'total_Other']

scaler = StandardScaler()
scaled_features = scaler.fit_transform(df_aggregated[columns])

pca = PCA(n_components=2)
pca_result = pca.fit_transform(scaled_features)

pca_df = pd.DataFrame(data=pca_result, columns=['PC1', 'PC2'])

fig4, axes = plt.subplots(figsize=(12, 8))
sns.scatterplot(x=pca_df['PC1'], y=pca_df['PC2'])
plt.title('PCA Result')
plt.xlabel('Principal Component 1')
plt.ylabel('Principal Component 2')
plt.show()

st.write(""" ***PCA Analysis*** """)
st.pyplot(fig4)
st.write(""" In the above PCA scatterplot a significant portion of the data lies close to the mean or does not vary dramatically""")

st.write("""
        ## Recommendations
        -  Launch a marketing campaign by partnering with the Top 3 Handset Manufacturers.
        -  Offer customized packages for the Top 10 Handset types.
        -  Partner with application companies to offer a premium package to customers.
""")






