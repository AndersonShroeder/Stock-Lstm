from collections import defaultdict
from Analyzer import Analyzer
import random
import numpy as np
import matplotlib.pyplot as plt

class Markov(Analyzer):
    
    def __init__(self):
        self.chain = None
        self.predictions = None


    def generate_chain(self, degree, data):

        #nested default dict
        dct = defaultdict(lambda: defaultdict(int))    

        #generate previously seen states of length degree -> key into state slice then add one to the state at the index after slice
        for i in range((len(data) - degree - 1)):
            r = degree + i
            slice = tuple(data[i: r])
            dct[slice][data[r]] += 1

        #convert to frequencies
        for key, value in dct.items():
            sums = sum(value.values())
            for key2, value2 in value.items():
                dct[key][key2]= value2/sums
                dct[key] = dict(dct[key])
        
        self.chain = dict(dct)


    def predict(self, last, num):
        states = []
        
        for _step in range(num):
            rand_list = [] #contains the numbers 0, 1, 2, 3 in their proper frequency
            weights = []
            
            if tuple(last) not in self.chain.keys(): #check if the key exists in dict
                rand_list = [0,1,2,3]
                weights = [.25, .25, .25, .25]
                    
            else: 
                for key, value in self.chain[tuple(last)].items():
                    rand_list.append(key)
                    weights.append(value)

            #randomly pick from list of elements - equivalent to a weighted average
            state = np.random.choice(rand_list, 1, p=weights)[0]

            states.append(state)
            last = last[1:] #shift last to the right in order to maintain order size
            last.append(state)

        self.predictions = np.asarray(states)
        

    def mse(self, expected):
        expected = np.asarray(expected)
        return np.sum(((self.predictions - expected)**2))/len(expected)

    def accuracy(self, expected):
        return (self.predictions == np.asarray(expected)).mean()


    def run(self, train, test, degree, trials):
        #initialize error as 0 and then add as trials progress
        cumulative_accuracy = 0
        error = 0
        for _trial in range(trials):
            self.generate_chain(degree, train)
            self.predict(test[:degree], len(test) - degree)
            cumulative_accuracy += self.accuracy(test[degree:])
            error += self.mse(test[degree:])
         
        return cumulative_accuracy/trials, error/trials


    def optimal_degree(self, train, test, trials, degrees):
        accuracy_plt = []
        mse_plt = []
        for i in degrees:
            accuracy, error = self.run(train, test, i, trials)
            accuracy_plt.append(accuracy)
            mse_plt.append(error)

        print(accuracy_plt.index(max(accuracy_plt)))
        print(max(accuracy_plt))
        plt.plot(accuracy_plt)
        plt.plot(mse_plt)
        plt.show()


