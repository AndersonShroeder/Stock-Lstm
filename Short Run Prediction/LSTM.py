from copy import deepcopy
from tensorflow.keras.models import Sequential
from tensorflow.keras.optimizers import Adam
from tensorflow.keras import layers
from sklearn.preprocessing import MinMaxScaler
from matplotlib.pyplot import figure
import datetime
import numpy as np
import matplotlib.pyplot as plt

class LSTM:
    def __init__(self, input_df, cols=None, n=3):
        self.model = None
        self.input_df = input_df
        if cols:
            self.cols = cols
        else:
            self.cols = input_df.columns.to_list()
        self.n = n

    def window_data(self):
        self.steps, self.X, self.y = self.windowed_df_to_date_X_y(self.input_df, self.cols, self.n)


    def str_to_datetime(self, s: str):
        split = s.split('-')
        year, month, day = int(split[0]), int(split[1]), int(split[2])
        return datetime.datetime(year=year, month=month, day=day)


    def windowed_df_to_date_X_y(self, windowed_dataframe, cols, n=3):
        scaler = MinMaxScaler()
        df_as_np = windowed_dataframe[cols].to_numpy()
        X = []
        y = []
        
        #get dates -> first column of df
        index = np.asarray([i for i in range(len(df_as_np[:, 0])-n)])

        for i in range(len(df_as_np) - n):
            row = [r for r in df_as_np[i:i+n]]
            X.append(row)
            label = df_as_np[i+n][0]
            y.append(label)


        return index, np.array(X), np.array(y)

    def divide_data(self, plots = True):
        self.window_data()
        q_80 = int(len(self.steps) * .8)
        q_90 = int(len(self.steps) * .9)

        self.steps_train, self.X_train, self.y_train = self.steps[:q_80], self.X[:q_80], self.y[:q_80]
        self.steps_val, self.X_val, self.y_val = self.steps[q_80:q_90], self.X[q_80:q_90], self.y[q_80:q_90]
        self.steps_test, self.X_test, self.y_test = self.steps[q_90:], self.X[q_90:], self.y[q_90:]

        #plot the data to visualize the splits
        if plots:
            figure(figsize=(10, 6))
            plt.plot(self.steps_train, self.y_train)
            plt.plot(self.steps_val, self.y_val)
            plt.plot(self.steps_test, self.y_test)
            plt.legend(['Train', 'Validation', 'Test'])

    def generate_model(self):
        self.model = Sequential([
        layers.Input((self.n, len(self.cols))), # 3 because we look 3 days in the past and 1 because there is only one variable
        layers.LSTM(64),
        layers.Dense(32, activation = 'relu'),
        layers.Dense(32, activation = 'relu'),
        layers.Dense(1) # only want one output -> predicted cost

        ])

        self.model.compile(
            loss='mse', optimizer=Adam(learning_rate=0.001),
            metrics = ['mean_absolute_error']
        )

    def run(self):
        self.generate_model()
        self.hist = self.model.fit(self.X_train, self.y_train, validation_data=(self.X_val, self.y_val), epochs = 70)

    def predict(self, input):
        return self.model.predict(input).flatten()

    def plot(self, inputs):
        for input in inputs:
            steps, x_vals, y_vals, name = input
            predictions = self.predict(x_vals).flatten()
            figure(figsize=(10,6))
            plt.plot(steps, predictions)
            plt.plot(steps, y_vals)
            plt.legend([f'{name} Predicitons', f'{name} Observations'])

    def recursive_prediction(self):
        initial_slice = deepcopy(self.X_train)[0].reshape(1,self.n,len(self.cols))
        predictions = []

        for i in range(1):
            prediction = self.predict(initial_slice)
            predictions.append(prediction)
            initial_slice = initial_slice[0][1:]
            new_slice = initial_slice[-1]
            new_slice[0] = prediction
            new_slice = new_slice.reshape(1, new_slice.shape[0])
            initial_slice = np.append(initial_slice, new_slice, axis = 0).reshape(1,self.n,len(self.cols))
            
        for i in range(len(self.y_test) - 1):
            prediction = self.predict(initial_slice)
            predictions.append(prediction)
            initial_slice = initial_slice[0][1:]
            new_slice = initial_slice[-1]
            new_slice[0] = prediction
            new_slice = new_slice.reshape(1, new_slice.shape[0])
            initial_slice = np.append(initial_slice, new_slice, axis = 0).reshape(1,self.n,len(self.cols))
            initial_slice[0][1][0] = self.y[i]

        return predictions

       
        