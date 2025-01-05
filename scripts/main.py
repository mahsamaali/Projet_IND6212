import data_collection
import data_preprocess as process
import pandas as pd






# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    nb_tweets=100
    since_date = "2020-03-01"
    until_date = "2020-04-02"
    #until_date = "2020-05-31"


    #getTweets base on the date
    df=data_collection.get_data(nb_tweets,since_date,until_date)

    #Merge data csv
    # data_collection.merge_csv()

    #Read file csv file containing emjois
    #file='assets/dataOil.csv'
    #file_emoji='assets/dat_English.csv'
    #df=pd.read_csv(filepath_or_buffer=file, encoding ='utf-8')

    #prepare data (deleting cols, clean data)

    #df=process.data_cleaning(df)


    #sentiment analysis
    #df=process.vader_sentiment_analysis(df)
    #new_df=process.feature_engineering(df)

    #Visualisation sentiment analysing
    #process.exploratory_data_analysis(df)


    #time_series analysis
    #new_df=process.time_based_analysis(new_df)
    #result_df = process.time_analysing(new_df)







    #popularity user
    #file_test='assets/data_raw_after_del.csv'
    #user_df = pd.read_csv(filepath_or_buffer=file, encoding='utf-8')
    #user_df_updated=data_collection.user_scan(user_df)













