'''
Created on 29.10.2019

@author: Zoli
'''

class BatteryEstimator(object):
    '''
    classdocs
    '''


    def __init__(self, battery):
        '''
        Constructor
        '''
        self.battery = battery
    
    def accumulateFeedInEnergy(self, energy, energyTypes):
        '''
        Accumulate energy fed into the electricity grid and thereby reduce the purchased energy, once the consumed energy exceeds the produced one
        energy: detailed energy measurements (Wh). Data type: dictionary (key: datetime, value: tuple of 6 - see energyTypes)
        energyTypes: type of energy stored in energy tuple
        batteryCapacity: (Wh)
        '''
        accumulatedEnergy = {}
        
        timestamps = list(energy.keys())
        for timestamp in timestamps:
            value = energy[timestamp]
            
            consumption = value[energyTypes.index('Consumption')]
            production = value[energyTypes.index('Production')]
            
            oldBatteryEnergy = self.battery.energy

            returnedEnergy = self.battery.chargeDischargeBattery(production - consumption)
            
            if returnedEnergy >= 0:
                feedIn = returnedEnergy
                purchased = 0
                selfConsumption = consumption
            else:
                feedIn = 0
                purchased = -returnedEnergy
                selfConsumption = 0
            
            valueList = list(value)
            
            valueList[energyTypes.index('FeedIn')] = feedIn 
            valueList[energyTypes.index('Purchased')] = purchased 
            valueList[energyTypes.index('SelfConsumption')] = selfConsumption
            valueList[energyTypes.index('Accumulated')] = self.battery.energy - oldBatteryEnergy

            accumulatedEnergy[timestamp] = tuple(valueList)
        
        return accumulatedEnergy
            
            
            
            
            
            
            
            
            