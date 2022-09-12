from scrapping import redditScript
import re
from textblob import TextBlob
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
id = 'ZDNWPNKr3KnHu4swatO7IQ'
secret = "R9_KgJD1GWgvlrG6NfFQvdIwdD4mHw"
subreddits = ['politics']

def normalize(row):
    list = []
    for text in row['title']:
        text = text.lower()
        text = re.sub(r"(@\[A-Za-z0-9]+)|([^0-9A-Za-z \t])|(\w+:\/\/\S+)|^rt|http.+?", "", text)
        list.append(text)
    return list


def getpolarity(text):
    return TextBlob(text).sentiment.polarity

def getsubj(text):
    return TextBlob(text).sentiment.subjectivity

def getsent(text):
    sia = SentimentIntensityAnalyzer()
    sentiment = sia.polarity_scores(text = text)
    return sentiment



def reddit_sentiment_process(subreddits):
    subreddits_dict = redditScript.reddit_scrape(id, secret, 'tigiy98', 'Tigiy123!', subreddits)
    for subreddit in subreddits:
        #Normalize Titles
        subreddits_dict[subreddit]['title'] = subreddits_dict[subreddit].apply(normalize, axis = 1)
        subreddits_dict[subreddit]['title'] = subreddits_dict[subreddit].apply(lambda row: row['title'][0], axis = 1)

        #Get sentiment scores
        subreddits_dict[subreddit]['polarity'] = subreddits_dict[subreddit]['title'].apply(getpolarity)
        subreddits_dict[subreddit]['subjectivity'] = subreddits_dict[subreddit]['title'].apply(getsubj)


        compound = []
        neg = []
        pos = []
        neu = []
        SIA = 0

        for i in range(len(subreddits_dict[subreddit]['title'])):
            SIA = getsent(subreddits_dict[subreddit]['title'][i])
            compound.append(SIA['compound'])
            neg.append(SIA['neg'])
            neu.append(SIA['neu'])
            pos.append(SIA['pos'])

        subreddits_dict[subreddit]['compound'] = compound
        subreddits_dict[subreddit]['negative'] = neg
        subreddits_dict[subreddit]['neutral'] = neu
        subreddits_dict[subreddit]['positive'] = pos

        keeps = ['compound', 'negative', 'neutral', 'positive', 'polarity', 'subjectivity', 'title']
        subreddits_dict[subreddit] = subreddits_dict[subreddit][keeps]

    print(subreddits_dict)

reddit_sentiment_process(subreddits)