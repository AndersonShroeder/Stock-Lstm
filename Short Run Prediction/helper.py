import matplotlib.pyplot as plt
import datetime
import numpy as np
import pandas as pd
def get_data_day(x, dataframe, row):
    lst = []
    for i in range(x):
        lst += dataframe.iloc[i][row]

def get_time_data_day(x, dataframe):
    times = []
    for i in range(x):
        date = dataframe.iloc[i]['date']
        for item in dataframe.iloc[i]['time']:
            time = item.split(":")
            times.append(datetime.datetime(date.year,date.month,date.day,int(time[0]),int(time[1])))
    return times

def plot_x_days_price(x, dataframe, subplot = plt):
    lst = get_data_day(x, dataframe, 'price')
    times = get_time_data_day(x, dataframe)
    subplot.plot(times, lst)
    return times


def plot_x_days_sentiment(x, subreddit, dataframe, data_gather, subplot = plt):
    dct_lst = {}
    for point in data_gather.keys():
        dct_lst[f'{point}'] = np.array(
            [dataframe.iloc[i][subreddit][key][point] for i in range(x) for key in dataframe.iloc[i][subreddit]]).astype(float)
        dct_lst[f'{point}'][f'{point}_list'==0] = np.nan

    times = [dataframe.iloc[i][subreddit].keys() for i in range(x)]

    for key, list in dct_lst.items():
        subplot.bar(times, list, color = data_gather[key], width=.005)
        subplot.bar(times, list, color = data_gather[key], width=.005)

def plot_x_days(x, subreddit, dataframe):
    figure, axis = plt.subplots(2,1)
    plot_x_days_sentiment(x, subreddit, dataframe, {'neg': 'red','pos':'green'},axis[0])
    plot_x_days_price(x, dataframe, axis[1])
    #plot_change(1, dataframe, axis[0])


def generate_day_frame(row, subreddit):
    df = pd.DataFrame.from_dict(row[subreddit], orient='index')
    return df


