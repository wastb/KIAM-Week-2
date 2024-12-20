import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
from sklearn.decomposition import PCA
from sklearn.preprocessing import StandardScaler

def aggregation(df):
         
        # Group and calculate the total values
        df['total_youtube_data'] = df['Youtube DL (Bytes)'] + df['Youtube UL (Bytes)']
        df['total_social_media_data'] = df['Social Media DL (Bytes)'] + df['Social Media UL (Bytes)']
        df['total_netflix_data'] = df['Netflix DL (Bytes)'] + df['Netflix UL (Bytes)']
        df['total_google_data'] = df['Google DL (Bytes)'] + df['Google UL (Bytes)']
        df['total_email_data'] = df['Email DL (Bytes)'] + df['Email UL (Bytes)']
        df['total_gaming_data'] = df[ 'Gaming DL (Bytes)'] + df['Gaming UL (Bytes)']
        df['total_other_data'] = df[ 'Other UL (Bytes)'] + df['Other DL (Bytes)']
        df['total_data'] = df['Total UL (Bytes)'] + df['Total DL (Bytes)']

        df_aggregated = df.groupby(['MSISDN/Number']).agg(xDR_sessions=('Bearer Id', 'count'), session_duration = ('Dur. (ms)', 'sum'), total_DL=('Total DL (Bytes)','sum'),
                                                    total_UL=('Total UL (Bytes)','sum'), total_social_media = ('total_social_media_data', 'sum'),  total_youtube = ('total_youtube_data', 'sum'),
                                                    total_Netflix = ('total_netflix_data', 'sum'), total_Google = ('total_google_data', 'sum'),
                                                    total_Email = ('total_email_data', 'sum'),
                                                    total_Gaming = ('total_gaming_data', 'sum'), total_Other= ('total_other_data', 'sum'),
                                                    total_data = ('total_data','sum')).reset_index()
        return df_aggregated

def pca(df_aggregated):
    # Dimensionality Reduction - PCA
    columns = ['total_social_media', 'total_youtube', 'total_Netflix',
               'total_Google', 'total_Email', 'total_Gaming', 'total_Other']

    scaler = StandardScaler()
    scaled_features = scaler.fit_transform(df_aggregated[columns])

    pca = PCA(n_components=2)
    pca_result = pca.fit_transform(scaled_features)

    pca_df = pd.DataFrame(data=pca_result, columns=['PC1', 'PC2'])
    plt.figure(figsize=(8, 6))
    sns.scatterplot(x=pca_df['PC1'], y=pca_df['PC2'])
    plt.title('PCA Result')
    plt.xlabel('Principal Component 1')
    plt.ylabel('Principal Component 2')
    plt.show()