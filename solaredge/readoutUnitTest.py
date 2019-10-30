'''
Created on 28.10.2019

@author: Zoli
'''
import unittest
import solaredge
import datareadout
from datetime import datetime

class ReadoutUnitTest(unittest.TestCase):


    def testGetTimeFramesWeekly_TimeFrameShorterThanAWeek_SameTimeframeReturned(self):
        d = datareadout.DataReadout(solaredge.Solaredge(''), '')
        startDate = d.parseDate('2019-01-01 00:00:00')
        endDate = d.parseDate('2019-01-03')
        timeFrames = d.getTimeFramesWeekly(startDate, endDate)
        self.assertTrue(len(timeFrames) == 1)
        self.assertEqual(startDate, timeFrames[0][0])
        self.assertEqual(endDate, timeFrames[0][1])

    def testGetTimeFramesWeekly_TimeFrameLongerThanOneWeek_AllLimitsUnique(self):
        d = datareadout.DataReadout(solaredge.Solaredge(''), '')
        startDate = d.parseDate('2019-01-01 00:00:00')
        endDate = d.parseDate('2019-01-10')
        timeFrames = d.getTimeFramesWeekly(startDate, endDate)
        self.assertTrue(len(timeFrames) == 2)
        self.assertEqual(startDate, timeFrames[0][0])
        self.assertEqual(endDate, timeFrames[1][1])
        self.assertGreater(timeFrames[1][0], timeFrames[0][1])

    def testDetailedEnergyConversion_ExampleInputString_OutputAsExpected(self):
        seGetDetailedEnergyOutput = {'energyDetails': {'timeUnit': 'QUARTER_OF_AN_HOUR', 'unit': 'Wh',
                                                        'meters': [{'type': 'Purchased', 'values': [{'date': '2019-10-27 12:00:00', 'value': 1.0}]},
                                                                   {'type': 'SelfConsumption', 'values': [{'date': '2019-10-27 12:00:00', 'value': 2.0}]},
                                                                   {'type': 'FeedIn', 'values': [{'date': '2019-10-27 12:00:00', 'value': 3.0}]},
                                                                   {'type': 'Consumption', 'values': [{'date': '2019-10-27 12:00:00', 'value': 4.0}]},
                                                                   {'type': 'Production', 'values': [{'date': '2019-10-27 12:00:00', 'value': 5.0}]},
                                                                   {'type': 'Accumulated', 'values': [{'date': '2019-10-27 12:00:00', 'value': 6.0}]}
                                                                   ]}}
        d = datareadout.DataReadout(solaredge.Solaredge(''), '')
        energy = d.convertEnergyData(seGetDetailedEnergyOutput)
        expectedEnergies = 1
        self.assertEqual(expectedEnergies, len(energy))
        expectedEntriesPerTimestamp = 6
        energyEntry = energy[datetime.strptime('2019-10-27 12:00:00', '%Y-%m-%d %H:%M:%S')]
        self.assertEqual(expectedEntriesPerTimestamp, len(energyEntry))
        expectedValues = (4, 2, 3, 1, 5, 6)
        self.assertEqual(expectedValues, energyEntry)

    def testDetailedEnergyConversion_ExampleInputStringMissingValues_ValueSetToZero(self):
        seGetDetailedEnergyOutput = {'energyDetails': {'timeUnit': 'QUARTER_OF_AN_HOUR', 'unit': 'Wh',
                                                        'meters': [{'type': 'Purchased', 'values': [{'date': '2019-10-27 12:00:00', 'value': 1.0}]},
                                                                   {'type': 'SelfConsumption', 'values': [{'date': '2019-10-27 12:00:00'}]},
                                                                   {'type': 'FeedIn', 'values': [{'date': '2019-10-27 12:00:00', 'value': 3.0}]},
                                                                   {'type': 'Consumption', 'values': [{'date': '2019-10-27 12:00:00', 'value': 4.0}]},
                                                                   {'type': 'Production', 'values': [{'date': '2019-10-27 12:00:00', 'value': 5.0}]},
                                                                   {'type': 'Accumulated', 'values': [{'date': '2019-10-27 12:00:00', 'value': 6.0}]}
                                                                   ]}}
        d = datareadout.DataReadout(solaredge.Solaredge(''), '')
        energy = d.convertEnergyData(seGetDetailedEnergyOutput)
        expectedEnergies = 1
        self.assertEqual(expectedEnergies, len(energy))
        expectedEntriesPerTimestamp = 6
        energyEntry = energy[datetime.strptime('2019-10-27 12:00:00', '%Y-%m-%d %H:%M:%S')]
        self.assertEqual(expectedEntriesPerTimestamp, len(energyEntry))
        expectedValues = (4, 0, 3, 1, 5, 6)
        self.assertEqual(expectedValues, energyEntry)

if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()