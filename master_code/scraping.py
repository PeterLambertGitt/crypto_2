import snscrape.modules.twitter as sntwitter
import pandas as pd
from datetime import datetime, timedelta
import csv

def hour_rounder(t):
        '''
        Rounds to nearest hour by adding a timedelta hour if minute >= 30
        '''
        return (t.replace(second=0, microsecond=0, minute=0, hour=t.hour)+timedelta(hours=t.minute//30))

def timedeltas(start='2022-06-24 06:00:00',last="2022-07-01 06:00:00",hour_delta=8,min_gap=10):
    '''
    Creates two lists of start and end times to scrape tweets from - a work around for the quantity of tweets per day. Of duration min_gap and spacing hour_delta
    '''
#     end = pd.Timestamp(start)+timedelta(minutes=min_gap)
#     end = end.isoformat("_", "seconds")

    if last == None:
        current = datetime.now()
        current.isoformat()
        current = pd.Timestamp(current)
        current = current.tz_localize(None)
    else:
        current = pd.Timestamp(last)

    ts = pd.Timestamp(start)
    ts = hour_rounder(ts+timedelta(hours=8))
    ts = pd.Timestamp(ts)
    ts = ts.tz_localize(None)

    start_list = []
    end_list = []
    start_list.append(ts.isoformat("_", "seconds")+"_UTC")
    end = ts + timedelta(minutes=min_gap)
    end_list.append(end.isoformat("_", "seconds")+"_UTC")

    while (ts+timedelta(hours=hour_delta))<(current-timedelta(minutes=min_gap)):
        ts = ts + timedelta(hours=hour_delta)
        es = ts + timedelta(minutes=min_gap)
        start_list.append(ts.isoformat("_", "seconds")+"_UTC")
        end_list.append(es.isoformat("_", "seconds")+"_UTC")

    return start_list, end_list


def append_to_csv(tweet, fileName):
    '''
    Writing the CSV for Snscrape
    '''
    counter = 0
    #Open OR create the target CSV file
    csvFile = open(fileName, "a", newline="", encoding='utf-8')
    csvWriter = csv.writer(csvFile)
    datetime_date = tweet.date
    username = tweet.user.username
    text = tweet.rawContent
    res = [datetime_date, username, text]
    csvWriter.writerow(res)
    counter += 1
    csvFile.close()
    return

def snscrape(num_tweets=149,start_date='2023-03-05T06:00:00.000Z',end_date='2023-03-06T06:00:00.000Z', hour_delta=8,min_gap=10,filename='run1.csv',make_csv=True):
    '''
    Selects a maximum of num_tweets per section defined by timedeltas, saves it to a CSV and returns it.
    '''
    start_list, end_list = timedeltas(start=start_date,last=end_date,hour_delta=hour_delta,min_gap=min_gap)

    # Create file, create headers for the data you want to save, in this example, we only want save these columns in our dataset

    try:
        with open(filename, "a", newline="", encoding='utf-8') as csvFile:
            csvWriter = csv.writer(csvFile)
            csvWriter.writerow(['datetime', 'username', 'text'])
            csvFile.close()
    except FileExistsError:
        pass

    # Using TwitterSearchScraper to scrape data and append tweets to list
    for i in range(len(start_list)):
        for i,tweet in enumerate(sntwitter.TwitterSearchScraper(f'#bitcoin since:{start_list[i]} until:{end_list[i]} lang:en').get_items()):
            if i>num_tweets:
                break
            append_to_csv(tweet, filename)

    # Creating a dataframe from the tweets list above
    # tweets_df2 = pd.DataFrame(tweets_list2, columns=['Datetime', 'Tweet Id', 'Text', 'Username'])

    if make_csv:
        return pd.read_csv(filename)
    else:
        return
