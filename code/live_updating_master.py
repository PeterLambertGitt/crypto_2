from module_imports import *

def update():
    ''' This function should be run daily to enable the database to be updated. It takes no inputs and both reads and overwrites the current csv containing the data.
    '''
    # Read most recent data
    old_tweet_data = pd.read_csv("~/code/giadapi/crypto_2/data/processed_data/sentiment_per_tweet.csv",lineterminator='\n',index_col=0)
    old_daily_data = pd.read_csv("~/code/giadapi/crypto_2/data/processed_data/sentiment_per_day.csv",lineterminator='\n',index_col=0)

    # Work out how long to update for
    datetime_idx = old_tweet_data.columns.get_loc("datetime")
    last_time_updated = old_tweet_data.iloc[-1,datetime_idx]
    date_now = str(datetime.now().date())

    print(f'Date is now {date_now}. Updating last occurred {last_time_updated}.')
    print('Updating tweets...')

    new_raw_tweet_data = snscrape(num_tweets=149,start_date=last_time_updated,end_date=None, hour_delta=8,min_gap=10,filename=f'../data/raw_data/scraped_{last_time_updated[:10]}_until_{date_now}.csv',make_csv=True)

    print('Scraping completed.')

    new_raw_tweet_data = new_raw_tweet_data.rename(columns={'text\r':'text'})
    new_raw_tweet_data['datetime'] = pd.to_datetime(new_raw_tweet_data['datetime'])
    new_raw_tweet_data['date'] = new_raw_tweet_data['datetime'].dt.date

    print('Removing spam...')

    new_raw_tweet_data = remove_spam(new_raw_tweet_data)
    new_preproc_tweet_data =  new_raw_tweet_data[['text', 'date','datetime','username']]

    print('Pre-processing tweets...')

    new_preproc_tweet_data['process_text'] = new_preproc_tweet_data['text'].apply(preprocess)

    # Load the model and run all tweets through model

    initialize_model()

    print('Analysing sentiment...')

    new_preproc_tweet_data['text'] = new_preproc_tweet_data['process_text'].apply(scores_bert)

    print('Scores completed!')

    new_preproc_tweet_data.reset_index(inplace=True)

    new_preproc_tweet_data['process_text'] = new_preproc_tweet_data.text
    new_preproc_tweet_data['negative_bert'] = new_preproc_tweet_data.text
    new_preproc_tweet_data['neutral_bert'] = new_preproc_tweet_data.text
    new_preproc_tweet_data['positive_bert'] = new_preproc_tweet_data.text

    for i in range(len(new_preproc_tweet_data)):
        new_preproc_tweet_data['negative_bert'][i] = new_preproc_tweet_data['text'][i][0]
        new_preproc_tweet_data['neutral_bert'][i] = new_preproc_tweet_data['text'][i][1]
        new_preproc_tweet_data['positive_bert'][i] = new_preproc_tweet_data['text'][i][2]

    new_proc_tweet_data = new_preproc_tweet_data.copy()
    new_proc_tweet_data.drop("text",axis=1,inplace=True)

    new_tweet_data = new_proc_tweet_data.rename(columns={'process_text':'text'})

    print('Saving updates separately.')

    new_tweet_data[["datetime", "username", "text", "date", "negative_bert", "neutral_bert", "positive_bert"]].to_csv(f"~/code/giadapi/crypto_2/data/processed_data/latest_tweet_data.csv")

    print('Combining historic and updated data.')

    fully_combined = pd.concat([old_tweet_data,new_tweet_data])
    fully_combined.reset_index(drop=True,inplace=True)
    new_vol_master = daily_data(fully_combined, f'new_vol_master_{last_time_updated[:10]}.csv', start_date_str=None,symbol='BTC-USD', end_date_str=None, period='1d', interval='1d')

    if datetime.now().weekday() == 0:
        fully_combined.to_csv("~/code/giadapi/crypto_2/data/backup_data/sentiment_per_tweet_until_{date_now}.csv")
        new_vol_master.to_csv("~/code/giadapi/crypto_2/data/backup_data/sentiment_per_day_until_{date_now}.csv")

    print('Saving full daily and per tweet data.')

    fully_combined.to_csv("~/code/giadapi/crypto_2/data/processed_data/sentiment_per_tweet.csv")
    new_vol_master.to_csv("~/code/giadapi/crypto_2/data/processed_data/sentiment_per_day.csv")

    print("Update completed.")

    return

if __name__ == "__main__":
    update()
