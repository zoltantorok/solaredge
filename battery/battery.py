'''
Created on 31.10.2019

@author: Zoli
'''
import math

class Battery(object):
    '''
    Battery handler class
    - Charge or discharge battery depending on whether the power is positive or negative
    - Return the charge that couldn't be stored (battery full) or discharged (battery empty)
    '''


    def __init__(self, capacity, chargingLossPercent, dischargingLossPercent, maxChargingPower, maxDischargingPower):
        '''
        Constructor
        '''
        self.capacity = capacity
        self.chargingLossPercent = chargingLossPercent
        self.dischargingLossPercent = dischargingLossPercent
        self.maxChargingPower = maxChargingPower
        self.maxDischargingPower = maxDischargingPower
        self.energy = 0
        self.resetBattery()
        
    def resetBattery(self):
        self.energy = 0
        
    def convertEnergyToPower(self, energy, timeUnit = 'QUARTER_OF_AN_HOUR'):
        if timeUnit == 'QUARTER_OF_AN_HOUR':
            return energy * 4
        elif timeUnit == 'HOUR':
            return energy * 1
        elif timeUnit == 'DAY':
            return energy / 24.0
        else:
            raise RuntimeError('Unsupported time unit while converting energy to power')

    def convertPowerToEnergy(self, power, timeUnit = 'QUARTER_OF_AN_HOUR'):
        if timeUnit == 'QUARTER_OF_AN_HOUR':
            return power / 4.0
        elif timeUnit == 'HOUR':
            return power
        elif timeUnit == 'DAY':
            return power * 24.0
        else:
            raise RuntimeError('Unsupported time unit while converting energy to power')
        
    def chargeDischargeBattery(self, energy, timeUnit = 'QUARTER_OF_AN_HOUR'):
        if math.isclose(energy, 0):
            return 0
        elif energy > 0:
            return self.chargeBattery(energy, timeUnit)
        else:
            return self.dischargeBattery(energy, timeUnit)
    
    def chargeBattery(self, energy, timeUnit):
        overflowEnergy = 0
        
        if self.convertEnergyToPower(energy, timeUnit) > self.maxChargingPower:
            maxChargingEnergy = self.convertPowerToEnergy(self.maxChargingPower, timeUnit)
            overflowEnergy = energy - maxChargingEnergy 
            energy = maxChargingEnergy
        
        energy = energy * (100 - self.chargingLossPercent) / 100.0
        
        self.energy = self.energy + energy
        if self.energy > self.capacity:
            overflowEnergy = overflowEnergy + self.energy - self.capacity
            self.energy = self.capacity
        
        return overflowEnergy
    
    def dischargeBattery(self, energy, timeUnit):
        underflowEnergy = 0
        
        if abs(self.convertEnergyToPower(energy, timeUnit)) > self.maxDischargingPower:
            maxDischargingEnergy = self.convertPowerToEnergy(self.maxDischargingPower, timeUnit)
            underflowEnergy = energy + maxDischargingEnergy # energy is negative
            energy = -maxDischargingEnergy
        
        dischargingLoss = (100 + self.dischargingLossPercent) / 100.0
        energy = energy * dischargingLoss 
        
        self.energy = self.energy + energy
        if self.energy < 0:
            # Not accepted energy is not affected by discharging loss
            self.energy = self.energy / dischargingLoss
            underflowEnergy = underflowEnergy + self.energy
            self.energy = 0
        
        return underflowEnergy
    
    
    
    
    
    
    
    