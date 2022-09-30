
from collections import defaultdict
import pandas as pd
import requests
import json
import datetime
from dateutil.relativedelta import relativedelta
import re
from textblob import TextBlob
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer


def fact():
    return defaultdict(lambda: defaultdict(lambda: defaultdict(int)))


def getpolarity(text):
    return TextBlob(text).sentiment.polarity


def getsubj(text):
    return TextBlob(text).sentiment.subjectivity


def getsent(text):
    sia = SentimentIntensityAnalyzer()
    sentiment = sia.polarity_scores(text = text)
    return sentiment


def gather_data_full(subreddit, before = datetime.datetime.now(), relative_days = None):
    """
    Gathers complete post history from a given subreddit and returns a pandas dataframe where the rows represent the day of posting
    and columns are a list of lists where each nested list by index is: 
                (0: title, 1: exact time, 2: polarity, 3: subjectivity, 4: neg, 5: neu, 6: pos, 7: compound)
    Inputs:
        - subreddit: a string that is the subreddit we gather post data on
        - before: an integer representing Unix Timestamp of the max time to query for - instant moment by default
        - relative_days: an integer representing the number of days back from the present day we gather data from
    Outputs:
        - Returns a pandas dataframe
    """

    after = before - relativedelta(days=relative_days) # finds date relative to current date, relative_days ago
    current = int(after.timestamp()) #converts to utc
    before = int(before.timestamp())

    post_dct = defaultdict(fact) #dict where keys are a date and values are a list of post data

    while current < before:
            one_day = current + 86400

            #api call for posts in one given day
            url = f"https://api.pushshift.io/reddit/search/submission/?after={current}&before={one_day}&subreddit={subreddit}&size=500"
            r = requests.get(url)
            data = json.loads(r.text)
            clean_data(post_dct, data['data'], subreddit)
            current = one_day

    post_dct = dict(post_dct)
    df = pd.DataFrame.from_dict(post_dct, orient='index')
    df[f'{subreddit}_times']

    return df


def clean_data(dct, data_set, subreddit, left_time:tuple = (9, 30), right_time:tuple = (16, 0)):
    """
    Helper function that normalizes and generates entry in dataframe for a given day - the days/posts are sorted by time of day
    Inputs:
        - dct: a dictionary that will be used to create the final dataframe
        - data_set: the dataset generated from the api call for one day
        - subreddit: a string the represents the current subreddit

    Outputs:
        - Does not return a value - modifies the dataframe dictionary
    """
    
    for post in data_set:

        #normalize the post titles
        title = post['title']
        title = title.lower()
        title = re.sub(r"(@\[A-Za-z0-9]+)|([^0-9A-Za-z \t])|(\w+:\/\/\S+)|^rt|http.+?", "", title)
        
        #Restricts the posts gathered to the times we are concerned about for a given day
        created = datetime.datetime.fromtimestamp(post['created_utc'])
        if ((created > datetime.datetime(created.year, created.month, created.day, hour=left_time[0],minute=left_time[1])) and 
            (created < datetime.datetime(created.year, created.month, created.day, hour=right_time[0],minute=right_time[1]))):

            #isolates the day to be used as key for dictionary and time for lstm
            key_date = str(created).split(" ") 

            #analyze news title and store data in a dictionary
            data = {}
            SIA = getsent(title)
            data['polarity'] = getpolarity(title)
            data['subjectivity'] = getsubj(title)
            data['compound'] = SIA['compound']
            data['neg'] = SIA['neg']
            data['neu'] = SIA['neu']
            data['pos'] = SIA['pos']

            #isolate only minutes of post - seconds are too percise for stock data
            key_date[1] = key_date[1][:5] + ":00"

            #add stored values to total values for the time
            for key, value in data.items():
                dct[key_date[0]][subreddit][key_date[1]][key] += value


def generate_csv(subreddit, relative_days):
    df = gather_data_full(subreddit, relative_days=relative_days)
    df.to_json(f'generated_data_{subreddit}.json', index=True)

generate_csv('Economics', 10)