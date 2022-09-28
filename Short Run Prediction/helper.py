import matplotlib.pyplot as plt
import datetime
import numpy as np

def plot_x_days_stock(x, dataframe, subplot = plt):
    lst = []
    times = []
    for i in range(1, x + 1):
        date = dataframe.index[i]
        for item in dataframe.iloc[i]['time']:
            time = item.split(":")
            times.append(datetime.datetime(date.year,date.month,date.day,int(time[0]),int(time[1])))
        #times += df2.iloc[i]['time']
        lst += dataframe.iloc[i]['price']
    subplot.plot(times, lst)

def plot_x_days_sentiment(x, dataframe, data_gather, subplot = plt):
    dct_lst = {}
    for point in data_gather.keys():
        dct_lst[f'{point}'] = np.array(
            [dataframe.iloc[i]['Economics'][key][point] for i in range(x) for key in dataframe.iloc[i]['Economics']]).astype(float)
        
        dct_lst[f'{point}'][f'{point}_list'==0] = np.nan

    y_vals = []
    for i in range(x):
        date = dataframe.index[i]
        for key in dataframe.iloc[i]['Economics']:
            time = key.split(":")
            y_vals.append(datetime.datetime(date.year,date.month,date.day,int(time[0]),int(time[1])))

    for key, list in dct_lst.items():
        subplot.bar(y_vals, list, color = data_gather[key], width=.005)
        subplot.bar(y_vals, list, color = data_gather[key], width=.005)

def plot_x_days(x, sentiment_dataframe, stock_dataframe):
    figure, axis = plt.subplots(2,1)
    plot_x_days_sentiment(x, sentiment_dataframe, {'neg': 'red','pos':'green'},axis[0])
    plot_x_days_stock(x, stock_dataframe, axis[1])