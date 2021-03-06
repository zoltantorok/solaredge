'''
Created on 10.11.2019

@author: Zoli
'''
import unittest
import energycost
import datetime

class EnergyCostUnitTest(unittest.TestCase):


    def setUp(self):
        self.validFrom = datetime.datetime(year=2019, month=1, day = 1)
        self.validTo = datetime.datetime(year=2019, month=12, day = 31, hour = 23, minute = 59, second = 59)
        self.validTestDate = datetime.datetime(year = 2019, month = 4, day = 1, hour=10, minute=0)
        self.validTestDateDifferentWeekDay = datetime.datetime(year = 2019, month = 4, day = 5, hour=10, minute=0)
        self.invalidTestDateBefore = datetime.datetime(year = 2018, month = 4, day = 1)
        self.invalidTestDateAfter = datetime.datetime(year = 2020, month = 4, day = 1)
        self.invalidTestOnEdgeBefore = datetime.datetime(year = 2018, month = 12, day = 31, hour = 23, minute = 59, second = 59)
        self.validTestOnEdge = datetime.datetime(year = 2019, month = 1, day = 1, hour = 0, minute = 0, second = 0)
        self.validTestOnEdge2 = datetime.datetime(year = 2019, month = 12, day = 31, hour = 23, minute = 59, second = 59)
        self.validFromNextYear = datetime.datetime(year=2020, month=1, day = 1)
        self.validToNextYear = datetime.datetime(year=2020, month=12, day = 31, hour = 23, minute = 59, second = 59)
        self.validTestDateNextYear = datetime.datetime(year = 2020, month = 4, day = 1, hour=10, minute=0)


    def tearDown(self):
        pass


    def testConstantEnergyCost_GetVariousDates_ExpectedValueReturnedOrRaise(self):
        cost = energycost.EnergyCost()
        energyCost = 0.2
        cost.setConstantEnergyCostPerKWh(energyCost, self.validFrom, self.validTo)
        
        self.assertEqual(energyCost, cost.getEnergyCost(self.validTestDate))

        self.assertEqual(energyCost, cost.getEnergyCost(self.validTestDateDifferentWeekDay))
        
        self.assertRaises(RuntimeError, cost.getEnergyCost, self.invalidTestDateBefore)

        self.assertRaises(RuntimeError, cost.getEnergyCost, self.invalidTestDateAfter)

        self.assertRaises(RuntimeError, cost.getEnergyCost, self.invalidTestOnEdgeBefore)

        self.assertEqual(energyCost, cost.getEnergyCost(self.validTestOnEdge))

        self.assertEqual(energyCost, cost.getEnergyCost(self.validTestOnEdge2))

    def testConstantEnergyRefund_GetVariousDates_ExpectedValueReturnedOrRaise(self):
        cost = energycost.EnergyCost()
        energyRefund = 0.2
        cost.setConstantEnergyRefundPerKWh(energyRefund, self.validFrom, self.validTo)
        
        self.assertEqual(energyRefund, cost.getEnergyRefund(self.validTestDate))

        self.assertEqual(energyRefund, cost.getEnergyRefund(self.validTestDateDifferentWeekDay))
        
        self.assertRaises(RuntimeError, cost.getEnergyRefund, self.invalidTestDateBefore)

        self.assertRaises(RuntimeError, cost.getEnergyRefund, self.invalidTestDateAfter)

        self.assertRaises(RuntimeError, cost.getEnergyRefund, self.invalidTestOnEdgeBefore)

        self.assertEqual(energyRefund, cost.getEnergyRefund(self.validTestOnEdge))

        self.assertEqual(energyRefund, cost.getEnergyRefund(self.validTestOnEdge2))

    def testDualTarifEnergyCost_GetVariousDates_ExpectedValueReturnedOrRaise(self):
        cost = energycost.EnergyCost()
        energyCostHigh = 0.2
        energyCostLow = 0.1
        highWeekdays = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday']
        highTarifHours = (datetime.time(hour=7, minute=0), datetime.time(hour=18, minute=59, second=59))
        cost.setDualTariffEnergyCost(energyCostHigh, highWeekdays, highTarifHours[0], highTarifHours[1], energyCostLow, self.validFrom, self.validTo)
        
        self.assertEqual(energyCostHigh, cost.getEnergyCost(self.validTestDate))

        self.assertEqual(energyCostHigh, cost.getEnergyCost(self.validTestDateDifferentWeekDay))
        
        self.assertRaises(RuntimeError, cost.getEnergyCost, self.invalidTestDateBefore)

        self.assertRaises(RuntimeError, cost.getEnergyCost, self.invalidTestDateAfter)

        self.assertRaises(RuntimeError, cost.getEnergyCost, self.invalidTestOnEdgeBefore)

        self.assertEqual(energyCostLow, cost.getEnergyCost(self.validTestOnEdge))

        self.assertEqual(energyCostLow, cost.getEnergyCost(self.validTestOnEdge2))

        self.lowTarifStart1 = datetime.datetime(year = 2019, month = 11, day = 21, hour = 0, minute = 0, second = 0)
        self.assertEqual(energyCostLow, cost.getEnergyCost(self.lowTarifStart1))

        self.lowTarifEnd1 = datetime.datetime(year = 2019, month = 11, day = 21, hour = 6, minute = 59, second = 59)
        self.assertEqual(energyCostLow, cost.getEnergyCost(self.lowTarifEnd1))

        self.highTarifStart = datetime.datetime(year = 2019, month = 11, day = 21, hour = 7, minute = 0, second = 0)
        self.assertEqual(energyCostHigh, cost.getEnergyCost(self.highTarifStart))

        self.highTarifEnd = datetime.datetime(year = 2019, month = 11, day = 21, hour = 18, minute = 59, second = 59)
        self.assertEqual(energyCostHigh, cost.getEnergyCost(self.highTarifEnd))

        self.lowTarifStart2 = datetime.datetime(year = 2019, month = 11, day = 21, hour = 19, minute = 0, second = 0)
        self.assertEqual(energyCostLow, cost.getEnergyCost(self.lowTarifStart2))

        self.lowTarifEnd2 = datetime.datetime(year = 2019, month = 11, day = 21, hour = 23, minute = 59, second = 59)
        self.assertEqual(energyCostLow, cost.getEnergyCost(self.lowTarifEnd2))

        for h in range(0, 23):
            self.lowTarifWeekend = datetime.datetime(year = 2019, month = 11, day = 24, hour = h, minute = 0, second = 0)
            self.assertEqual(energyCostLow, cost.getEnergyCost(self.lowTarifWeekend))

    def testDualTarifEnergyCostWithTwoYears_GetVariousDates_ExpectedValueReturnedOrRaise(self):
        cost = energycost.EnergyCost()
        energyCostHigh = 0.2
        energyCostLow = 0.1
        energyCostHighNextYear = 0.3
        energyCostLowNextYear = 0.2
        highWeekdays = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday']
        highTarifHours = (datetime.time(hour=7, minute=0), datetime.time(hour=18, minute=59, second=59))
        cost.setDualTariffEnergyCost(energyCostHigh, highWeekdays, highTarifHours[0], highTarifHours[1], energyCostLow, self.validFrom, self.validTo)
        cost.setDualTariffEnergyCost(energyCostHighNextYear, highWeekdays, highTarifHours[0], highTarifHours[1],
                                     energyCostLowNextYear, self.validFromNextYear, self.validToNextYear)
        
        self.assertEqual(energyCostHigh, cost.getEnergyCost(self.validTestDate))
        self.assertEqual(energyCostHighNextYear, cost.getEnergyCost(self.validTestDateNextYear))
            
if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    