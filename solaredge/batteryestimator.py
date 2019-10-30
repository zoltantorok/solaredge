'''
Created on 29.10.2019

@author: Zoli
'''

class BatteryEstimator(object):
    '''
    classdocs
    '''


    def __init__(self):
        '''
        Constructor
        '''
    
    def accumulateFeedInEnergy(self, energy, energyTypes, batteryCapacity):
        '''
        Accumulate energy fed into the electricity grid and thereby reduce the purchased energy, once the consumed energy exceeds the produced one
        energy: detailed energy measurements (Wh). Data type: dictionary (key: datetime, value: tuple of 6 - see energyTypes)
        energyTypes: type of energy stored in energy tuple
        batteryCapacity: (Wh)
        '''
        batteryChargeLevel = 0
        oldBatteryChargeLevel = 0
        accumulatedEnergy = {}
        
        timestamps = list(energy.keys())
        for timestamp in timestamps:
            value = energy[timestamp]
            
            consumption = value[energyTypes.index('Consumption')]
            production = value[energyTypes.index('Production')]
            
            batteryChargeLevel = batteryChargeLevel + production - consumption
            
            if batteryChargeLevel > batteryCapacity:
                overflowEnergy = batteryChargeLevel - batteryCapacity
                batteryChargeLevel = batteryCapacity
                feedIn = overflowEnergy
                purchased = 0
                selfConsumption = consumption
            elif batteryChargeLevel < 0:
                underflowEnergy = -batteryChargeLevel
                batteryChargeLevel = 0
                feedIn = 0
                purchased = underflowEnergy
                selfConsumption = 0
            else:
                feedIn = 0
                purchased = 0
                selfConsumption = consumption
            
            valueList = list(value)
            
            valueList[energyTypes.index('FeedIn')] = feedIn 
            valueList[energyTypes.index('Purchased')] = purchased 
            valueList[energyTypes.index('SelfConsumption')] = selfConsumption
            valueList[energyTypes.index('Accumulated')] = batteryChargeLevel - oldBatteryChargeLevel

            oldBatteryChargeLevel = batteryChargeLevel
            
            accumulatedEnergy[timestamp] = tuple(valueList)
        
        return accumulatedEnergy
            
            
            
            
            
            
            
            
            