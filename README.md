# Investment Assessment: Data-Driven Insights on TellCo's Growth Potential

## Executive Summary

This project provides a comprehensive investment assessment of TellCo, a mobile service provider in the Republic of Pefkakia, to support a data-driven decision on its acquisition. By analyzing customer behavior, network usage, and engagement trends, this study uncovers opportunities to optimize profitability and operational efficiency.
## Project Overview

The objective of this project is to analyze the data provided by TellCo to identify opportunities for growth and to assess whether TellCo is a worthy investment. The analysis is divided into four primary tasks:

1. **User Overview Analysis**: Understanding customer behavior and usage patterns.
2. **User Engagement Analysis**: Evaluating user engagement metrics and clustering users based on engagement.
3. **Experience Analysis**: Analyzing user experience metrics, including network performance and device characteristics.
4. **Satisfaction Analysis**: Combining engagement and experience metrics to compute satisfaction scores and predict customer satisfaction.

## Dataset Description

- **Data Source**: xDR records from TellCo.
- **Attributes**: Includes user activity data on various applications (e.g., Social Media, Google, Email, YouTube, Netflix, Gaming) and network performance metrics (e.g., TCP retransmission, RTT, Throughput).
- **Schema**: Detailed description of attributes and SQL schema.

## Project Setup

### Prerequisites

- Python 3.8+
- PostgreSQL Database

### Installation

1. **Clone the Repository**:

    ```bash
    git clone https://github.com/wastb/KIAM-Week-2
    cd KIAM-Week-2
    ```

2. **Setup Virtual Environment**:

    ```bash
   python -m venv .venv
    ```

3. **Install Dependencies**:

    ```bash
    pip install -r requirements.txt
    ```

4. **Database Setup**:
    - Import the provided SQL schema into your PostgreSQL database.
    - Configure the connection settings in your project configuration files.

5. Streamlit App:

   - Streamlit dashboard can be found in streamlit/HomePage.py.
   - To run the Streamlit app locally, use the following command:

   ```bash
   streamlit run streamlit/HomePage.py
   ```
   
   - Once streamlite is running, access your Streamlit app at http:/localhost:8501.

## Tasks and Methodologies

### Task 1 - User Overview Analysis

- **Business Overview**: Understanding user behavior is crucial for any business aiming to enhance its offerings and tailor solutions to customer needs. This analysis provides insights into customer device preferences and usage patterns, which can drive targeted marketing strategies and product improvements.

- **Objective**: Conduct a comprehensive User Overview Analysis to identify the most popular handsets, manufacturers, and their usage patterns.
- **Sub-tasks**:
  - Identify Top 10 Handsets: Determine the top 10 handsets used by customers.
  - Identify Top 3 Manufacturers: Identify the top 3 handset manufacturers.
  - Analyze Top Handsets by Manufacturer: For each of the top 3 manufacturers, identify the top 5 handsets.
  - Interpretation and Recommendations: Provide insights and recommendations based on the analysis to inform marketing strategies.

- **Additional Analysis**:
  - Aggregate user data on xDR (data sessions) including:
    - Number of sessions
    - Session duration
    - Total download (DL) and upload (UL) data
    - Data volume per application
  - Perform Exploratory Data Analysis (EDA) to uncover insights and handle missing values and outliers.
    - Describe variables and data types
    - Segment users into deciles based on total session duration and compute total data per decile
    - Conduct univariate and bivariate analyses
    - Perform correlation analysis
    - Execute Principal Component Analysis (PCA) for dimensionality reduction and interpret results

### Task 2 - User Engagement Analysis

- **Business Overview**: Evaluating user engagement is essential for enhancing user experience and optimizing network resources. By understanding how frequently and for how long users engage with applications, businesses can tailor their offerings to improve user satisfaction and retention.

- **Objective**: Assess user engagement based on session frequency, duration, and traffic to optimize service quality and resource allocation.

- **Sub-tasks**:
  - Aggregate Engagement Metrics: Aggregate session frequency, duration, and total traffic per customer.
  - Engagement Clustering: Normalize metrics and use k-means clustering (k=3) to classify customers into engagement clusters.
  - Analyze Engagement Metrics: Compute and interpret non-normalized metrics for each cluster. Identify top engaged users and applications.
  - Visualize Engagement: Plot top 3 most used applications and identify the optimal number of clusters using the elbow method.

### Task 3 - Experience Analysis

- **Business Overview**: Analyzing user experience in the telecom industry involves assessing network performance and device characteristics. This helps in understanding user satisfaction related to network parameters and device performance, which is vital for improving service quality.

- **Objective**: Evaluate user experience based on network parameters and device characteristics to identify performance issues and areas for improvement.

- **Sub-tasks**:
  - Aggregate Experience Metrics: Collect average TCP retransmission, RTT, throughput, and handset type per customer. Handle missing values and outliers.
  - Top and Bottom Values: Identify the top 10, bottom 10, and most frequent values for TCP retransmission, RTT, and throughput.
  - Analyze Metrics by Handset Type: Compute and interpret the distribution of throughput and average TCP retransmission per handset type.
  - Experience Clustering: Perform k-means clustering (k=3) on experience metrics and describe each cluster based on data insights.

### Task 4 - Satisfaction Analysis

- **Business Overview**: Customer satisfaction is influenced by both engagement and experience. Analyzing satisfaction helps in identifying highly satisfied customers and improving service quality based on user feedback.

- **Objective**: Analyze customer satisfaction by combining engagement and experience metrics to predict satisfaction scores and identify areas for improvement.

- **Sub-tasks**:
  - Compute engagement and experience scores using Euclidean distance.
  - Build a regression model to predict satisfaction scores.
  - Perform clustering on satisfaction scores and export results.
  - Compute Scores: Assign engagement and experience scores to users using Euclidean distance. Compute average satisfaction scores.
  - Predict Satisfaction: Build a regression model to predict satisfaction scores.
  - Clustering: Perform k-means clustering (k=2) on engagement and experience scores. Aggregate and interpret average scores per cluster.
  - Export Data: Export the final table containing user IDs and scores to a local MySQL database. Provide a screenshot of the query output.
  - Model Tracking: Deploy and monitor the model using tools like Docker. Track and document model changes, metrics, and outputs.

### Dashboard Development

- **Objective**: Develop an interactive dashboard using Streamlit to visualize insights.
- **Features**:
  - User-friendly navigation and clear data visualizations.
  - Interactive widgets for data exploration.

- **Deliverables**:
  - Streamlit dashboard accessible via a public URL.

## Conclusion

This project aims to provide a comprehensive analysis of TellCo's telecom data, offering insights into user behavior, engagement, experience, and satisfaction. The findings will inform investment decisions and strategic recommendations. Through meticulous analysis and advanced visualization, we seek to enhance understanding and drive profitable investment outcomes.

## Contact

For any questions or further information, please contact [Wasihun Tesfaye](mailto:wasihunpersonal@gmail.com).
