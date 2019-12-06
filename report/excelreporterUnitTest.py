'''
Created on 24.11.2019

@author: Zoli
'''
import unittest
import json
from solaredge import datareadout
import excelreporter
import os
import datetime
from energycost import energycost, energycostcalculator

class ExcelReporterUnitTest(unittest.TestCase):
    testDataDetailedEnergy = '../solaredge/testDetailedEnergyString.txt'
    outputTestFile = 'report.xlsx'
    outputTestFileBattery = 'reportBattery.xlsx'

    def setUp(self):
        testDataFile = open(self.testDataDetailedEnergy, 'r')
        testDataAlmostJsonString = testDataFile.read()
        testDataFile.close()
        testDataJsonString = testDataAlmostJsonString.replace("\'", "\"")
        testData = json.loads(testDataJsonString)
        self.testData = datareadout.DataReadout.convertEnergyData(testData) 
        self.energyTypes = datareadout.DataReadout.energyTypes()
        
        self.energyCostHigh = 0.2526
        self.energyCostLow = 0.1901
        highWeekdays = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday']
        highTarifHours = (datetime.time(hour=7, minute=0), datetime.time(hour=18, minute=59, second=59))
        validFrom = datetime.datetime(year=2019, month=1, day=1)
        validTo = datetime.datetime(year=2019, month=12, day=31, hour=23, minute=59, second=59)
        cost = energycost.EnergyCost()
        cost.setDualTariffEnergyCost(self.energyCostHigh, highWeekdays, highTarifHours[0], highTarifHours[1], self.energyCostLow, validFrom, validTo)
        self.refund = 0.093
        cost.setConstantEnergyRefundPerKWh(refund=self.refund, validFrom=validFrom, validTo=validTo)
        self.costCalculator = energycostcalculator.EnergyCostCalculator(cost)


    def tearDown(self):
        pass

    def testEnergyDataWritingToExcelFile(self):
        reporter = excelreporter.ExcelReporter(self.outputTestFile)
        reporter.writeEnergyData(self.testData, self.energyTypes, self.costCalculator)
        self.assertTrue(os.path.isfile(self.outputTestFile))

    def testAccumulatedEnergyDataWritingToExcelFile(self):
        reporter = excelreporter.ExcelReporter(self.outputTestFileBattery)
        reporter.writeEnergyData(self.testData, self.energyTypes, self.costCalculator)
        self.assertTrue(os.path.isfile(self.outputTestFileBattery))


if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()



















