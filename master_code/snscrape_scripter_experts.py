import snscrape.modules.twitter as sntwitter
import pandas as pd
# For sending GET requests from the API
import requests
# For saving access tokens and for file management when creating and adding to the dataset
import os
# For dealing with json responses we receive from the API
import json
# For saving the response data in CSV format
import csv
# For parsing the dates received from twitter in readable formats
import datetime
import dateutil.parser
import unicodedata
#To add wait time between requests
import time
from datetime import datetime
from datetime import timedelta

def timedeltas(start='2022-06-24 06:00:00',last="2022-07-01 06:00:00",hour_delta=8,min_gap=10):

    end = pd.Timestamp(start)+timedelta(minutes=min_gap)
#     end = end.tz_localize(None)
    end = end.isoformat("_", "seconds")

    if last == None:
        current = datetime.now()
        current.isoformat()
    else:
        current = pd.Timestamp(last)

    ts = pd.Timestamp(start)

#     ts = ts.tz_localize(None)

    start_list = []
    end_list = []
    start_list.append(ts.isoformat("_", "seconds")+"_UTC")
    end_list.append(end+"_UTC")


    while (ts+timedelta(hours=hour_delta))<(current-timedelta(minutes=min_gap)):
        ts = ts + timedelta(hours=hour_delta)
        es = ts + timedelta(minutes=min_gap)
        start_list.append(ts.isoformat("_", "seconds")+"_UTC")
        end_list.append(es.isoformat("_", "seconds")+"_UTC")

    return start_list, end_list


def append_to_csv(tweet, fileName):

    #A counter variable
    counter = 0

    #Open OR create the target CSV file
    csvFile = open(fileName, "a", newline="", encoding='utf-8')
    csvWriter = csv.writer(csvFile)

    #Loop through each tweet


    # We will create a variable for each since some of the keys might not exist for some tweets
    # So we will account for that
#         tweet.date, tweet.id, tweet.content, tweet.user.username

    # 1. Tweet Date
    datetime = tweet.date

    # 2. username
    username = tweet.user.username

    # 8. Tweet text
    text = tweet.content

    # Assemble all data in a list
    res = [datetime, username, text]

    # Append the result to the CSV file
    csvWriter.writerow(res)
    counter += 1

    # When done, close the CSV file
    csvFile.close()


    return

def get_usernames(file_csv='../../raw_data/Usernames - Sheet1.csv'):
    with open(file_csv, newline='') as f:
        reader = csv.reader(f)
        data = list(reader)
        experts = []
        for i in range(len(data)):
            experts.append(data[i][0][1:])
        return experts




def snscrape_expert(start_date='2021-01-01T06:00:00.000Z',end_date='2023-04-04T06:00:00.000Z',filename='../../raw_data/010122_040423.csv',users_name=['ElonMusk'],make_csv=True):

    # Creating list to append tweet data to
#     start_list, end_list = timedeltas2(start=start_date,end=end_date,hour_delta=hour_delta,min_gap=min_gap)
    # start_list, end_list = timedeltas(start=start_date,last=end_date,hour_delta=hour_delta,min_gap=min_gap)

#     print(start_list)

    # Create file
    csvFile = open(filename, "a", newline="", encoding='utf-8')
    csvWriter = csv.writer(csvFile)

    #Create headers for the data you want to save, in this example, we only want save these columns in our dataset
    csvWriter.writerow(['datetime', 'username', 'text'])
    csvFile.close()
    if end_date==None:

        for n, k in enumerate(users_name):
            # for i,tweet in enumerate(sntwitter.TwitterSearchScraper(f'#bitcoin from:{k} since:{start_list[i]} until:{end_list[i]} lang:en').get_items()):
            for i,tweet in enumerate(sntwitter.TwitterSearchScraper(f'from:{users_name[n]} since:{start_date} lang:en').get_items()):
                append_to_csv(tweet, filename)

    else:
        for n, k in enumerate(users_name):
            # for i,tweet in enumerate(sntwitter.TwitterSearchScraper(f'#bitcoin from:{k} since:{start_list[i]} until:{end_list[i]} lang:en').get_items()):
            for i,tweet in enumerate(sntwitter.TwitterSearchScraper(f'from:{users_name[n]} since:{start_date} until:{end_date} lang:en').get_items()):
                append_to_csv(tweet, filename)



    if make_csv:
        return pd.read_csv(filename)
    else:
        return

if __name__ == "__main__":
    experts = get_usernames(file_csv='raw_data/104_expert_users.csv')
    cuts = int(len(experts)/2)
    experts = experts[:cuts]
    snscrape_expert(start_date='2021-01-01_06:00:00_UTC',end_date='2023-04-04_06:00:00_UTC',filename='raw_data/010122_040423_H1experts.csv',users_name=experts,make_csv=False)
