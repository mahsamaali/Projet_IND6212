import pandas as pd
import numpy as np
import re
import nltk
from nltk.sentiment.vader import SentimentIntensityAnalyzer as SIA

import seaborn as sns
import matplotlib.pyplot as plt


def data_cleaning(df):

	#Selecting english tweets


	#df.to_csv('assets/dat_English.csv')

	# Remove twitter handlers
	df.content = df.content.apply(lambda x: re.sub('@[^\s]+', '', str(x)))

	# remove hashtags
	df.content  = df.content.apply(lambda x: re.sub(r'\B#\S+', '', str(x)))

	# Remove URLS
	df.content  = df.content.apply(lambda x: re.sub(r"http\S+", "", str(x)))

	# Remove all the special characters
	#df.content  = df.content.apply(lambda x: ' '.join(re.findall(r'\w+', x)))

	# remove all single characters
	df.content  = df.content.apply(lambda x: re.sub(r'\s+[a-zA-Z]\s+', '', str(x)))

	# Substituting multiple spaces with single space
	df.content  = df.content.apply(lambda x: re.sub(r'\s+', ' ', str(x), flags=re.I))

	df.drop_duplicates(['content'], keep="first", inplace=True)

	#df.to_csv('assets/dat_after_cleaning.csv')

	return df

def vader_sentiment_analysis(df):
	sid = SIA()
	df['sentiments'] = df['content'].apply(lambda x: sid.polarity_scores(' '.join(re.findall(r'\w+', x.lower()))))
	df['Positive Sentiment'] = df['sentiments'].apply(lambda x: x['pos'] + 1 * (10 ** -6))
	df['Neutral Sentiment'] = df['sentiments'].apply(lambda x: x['neu'] + 1 * (10 ** -6))
	df['Negative Sentiment'] = df['sentiments'].apply(lambda x: x['neg'] + 1 * (10 ** -6))
	df.drop(columns=['sentiments'], inplace=True)
	return df

def feature_engineering(df):
	# Number of Words
	df['Number_Of_Words'] = df.content.apply(lambda x: len(x.split(' ')))
	# Average Word Length
	df['Mean_Word_Length'] = df.content.apply(lambda x: np.round(np.mean([len(w) for w in x.split(' ')]), 2))

	return df

def exploratory_data_analysis(df):
	plt.subplot(2, 1, 1)
	plt.title('Distriubtion Of Sentiments Across Our Tweets', fontsize=12, fontweight='bold')
	sns.kdeplot(df['Negative Sentiment'], bw_method=0.1)
	sns.kdeplot(df['Positive Sentiment'], bw_method=0.1)
	sns.kdeplot(df['Neutral Sentiment'], bw_method=0.1)
	plt.subplot(2, 1, 2)
	plt.title('CDF Of Sentiments Across Our Tweets', fontsize=12, fontweight='bold')
	sns.kdeplot(df['Negative Sentiment'], bw_method=0.1, cumulative=True)
	sns.kdeplot(df['Positive Sentiment'], bw_method=0.1, cumulative=True)
	sns.kdeplot(df['Neutral Sentiment'], bw_method=0.1, cumulative=True)
	plt.xlabel('Sentiment Value', fontsize=12)
	plt.show()

def time_based_analysis(df):
	# Sorting And Feature Engineering
	df = df.sort_values(by='date')
	df =df.copy()
	df['date'] = pd.to_datetime(df['date']).dt.date

	df['year'] = pd.DatetimeIndex(df['date']).year
	df['month'] = pd.DatetimeIndex(df['date']).month
	df['day'] = pd.DatetimeIndex(df['date']).day
	df['day_of_year'] = pd.DatetimeIndex(df['date']).dayofyear
	df['quarter'] = pd.DatetimeIndex(df['date']).quarter
	df['season'] = df.month % 12 // 3 + 1

	return df


