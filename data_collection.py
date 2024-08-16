import os
import pandas as pd
import ast
import glob

# Setting variables to be used in format string command below
def get_data(tweet_count,since_date,until_date):

	text_query = "#oilprice OR #CrudeOil OR #fuelprices OR #oil OR #OOTT OR #opec OR #oilbusiness"


	# Using OS library to call CLI commands in Python
	os.system(
		'snscrape --jsonl  --since {} twitter-search "{} until:{}" > assets/dataOil.json'.format(since_date,
		                                                                                                  text_query,
		                                                                                                  until_date))
	file_csv='assets/{}.csv'.format(until_date)

	tweets_df1 = pd.read_json('assets/dataOil.json', lines=True)




	#save emglish tweets
	tweets_df1=tweets_df1.loc[tweets_df1['lang'] == 'en']
	tweets_df1=delete_column(tweets_df1)
	tweets_df1.to_csv(file_csv, sep=',', index=False)
	return tweets_df1
	#print("Before return \n",len(tweets_df1))



def delete_column(df):
	df.drop(['_type','id','lang' ,'url','renderedContent','conversationId','inReplyToUser','source','sourceUrl','sourceLabel','outlinks','tcooutlinks','media','mentionedUsers','coordinates','place'], axis=1, inplace=True)
	#df.to_csv('assets/data_raw_after_del.csv', sep=',', index=False)
	return df


def user_scan(df):
	user_df=df.user
	user_dict = {}

	for i in range(len(user_df)):
		user_dict[i] = user_df[i]

	return user_dict


def merge_csv():
	# 1. defines path to excel files
	path = "data/"

	# 2. creates list with excel files to merge based on name convention
	file_list = [path + f for f in os.listdir(path) if f.startswith('week')]

	# 3. creates empty list to include the content of each file converted to pandas DF
	excel_list = []

	# 4. reads each (sorted) file in file_list, converts it to pandas DF and appends it to the excel_list
	for file in sorted(file_list):
		df_clean = pd.read_csv(filepath_or_buffer=file, encoding ='utf-8',skiprows=1)
		excel_list.append(df_clean.assign(File_Name=os.path.basename(file)))

	# 5. merges single pandas DFs into a single DF, index is refreshed
	excel_merged = pd.concat(excel_list, ignore_index=True)

	# 6. Single DF is saved to the path in Excel format, without index column
	excel_merged.to_csv(path + 'tweets.csv', index=False)

def merge_csv_2():
	os.chdir("data/")
	extension = 'csv'
	all_filenames = [i for i in glob.glob('*.{}'.format(extension))]
	# combine all files in the list
	combined_csv = pd.concat([pd.read_csv(filepath_or_buffer=f,dtype={"user_id": int, "username": "string"} ,encoding ='utf-8') for f in all_filenames])
	# export to csv
	combined_csv.to_csv("combined_csv.csv", index=False, encoding='utf-8')