'''
Created on 27.10.2019

@author: Zoli
'''

from datetime import datetime, timedelta

class DataReadout(object):
    '''
    classdocs
    '''
    shortFormat = '%Y-%m-%d'
    extFormat = shortFormat + ' %H:%M:%S'
    timeUnit = 'QUARTER_OF_AN_HOUR'

    def __init__(self, solaredge, site_id):
        '''
        Constructor
        '''
        self.solaredge = solaredge
        self.site_id = site_id
        self.timeUnitTimeDelta = timedelta(minutes=15)  
        self.timeLimitForMultiReadout = timedelta(weeks=1)

    
    def getDetailedEnergy(self, startDate, endDate):
        start = self.parseDate(startDate)
        end = self.parseDate(endDate)
        queryTimeDifference = end - start
        if queryTimeDifference <= self.timeLimitForMultiReadout:
            return self.readDetailedEnergy(start, end)
        else:
            timeFrames = self.getTimeFramesWeekly(start, end)
            energy = {}
            for frame in timeFrames:
                energy.update(self.readDetailedEnergy(frame[0], frame[1]))
            return energy
            
    def getTimeFramesWeekly(self, startDate, endDate):
        thisStart = startDate
        timeFrames = []
        
        while endDate >= thisStart + self.timeLimitForMultiReadout:
            timeFrames.append((thisStart, thisStart + self.timeLimitForMultiReadout))
            thisStart = thisStart + self.timeLimitForMultiReadout + self.timeUnitTimeDelta
        
        if thisStart < endDate:
            timeFrames.append((thisStart, endDate))
        
        return timeFrames
    
    def readDetailedEnergy(self, startDate, endDate):
        if not isinstance(startDate, datetime) and not isinstance(endDate, datetime):
            raise RuntimeError('readDetailedEnergy expects datetime.date objects')
        energy = self.solaredge.get_energyDetails(self.site_id, self.formatDate(startDate), self.formatDate(endDate), None, self.timeUnit)
        return self.convertEnergyData(energy)

    @staticmethod
    def energyTypes():
        return ['Consumption', 'SelfConsumption', 'FeedIn', 'Purchased', 'Production', 'Accumulated']

    @staticmethod
    def convertEnergyData(seEnergy):
        # expecting: {'energyDetails': {'timeUnit': 'QUARTER_OF_AN_HOUR', 'unit': 'Wh', 'meters': [{'type': 'SelfConsumption', 'values': [{'date': '2019-10-27 12:00:00', 'value': 401.0}, {'date': '2019-10-27 12:15:00'
        energyDetails = seEnergy['energyDetails']
        if energyDetails['timeUnit'] != DataReadout.timeUnit:
            raise RuntimeError('Unexpected time unit received for detailed energy: ' + energyDetails['timeUnit'])
        
        energy = {}
        
        meters = energyDetails['meters']
        for meter in meters:
            meterType = meter['type']
            meterValues = meter['values']
            
            for value in meterValues:
                timestamp = DataReadout.parseDate(value['date'])
                if 'value' in value:
                    val = value['value']
                else:
                    val = 0
                
                if timestamp not in energy:
                    energy[timestamp] = (0, 0, 0, 0, 0, 0)
                
                entries = list(energy[timestamp])
                entries[DataReadout.energyTypes().index(meterType)] = val
                energy[timestamp] = tuple(entries)
        return energy
    
    @staticmethod
    def formatDate(date):
        return date.strftime(DataReadout.extFormat)
    
    @staticmethod
    def parseDate(dateStr):
        if ':' in dateStr:
            startFormat = DataReadout.extFormat
        else:
            startFormat = DataReadout.shortFormat
        return datetime.strptime(dateStr, startFormat)
    
    
    
    