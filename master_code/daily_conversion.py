from module_imports import *

def tweet_daily_rate(tweet_data_original):
    '''
    Creates a new columns detailing tweets per day
    '''
    tweet_data = tweet_data_original.copy()

    tweet_data['datetime'] = pd.to_datetime(tweet_data['datetime'])
    tweet_data['hour'] = tweet_data['datetime'].dt.hour
    tweet_data['date'] = tweet_data['datetime'].dt.date

    daily_tweets = tweet_data.groupby(['date', 'hour']).agg({'negative_bert':'mean',
                                                    'neutral_bert':'mean',
                                                    'positive_bert':'mean',
                                                    'text':'count',
                                                    'datetime': lambda x: x.max() - x.min()})

    daily_tweets['datetime_seconds'] = daily_tweets['datetime'].dt.total_seconds()
    daily_tweets['tweets_rate'] = daily_tweets['text']/(daily_tweets['datetime_seconds'])
    daily_tweets_col = daily_tweets.groupby('date').agg({'tweets_rate':'mean'})
    daily_tweets_col['tweets_rate']*86400

    cut_off =daily_tweets.columns.get_loc("positive_bert")
    vol_data = daily_tweets.iloc[:,:cut_off+1]

    vol_data.reset_index(inplace=True)
    vol_data.drop('hour',axis=1,inplace=True)

    vol_data = vol_data.groupby(['date']).agg({'negative_bert':'mean',
                                        'neutral_bert':'mean',
                                        'positive_bert':'mean',
                                        })

    daily_tweets_col = daily_tweets.groupby('date').agg({'tweets_rate':'mean'})
    vol_data['daily_tweets'] = daily_tweets_col['tweets_rate']*86400
    vol_data.reset_index(inplace=True)
    return vol_data

def load_historic_data(symbol, start_date_str, end_date_str, period, interval):
    '''
    Loads price from Yahoo for BTC-USD by default.
    '''
    try:
        df = yf.download(symbol, start=start_date_str, end=end_date_str, period=period, interval=interval)
        #  Add symbol

        df["Symbol"] = symbol
        df['price_change'] = df['Close'].pct_change()
#         print(df)
        return df

    except:
        print(f'Error loading stock data for + {symbol}')
        return None

def daily_data(tweet_data, filename, start_date_str=None,symbol='BTC-USD', end_date_str=None, period='1d', interval='1d'):
    '''
    Creation of new DataFrame for daily averages of all data.
    '''

    vol_data = tweet_daily_rate(tweet_data)

    if start_date_str == None:
        v_date = vol_data.columns.get_loc("date")
        start_date_str = vol_data.iloc[0,v_date]

    vol_data['MA7_Sentiment'] = vol_data['positive_bert'].rolling(window=8).mean()
    vol_data['MA20_Sentiment'] = vol_data['positive_bert'].rolling(window=21).mean()
    vol_data['MA50_Sentiment'] = vol_data['positive_bert'].rolling(window=51).mean()

    if end_date_str == None:
        today = datetime.date.today()
        today_str = datetime.datetime.strftime(today, "%Y-%m-%d")
        BTC_price = pd.DataFrame(load_historic_data(symbol, start_date_str, today_str, period, interval))
    else:
        BTC_price = pd.DataFrame(load_historic_data(symbol, start_date_str, end_date_str, period, interval))
#     print(BTC_price)
    vol_data['BTC_price']=BTC_price.reset_index()['Adj Close']
    vol_data['BTC_trading_volume']=BTC_price.reset_index()['Volume']

    vol_data = vol_data[['date','negative_bert', 'neutral_bert', 'positive_bert',
        'daily_tweets', 'MA7_Sentiment', 'MA20_Sentiment',
        'MA50_Sentiment', 'BTC_price','BTC_trading_volume']]


    vol_data.to_csv(f'{filename}.csv')
    return vol_data
