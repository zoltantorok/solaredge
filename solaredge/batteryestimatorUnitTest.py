'''
Created on 29.10.2019

@author: Zoli
'''
import unittest
import datareadout
import solaredge
import json
import batteryestimator
import battery
from dataplotter import DataPlotter

class BatteryEstimatorUnitTest(unittest.TestCase):
    testDataDetailedEnergy = 'testDetailedEnergyString.txt'

    def setUp(self):
        dataReader = datareadout.DataReadout(solaredge.Solaredge(''), 0)
        testDataFile = open(self.testDataDetailedEnergy, 'r')
        testDataAlmostJsonString = testDataFile.read()
        testDataFile.close()
        testDataJsonString = testDataAlmostJsonString.replace("\'", "\"")
        testData = json.loads(testDataJsonString)
        self.testData = dataReader.convertEnergyData(testData) 
        self.energyTypes = dataReader.meterTypes

    def tearDown(self):
        pass


    def testBatteryEstimator_AttachIdealBattery_EnergyChecksPass(self):
        idealBattery = battery.Battery(capacity=9300, chargingLossPercent=0, dischargingLossPercent=0, maxChargingPower=5000, maxDischargingPower=7000)
        batteryEstimator = batteryestimator.BatteryEstimator(idealBattery)
        newEnergy = batteryEstimator.accumulateFeedInEnergy(self.testData, self.energyTypes)
        
        oldSums = [sum(x) for x in zip(*self.testData.values())]
        newSums = [sum(x) for x in zip(*newEnergy.values())]
        
        self.assertEqual(oldSums[self.energyTypes.index('Production')], newSums[self.energyTypes.index('Production')])
        self.assertEqual(oldSums[self.energyTypes.index('Consumption')], newSums[self.energyTypes.index('Consumption')])
        self.assertGreater(newSums[self.energyTypes.index('SelfConsumption')], oldSums[self.energyTypes.index('SelfConsumption')])
        self.assertEqual(newSums[self.energyTypes.index('Production')] + newSums[self.energyTypes.index('Purchased')],
                         newSums[self.energyTypes.index('Consumption')] + newSums[self.energyTypes.index('FeedIn')] +
                         newSums[self.energyTypes.index('Accumulated')])
        #self.assertEqual(oldSums[self.energyTypes.index('Production')] + oldSums[self.energyTypes.index('Purchased')],
        #                 oldSums[self.energyTypes.index('Consumption')] + oldSums[self.energyTypes.index('FeedIn')])
        

if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()