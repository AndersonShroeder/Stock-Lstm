import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
myFmt = mdates.DateFormatter('%H%:%M:%S')

class Analyzer:
    def __init__(self, subreddits, dataframe):
        self.subreddits = subreddits
        self.dataframe = dataframe
        self.df_dict = self.generate_daily_full()


    #convert subreddit to nested lists containing dict
    def convert(self, row, subreddit):
        lst = []
        for dct in row.loc[subreddit]:
            lst.append([dct])
        return lst
        

    #generate daily data
    def generate_daily_data(self, index, subreddit):
        #create a data frame of all possible minute values in a day
        d = self.dataframe.iloc[index][['date', 'na']].to_dict()
        d['time'] = pd.date_range(self.dataframe['date'].iat[index], freq='Min', periods=60*24, name='date')
        df = pd.DataFrame(d)
        df.set_index(df['time'], inplace = True)
        df = df[[]]

        #create dataframe for each column we want time series for
        price_time_df = pd.DataFrame(self.dataframe.iloc[index]['price'], index = self.dataframe.iloc[index]['stock_time'], columns=['price'])
        percent_change_df = pd.DataFrame(self.dataframe.iloc[index]['percent_change'], index = self.dataframe.iloc[index]['stock_time'], columns=['percent_change'])
        
        #create dataframe of sentiment_data
        lst = [price_time_df, percent_change_df]
        for subreddit in self.subreddits:
            reddit_df = pd.DataFrame(self.dataframe.iloc[index][subreddit], index = self.dataframe.iloc[index]['sentiment_time'], columns=['sentiment']).reset_index()
            sentiment_time_df = pd.json_normalize(reddit_df['sentiment'])
            sentiment_time_df['index'] = reddit_df['index']
            sentiment_time_df.set_index(['index'], inplace=True)
            lst.append(sentiment_time_df)
        #print(sentiment_time_df)
        

        joined_df = df.join(lst)
        joined_df.reset_index(inplace=True)

        pd.to_datetime(joined_df['time'])
        

        return joined_df

    #generate a list of dataframes for each day in the dataset
    def generate_daily_full(self):
        dct = {}
        for subreddit in self.subreddits:
            self.dataframe[subreddit] = self.dataframe.apply(lambda row: self.convert(row, subreddit), axis = 1)
            dct[subreddit]=[self.generate_daily_data(i, subreddit) for i in range(len(self.dataframe))]

        return dct

    import matplotlib.dates as mdates
    myFmt = mdates.DateFormatter('%H%:%M:%S')
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

                            ax.xaxis.set_major_formatter(myFmt)

                            # set x-axis label
                            ax.set_xlabel("Time", fontsize = 14)
                            # set y-axis label
                            ax.set_ylabel("Price", color="red", fontsize=14)
                            ax2=ax.twinx()
                            # make a plot with different y-axis using second axis object
                            for arg in plot_args:
                                    ax2.bar(self.df_dict[subreddit][day].time, self.df_dict[subreddit][day][arg] ,color=colors[arg], width = .002)
                            ax2.set_ylabel("Sentiment",color="black",fontsize=14)
                            plt.show()
