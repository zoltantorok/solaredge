'''
Created on 28.10.2019

@author: Zoli
'''
import matplotlib
import matplotlib.pyplot as plt
import matplotlib.dates as mdates

class DataPlotter(object):
    '''
    classdocs
    '''


    def __init__(self):
        '''
        Constructor
        '''
        
    def plotDetailedEnergyData(self, energy, labels, figure = 1, show = True):
        plt.figure(figure)
        plt.gca().xaxis_date()
        plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%d-%m-%Y %H:%M'))
        colors = {'Consumption' : 'gray', 'Production' : 'green', 'FeedIn' : 'black', 'Purchased' : 'red', 'SelfConsumption' : 'blue', 'Accumulated' : 'yellow'}
        for i in range(len(labels)):
            plt.plot(list(energy.keys()), [e[i] for e in energy.values()], label=labels[i], color=colors[labels[i]])

        plt.gcf().autofmt_xdate()
        plt.ylabel('Energy (Wh)')
        plt.xlabel('Time')
        plt.legend(loc='upper left', frameon=True)
        if show:
            plt.show()















