import requests
import pandas as pd

def add_posts(dataframe, res):
    for post in res.json()['data']['children']:

        temp = {
        'name': post['data']['name'],
        'title': post['data']['title'],
        'selftext': post['data']['selftext'],
        'score': post['data']['score']}

        dataframe.iloc[len(dataframe) - 1] = temp

def reddit_scrape(app_id, secret, username, password, subreddits):
    df_dict = {}
    app_id = app_id
    secret = secret
    auth = requests.auth.HTTPBasicAuth(app_id, secret)

    reddit_username = username
    reddit_password = password

    data = {
    'grant_type': 'password',
    'username': reddit_username,
    'password': reddit_password
    }

    headers = {'User-Agent': 'Tutorial2/0.0.1'}
    res = requests.post('https://www.reddit.com/api/v1/access_token',auth=auth, data=data, headers=headers)
    res.json()
    token = res.json()['access_token']
    headers['Authorization'] = 'bearer {}'.format(token)
    requests.get('https://oauth.reddit.com/api/v1/me', headers=headers)

    api = 'https://oauth.reddit.com'


    for subreddit in subreddits:
        print(f'{api}/r/{subreddit}/hot')
        res = requests.get(f'{api}/r/{subreddit}/hot', headers=headers, params={'limit': '100'})
        res.json()
        df = pd.DataFrame({'name': [], 'title': [], 'selftext': [], 'score': []})

        for post in res.json()['data']['children']: #extracts each post information

            temp = {
            'name': post['data']['name'],
            'title': post['data']['title'],
            'selftext': post['data']['selftext'],
            'score': post['data']['score']}

            df = df.append(temp, ignore_index=True)

        df_dict[subreddit] = df #subreddit specific dataframe is stored in dictionary where key is subreddit name
    
    return df_dict
