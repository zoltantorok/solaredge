'''
Created on 10.11.2019

@author: Zoli
'''
import datetime

class EnergyCost(object):
    '''
    classdocs
    '''
    dayStart = datetime.time(0, 0)
    dayEnd = datetime.time(hour=23, minute=59, second=59)
    timeEpsilon = datetime.timedelta(seconds=1)

    def __init__(self):
        '''
        Constructor
        '''
        self.energyCostLookup = {}
        self.energyRefundLookup = {}
        
    def getEnergyCost(self, reqDateTime):
        for singleCostKey, singleCostValue in self.energyCostLookup.items():
            if singleCostKey[0] <= reqDateTime <= singleCostKey[1]:
                if singleCostKey[2] == reqDateTime.weekday():
                    for value in singleCostValue:
                        if value[0] <= reqDateTime.time() <= value[1]:
                            return value[2]
        
        raise RuntimeError('Energy cost wasn\'t found for the required date')
    
    def getEnergyRefund(self, reqDateTime):
        for singleRefundKey, singleRefundValue in self.energyRefundLookup.items():
            if singleRefundKey[0] <= reqDateTime <= singleRefundKey[1]:
                return singleRefundValue[2] 
        
        raise RuntimeError('Energy cost wasn\'t found for the required date')
        
    def setConstantEnergyCostPerKWh(self, cost, validFrom, validTo):
        for d in range(7):
            self.addTimeLimitedEnergyCostPerKWh(d, self.dayStart, self.dayEnd, cost, validFrom, validTo)

    def setConstantEnergyRefundPerKWh(self, refund, validFrom, validTo):
        singleWeekday = 0
        self.energyRefundLookup[(validFrom, validTo, singleWeekday)] = (self.dayStart, self.dayEnd, refund)
            
    def addTimeLimitedEnergyCostPerKWh(self, weekday, startTime, endTime, cost, validFrom, validTo):
        '''
        weekday: 0..6 or Monday..Sunday, respectively
        '''
        weekdayNumber = self.getWeekdayNumber(weekday)
        key = (validFrom, validTo, weekdayNumber)
        if key not in self.energyCostLookup.keys():
            self.energyCostLookup[key] = []
        self.energyCostLookup[key].append((startTime, endTime, cost))
    
    def setDualTariffEnergyCost(self, highTariff, weekdaysHighTariff, startTime, endTime, lowTariff, validFrom, validTo):
        weekdaysHighTariffWithNumber = []
        for d in weekdaysHighTariff:
            weekdaysHighTariffWithNumber.append(self.getWeekdayNumber(d))
        
        for d in range(7):
            if d in weekdaysHighTariffWithNumber:
                timeDiffBeforeStart = self.convertTimeOfDayToSeconds(startTime) - self.convertTimeOfDayToSeconds(self.dayStart)
                if timeDiffBeforeStart > 0:
                    self.addTimeLimitedEnergyCostPerKWh(d, self.dayStart, self.addTime(startTime, -self.timeEpsilon), lowTariff, validFrom, validTo)
                    
                self.addTimeLimitedEnergyCostPerKWh(d, startTime, endTime, highTariff, validFrom, validTo)
                
                timeDiffAfterEnd = self.convertTimeOfDayToSeconds(self.dayEnd) - self.convertTimeOfDayToSeconds(endTime)
                if timeDiffAfterEnd > 0:
                    self.addTimeLimitedEnergyCostPerKWh(d, self.addTime(endTime, self.timeEpsilon), self.dayEnd, lowTariff, validFrom, validTo)
                
            else:
                self.addTimeLimitedEnergyCostPerKWh(d, self.dayStart, self.dayEnd, lowTariff, validFrom, validTo)
            
    def getWeekdayNumber(self, weekday):
        if isinstance(weekday, int):
            if weekday not in range(0, 7):
                raise RuntimeError('Unexpected weekday received')
            weekdayNumber = weekday 
        elif isinstance(weekday, str):
            weekdays = ['monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday']
            weekdayNumber = weekdays.index(weekday.casefold()) 

        return weekdayNumber

    def convertTimeOfDayToSeconds(self, time):
        timeAsTimeDelta = datetime.datetime.combine(datetime.date.min, time) - datetime.datetime.min
        return timeAsTimeDelta.total_seconds()

    def addTime(self, time, timeDelta):
        dateAndTime = datetime.datetime.combine(datetime.date.min, time)
        dateAndTime = dateAndTime + timeDelta
        return dateAndTime.time()

