def time_analysing(df):
	#df = df.reset_index().drop(columns=['index'])
	partitions = []
	partitions.append(df.loc[44:np.round(len(df) / 3, 0) - 1, :])
	partitions.append(df.loc[np.round(len(df) / 3, 0):2 * int(len(df) / 3) - 1, :])
	partitions.append(df.loc[2 * np.round(len(df) / 3, 0):3 * int(len(df) / 3) - 1, :])

	neg_part_means = []
	neg_part_std = []
	pos_part_means = []
	pos_part_std = []
	for part in partitions:
		neg_part_means.append(part['Negative Sentiment'].mean())
		neg_part_std.append(part['Negative Sentiment'].std())
		pos_part_means.append(part['Positive Sentiment'].mean())
		pos_part_std.append(part['Positive Sentiment'].std())

	result_df = pd.DataFrame({'Positive Sentiment Mean': pos_part_means, 'Negative Sentiment Mean': neg_part_means,
	                       'Positive Sentiment SD': pos_part_std, 'Negative Sentiment SD': neg_part_std},
	                      index=[f'Partition_{i}' for i in range(1, 4)])
	# res_df.style.apply(highlight_greater,axis=None)
	result_df = result_df.T
	result_df = pd.DataFrame(result_df.values, columns=result_df.columns,
	                      index=['Positive Sentiment', 'Negative Sentiment', 'Positive Sentiment',
	                             'Negative Sentiment'])
	result_df = pd.concat([result_df.iloc[:2, :], result_df.iloc[2:, :]], axis=1)
	result_df.columns = ['Partition_1_Mean', 'Partition_2_Mean', 'Partition_3_Mean', 'Partition_1_SD', 'Partition_2_SD',
	                  'Partition_3_SD']

	result_df.style.apply(highlight_greater, axis=None)

	return result_df


def highlight_greater(x):
		temp = x.copy()
		temp = temp.round(0).astype(int)
		m1 = (temp['Partition_1_Mean'] == temp['Partition_2_Mean'])
		m2 = (temp['Partition_1_SD'] == temp['Partition_2_SD'])
		m3 = (temp['Partition_1_Mean'] < temp['Partition_2_Mean'] + 3) & (
					temp['Partition_1_Mean'] > temp['Partition_2_Mean'] - 3)
		m4 = (temp['Partition_1_SD'] < temp['Partition_2_SD'] + 3) & (
					temp['Partition_1_SD'] > temp['Partition_2_SD'] - 3)

		df = pd.DataFrame('background-color: ', index=x.index, columns=x.columns)
		# rewrite values by boolean masks
		df['Partition_1_Mean'] = np.where(~m1, 'background-color: {}'.format('salmon'), df['Partition_1_Mean'])
		df['Partition_2_Mean'] = np.where(~m1, 'background-color: {}'.format('salmon'), df['Partition_2_Mean'])
		df['Partition_1_Mean'] = np.where(m3, 'background-color: {}'.format('gold'), df['Partition_1_Mean'])
		df['Partition_2_Mean'] = np.where(m3, 'background-color: {}'.format('gold'), df['Partition_2_Mean'])
		df['Partition_1_Mean'] = np.where(m1, 'background-color: {}'.format('mediumseagreen'), df['Partition_1_Mean'])
		df['Partition_2_Mean'] = np.where(m1, 'background-color: {}'.format('mediumseagreen'), df['Partition_2_Mean'])

		df['Partition_1_SD'] = np.where(~m2, 'background-color: {}'.format('salmon'), df['Partition_1_SD'])
		df['Partition_2_SD'] = np.where(~m2, 'background-color: {}'.format('salmon'), df['Partition_2_SD'])
		df['Partition_1_SD'] = np.where(m4, 'background-color: {}'.format('gold'), df['Partition_1_SD'])
		df['Partition_2_SD'] = np.where(m4, 'background-color: {}'.format('gold'), df['Partition_2_SD'])
		df['Partition_1_SD'] = np.where(m2, 'background-color: {}'.format('mediumseagreen'), df['Partition_1_SD'])
		df['Partition_2_SD'] = np.where(m2, 'background-color: {}'.format('mediumseagreen'), df['Partition_2_SD'])

		return df



