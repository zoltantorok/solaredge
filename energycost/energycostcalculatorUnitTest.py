'''
Created on 31.10.2019

@author: Zoli
'''
import unittest
import energycostcalculator
import energycost
import datetime

class EnergyCostCalculatorUnitTest(unittest.TestCase):
    testDataDetailedEnergy = 'testDetailedEnergyString.txt'

    def setUp(self):
        self.energyTypes = ['', '', 'FeedIn', 'Purchased']
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

    def testEnergyCostCalculation_EnergyPurchased_CostEqualsExpected(self):
        energyPerQuarterOfAnHourWh = 250
        # Low tariff
        testData = {datetime.datetime(2019, 11, 21, 0, 0): (0, 0, 0, energyPerQuarterOfAnHourWh, 0, 0),
                    datetime.datetime(2019, 11, 21, 0, 15): (0, 0, 0, energyPerQuarterOfAnHourWh, 0, 0),
                    datetime.datetime(2019, 11, 21, 0, 30): (0, 0, 0, energyPerQuarterOfAnHourWh, 0, 0),
                    datetime.datetime(2019, 10, 21, 0, 45): (0, 0, 0, energyPerQuarterOfAnHourWh, 0, 0)}
        cost = self.costCalculator.calculateCost(testData, self.energyTypes)
        
        self.assertEqual(self.energyCostLow, cost)

        # High tariff
        testData = {datetime.datetime(2019, 11, 21, 8, 0): (0, 0, 0, energyPerQuarterOfAnHourWh, 0, 0),
                    datetime.datetime(2019, 11, 21, 8, 15): (0, 0, 0, energyPerQuarterOfAnHourWh, 0, 0),
                    datetime.datetime(2019, 11, 21, 8, 30): (0, 0, 0, energyPerQuarterOfAnHourWh, 0, 0),
                    datetime.datetime(2019, 10, 21, 8, 45): (0, 0, 0, energyPerQuarterOfAnHourWh, 0, 0)}
        cost = self.costCalculator.calculateCost(testData, self.energyTypes)
        
        self.assertEqual(self.energyCostHigh, cost)

    def testEnergyCostCalculation_EnergyFedIn_RefundEqualsExpected(self):
        energyPerQuarterOfAnHourWh = 250
        testData = {datetime.datetime(2019, 11, 21, 0, 0): (0, 0, energyPerQuarterOfAnHourWh, 0, 0, 0),
                    datetime.datetime(2019, 11, 21, 0, 15): (0, 0, energyPerQuarterOfAnHourWh, 0, 0, 0),
                    datetime.datetime(2019, 11, 21, 0, 30): (0, 0, energyPerQuarterOfAnHourWh, 0, 0, 0),
                    datetime.datetime(2019, 10, 21, 0, 45): (0, 0, energyPerQuarterOfAnHourWh, 0, 0, 0)}
        cost = self.costCalculator.calculateCost(testData, self.energyTypes)
        
        self.assertEqual(-self.refund, cost)


if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()