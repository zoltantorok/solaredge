'''
Created on 29.10.2019

@author: Zoli
'''
import unittest
from solaredge import datareadout
import json
import batteryestimator
import battery
import datetime

class BatteryEstimatorUnitTest(unittest.TestCase):
    testDataDetailedEnergy = '../solaredge/testDetailedEnergyString.txt'

    def setUp(self):
        testDataFile = open(self.testDataDetailedEnergy, 'r')
        testDataAlmostJsonString = testDataFile.read()
        testDataFile.close()
        testDataJsonString = testDataAlmostJsonString.replace("\'", "\"")
        testData = json.loads(testDataJsonString)
        self.testData = datareadout.DataReadout.convertEnergyData(testData) 
        self.energyTypes = datareadout.DataReadout.energyTypes()

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
        
    def testBatteryEstimator_UseRealBattery_PurchasedEnergyDecreasesWithBattery(self):
        realBattery = battery.Battery(capacity=9300, chargingLossPercent=1, dischargingLossPercent=1, maxChargingPower=5000, maxDischargingPower=7000)
        batteryEstimator = batteryestimator.BatteryEstimator(realBattery)

        oct30energyData = {}
        for key in self.testData.keys():
            if key >= datetime.datetime(year=2019, month=10, day=29, hour=0, minute=0, second=0) and key < datetime.datetime(year=2019, month=10, day=30, hour=0, minute=0, second=0):
                oct30energyData[key] = self.testData[key]
        
        accumulatedEnergy = batteryEstimator.accumulateFeedInEnergy(oct30energyData, self.energyTypes)
        
        oldSums = [sum(x) for x in zip(*oct30energyData.values())]
        newSums = [sum(x) for x in zip(*accumulatedEnergy.values())]

        self.assertGreater(oldSums[self.energyTypes.index('Purchased')], newSums[self.energyTypes.index('Purchased')])

if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()























