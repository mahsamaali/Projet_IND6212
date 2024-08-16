import data_preprocess
import pandas as pd

file_location='data/data-3mois-2011.csv'

# Reading Data using Pandas
data = pd.read_csv(filepath_or_buffer=file_location, encoding ='utf-8',engine='python')
data=data_preprocess.data_cleaning(data)
data2=data_preprocess.vader_sentiment_analysis(data)
new_df=data_preprocess.feature_engineering(data2)

# Visualisation sentiment analysing
data_preprocess.exploratory_data_analysis(new_df)
data2.to_csv('data/result_score_3mois.csv')
