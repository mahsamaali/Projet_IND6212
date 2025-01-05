
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

import data_preprocess

sns.set(style='darkgrid', context='talk', palette='Dark2')

from nltk.sentiment.vader import SentimentIntensityAnalyzer
import nltk
nltk.download('vader_lexicon')


# File Location and Selected Columns
file_location = 'data/data1.csv'
cols = [1]

# Reading Data using Pandas
data = pd.read_csv(filepath_or_buffer=file_location, encoding ='utf-8',engine='python')
data=data_preprocess.data_cleaning(data)

# Labeling Our Data
sia = SentimentIntensityAnalyzer()
results = []

for item in data['content']:
    pol_score = sia.polarity_scores(item)
    pol_score['Score'] = item
    results.append(pol_score)


# DataFrames
data = pd.DataFrame.from_records(results)

# Creating Label
data['label'] = "Neutral"
data.loc[data['compound'] > 0.2, 'label'] = "Positive"
data.loc[data['compound'] < -0.2, 'label'] = "Negative"


data2 = data[['Score', 'label']]


data2.to_csv('data/result.csv')
