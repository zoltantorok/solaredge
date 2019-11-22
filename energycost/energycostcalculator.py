'''
Created on 31.10.2019

@author: Zoli
'''
import energycost

class EnergyCostCalculator(object):
    '''
    classdocs
    '''


    def __init__(self, energyCosts):
        '''
        Constructor
        '''
        self.energyCosts = energyCosts
    
    def calculateCost(self, energyData, labels):
        
        cost = 0
        
        timestamps = list(energyData.keys())
        for timestamp in timestamps:
            value = energyData[timestamp]
            
            feedIn = value[labels.index('FeedIn')]
            purchased = value[labels.index('Purchased')]
            
            costPerKwh = self.energyCosts.getEnergyCost(timestamp)
            refundFeedInKwh = self.energyCosts.getEnergyRefund(timestamp)
                        
            cost = cost + costPerKwh * purchased / 1000.0
            cost = cost - refundFeedInKwh * feedIn / 1000.0  

        return cost
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    