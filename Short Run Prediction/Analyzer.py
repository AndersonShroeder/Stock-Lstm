import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import numpy as np
myFmt = mdates.DateFormatter('%H%:%M:%S')

class Analyzer:
    """
    Generator class which contains methods to generate data from subreddits/stock prices.
    Initializes with:
        - Subreddits: a list of subreddit titles where each title is a string
        - Dataframe: a pandas dataframe containing the stock prices per time interval
        - 
    """

    def __init__(self, subreddits, dataframe):
        self.subreddits = subreddits
        self.dataframe = dataframe
        self.df_dict = self.generate_daily_full(subreddits, dataframe)
        self.complete_markov = {subreddit:[] for subreddit in self.subreddits}
        self.combined_df_dict = None



    def convert(self, row, subreddit):
        lst = []
        for dct in row.loc[subreddit]:
            lst.append([dct])

        return lst
        


    def generate_daily_data(self, index, subreddit):
        """
        Creates a dataframe that is the result of merging the stock prices per time period
        and the subreddit specific data
        Inputs:
            - index: the index of the row being used to generate data
        Outputs:
            - Returns a pandas dataframe of daily subreddit/stock price data
        """
        
        #create a dictionary with a time key that has every minute ina 24 hour period
        d = self.dataframe.iloc[index][['date', 'na']].to_dict()
        d['time'] = pd.date_range(self.dataframe['date'].iat[index], freq='Min', periods=60*24, name='date')
        
        #create an empty dataframe with the index as the generated time
        df = pd.DataFrame(d)
        df.set_index(df['time'], inplace = True)
        df = df[[]]

        #create dataframe for each column of stock data we want time series for -> index is stock_time
        price_time_df = pd.DataFrame(self.dataframe.iloc[index]['price'], 
                                    index = self.dataframe.iloc[index]['stock_time'], 
                                    columns=['price'])

        percent_change_df = pd.DataFrame(self.dataframe.iloc[index]['percent_change'], 
                                        index = self.dataframe.iloc[index]['stock_time'], 
                                        columns=['percent_change'])
        
        #store created dataframes in a list to later be merged into one dataframe
        lst = [price_time_df, percent_change_df]

        #create dataframes of sentiment_data -> index is sentiment_time
        for subreddit in self.subreddits:
            reddit_df = pd.DataFrame(self.dataframe.iloc[index][subreddit], 
                                    index = self.dataframe.iloc[index]['sentiment_time'], 
                                    columns=['sentiment']).reset_index()

            sentiment_time_df = pd.json_normalize(reddit_df['sentiment'])
            sentiment_time_df['index'] = reddit_df['index']
            sentiment_time_df.set_index(['index'], inplace=True)
            lst.append(sentiment_time_df)
        
        #Create new Dataframe by joining all of the generated dataframes
        joined_df = df.join(lst)
        joined_df.reset_index(inplace=True)
        joined_df = joined_df.dropna(subset=['price'])
        joined_df.index = joined_df.pop('time')
        #pd.to_datetime(joined_df['time'])
        
        return joined_df



    def generate_daily_full(self, subreddits, dataframe):
        dct = {}
        df = pd.DataFrame()
        for subreddit in subreddits:
            dataframe[subreddit] = dataframe.apply(lambda row: self.convert(row, subreddit), axis = 1)
            lst = [self.generate_daily_data(i, subreddit) for i in range(len(dataframe))]
            for i in lst:
                df=pd.concat([df, i], ignore_index=False)
            df = df.fillna(method='ffill').dropna()
            dct[subreddit] = df
        return dct



    def markov_chain_data(self):
        """
        Adds a column to the daily dataframes indicating the markov bin the time interval falls into
        """
        for subreddit in self.subreddits:
            for df in self.df_dict[subreddit]:

                #generates a numpy array populated with values that correspond to precent changes -> new markov_bins column
                df['markov_bins'] = np.where(
                    (df['percent_change'] < -.1), 0, np.where(
                        ((df['percent_change'] > -.1) & (df['percent_change'] < 0)), 1, np.where(
                            ((df['percent_change'] < .1) & (df['percent_change'] > 0)), 2, np.where(
                                (df['percent_change'] > .1), 3, np.nan
                            ))))

                self.complete_markov[subreddit] += list(df.markov_bins.dropna())


    def plot_markov_hist(self, start_day, end_day):

        #iterate through the range of start_day and end_day -> create a dictionary where the key is bin # and key is the count
        for day in range(start_day, end_day+1):
            lst = np.array(self.df_dict['Economics'][day].markov_bins.dropna())
            unique, counts = np.unique(lst, return_counts=True)
            dct = dict(zip(unique,counts))
            plt.bar(unique, counts)
            plt.show()
            


    def plot_subreddits_day(self, subreddits, plot_args, start_day, end_day, percent_change = False):
        colors = {'neg': 'red','pos':'green', 'neu': 'blue'}
        for day in range(start_day, end_day+1): 
            for subreddit in subreddits:
                fig,ax = plt.subplots()
                if not percent_change:
                    ax.plot(self.df_dict[subreddit][day].time, self.df_dict[subreddit][day].price, color="black",)
                else:
                    ax.plot(self.df_dict[subreddit][day].time, self.df_dict[subreddit][day].percent_change, color="blue")
                    ax.set_ylim([-.3, .3])

                #ax.xaxis.set_major_formatter(myFmt)

                # set x-axis label
                ax.set_xlabel("Time", fontsize = 14)
                # set y-axis label
                ax.set_ylabel("Price", color="red", fontsize=14)
                ax2=ax.twinx()
                # make a plot with different y-axis using second axis object
                for arg in plot_args:
                    ax2.bar(self.df_dict[subreddit][day].time, self.df_dict[subreddit][day][arg] ,color=colors[arg], width = .002)
                ax2.set_ylabel("Sentiment",color="black",fontsize=14)
                fig.set_figwidth(15)
                fig.set_figheight(5)
                plt.show()


    def generate_train_test(self, index):
        """
        
        """
        for subreddit in self.subreddits:
            df_temp = pd.concat(self.df_dict[subreddit])
            for column in df_temp.columns:
                if column != 'time':
                    df_temp[column].fillna(value = df_temp[column].mean(), inplace=True)
            n = len(df_temp)
            
            train_df = df_temp[0:int(n*.7)]
            train_x = train_df.drop(['time', 'price'], axis=1)
            train_y = train_df[['price']]

            val_df = df_temp[int(n*.7):int(n*.9)]
            val_x = val_df.drop(['time', 'price'], axis=1)
            val_y = val_df[['price']]
            
            test_df = df_temp[int(n*.9):]
            test_x = test_df.drop(['time', 'price'], axis=1)
            test_y = test_df[['price']]

        return [(train_x, train_y), (val_x, val_y), (test_x, test_y)]