from scrapping import redditScript
id = 'ZDNWPNKr3KnHu4swatO7IQ'
secret = "R9_KgJD1GWgvlrG6NfFQvdIwdD4mHw"
subreddits = ['politics']

def reddit_sentiment_process(subreddits):
    subreddits_dict = redditScript.reddit_scrape(id, secret, 'tigiy98', 'Tigiy123!', subreddits)

