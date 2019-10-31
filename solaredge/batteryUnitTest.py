'''
Created on 31.10.2019

@author: Zoli
'''
import unittest
import battery

class Test(unittest.TestCase):


    def setUp(self):
        pass

    def tearDown(self):
        pass


    def testBattery_chargingIdealBattery_chargedEnergyStored(self):
        testBattery = battery.Battery(capacity=1000, chargingLossPercent=0, dischargingLossPercent=0, maxChargingPower=1000, maxDischargingPower=1000)
        chargeEnergy = 100 # Wh
        
        returnedEnergy = testBattery.chargeDischargeBattery(chargeEnergy)
        
        expectedReturnedEnergy = 0
        self.assertEqual(expectedReturnedEnergy, returnedEnergy)

        self.assertEqual(chargeEnergy, testBattery.energy)

    def testBattery_chargingIdealBattery_dischargedEnergySubtracted(self):
        testBattery = battery.Battery(capacity=1000, chargingLossPercent=0, dischargingLossPercent=0, maxChargingPower=1000, maxDischargingPower=1000)
        chargeEnergy = 100 # Wh
        returnedEnergy = testBattery.chargeDischargeBattery(chargeEnergy)

        expectedReturnedEnergy = 0
        self.assertEqual(expectedReturnedEnergy, returnedEnergy)
        
        returnedEnergy = testBattery.chargeDischargeBattery(-chargeEnergy)
        self.assertEqual(expectedReturnedEnergy, returnedEnergy)
        
        expectedEnergy = 0
        self.assertEqual(expectedEnergy, testBattery.energy)

    def testBattery_chargingIdealBattery_OverloadedEnergyReturned(self):
        testBattery = battery.Battery(capacity=1000, chargingLossPercent=0, dischargingLossPercent=0, maxChargingPower=10000, maxDischargingPower=10000)
        chargeEnergy = 1000 # Wh
        overloadedEnergy = 100
        returnedEnergy = testBattery.chargeDischargeBattery(chargeEnergy + overloadedEnergy)
        self.assertEqual(overloadedEnergy, returnedEnergy)
        self.assertEqual(chargeEnergy, testBattery.energy)

    def testBattery_dischargingIdealBattery_EmptyBatteryReturnsDischargedEnergy(self):
        testBattery = battery.Battery(capacity=1000, chargingLossPercent=0, dischargingLossPercent=0, maxChargingPower=10000, maxDischargingPower=10000)
        dischargedEnergy = -100 # Wh
        returnedEnergy = testBattery.chargeDischargeBattery(dischargedEnergy)
        self.assertEqual(dischargedEnergy, returnedEnergy)
        expectedBatteryEnergy = 0
        self.assertEqual(expectedBatteryEnergy, testBattery.energy)

    def testBattery_dischargingIdealBattery_ChargedBatteryReturnsZero(self):
        testBattery = battery.Battery(capacity=1000, chargingLossPercent=0, dischargingLossPercent=0, maxChargingPower=10000, maxDischargingPower=10000)
        testBattery.energy = 100 # Wh
        dischargedEnergy = -10 # Wh
        returnedEnergy = testBattery.chargeDischargeBattery(dischargedEnergy)
        
        expectedReturnedEnergy = 0
        self.assertEqual(expectedReturnedEnergy, returnedEnergy)

    def testBattery_chargingIdealBatteryChargeWithZeroEnergy_NothingHappens(self):
        testBattery = battery.Battery(capacity=1000, chargingLossPercent=0, dischargingLossPercent=0, maxChargingPower=10000, maxDischargingPower=10000)
        chargedEnergy = 0 # Wh
        oldBatteryEnergy = testBattery.energy
        returnedEnergy = testBattery.chargeDischargeBattery(chargedEnergy)
        
        expectedReturnedEnergy = 0
        self.assertEqual(expectedReturnedEnergy, returnedEnergy)
        
        self.assertEqual(oldBatteryEnergy, testBattery.energy)

    def testBattery_chargingRealBattery_ChargingEnergyLossHappens(self):
        testBattery = battery.Battery(capacity=1000, chargingLossPercent=5, dischargingLossPercent=5, maxChargingPower=10000, maxDischargingPower=10000)
        chargeEnergy = 100 # Wh
        
        returnedEnergy = testBattery.chargeDischargeBattery(chargeEnergy)

        expectedBatteryEnergy = chargeEnergy * (100 - testBattery.chargingLossPercent) / 100
        self.assertEqual(expectedBatteryEnergy, testBattery.energy)
        
        expectedReturnedEnergy = 0
        self.assertEqual(expectedReturnedEnergy, returnedEnergy)

    def testBattery_dischargingRealBattery_DischargingEnergyLossHappens(self):
        testBattery = battery.Battery(capacity=1000, chargingLossPercent=5, dischargingLossPercent=5, maxChargingPower=10000, maxDischargingPower=10000)
        dischargedEnergy = -100 # Wh
        testBatteryInitialEnergy = 1000
        testBattery.energy = testBatteryInitialEnergy
        
        returnedEnergy = testBattery.chargeDischargeBattery(dischargedEnergy)

        expectedBatteryEnergy = testBatteryInitialEnergy + dischargedEnergy * (100 + testBattery.chargingLossPercent) / 100
        self.assertEqual(expectedBatteryEnergy, testBattery.energy)
        
        expectedReturnedEnergy = 0
        self.assertEqual(expectedReturnedEnergy, returnedEnergy)

    def testBattery_chargingRealBatteryWithTooHighPower_OverChargingEnergyReturned(self):
        testBattery = battery.Battery(capacity=1000, chargingLossPercent=0, dischargingLossPercent=0, maxChargingPower=100, maxDischargingPower=100)
        chargeEnergy = 100 # Wh
        
        returnedEnergy = testBattery.chargeDischargeBattery(chargeEnergy)

        self.assertEqual(chargeEnergy - returnedEnergy, testBattery.energy)
        
        expectedReturnedEnergy = chargeEnergy - testBattery.maxChargingPower / 4
        self.assertEqual(expectedReturnedEnergy, returnedEnergy)

    def testBattery_dischargingRealBatteryWithTooHighPower_OverDischargingEnergyReturned(self):
        testBattery = battery.Battery(capacity=1000, chargingLossPercent=0, dischargingLossPercent=0, maxChargingPower=100, maxDischargingPower=100)
        dischargedEnergy = -100 # Wh
        testBatteryInitialEnergy = 1000
        testBattery.energy = testBatteryInitialEnergy
        
        returnedEnergy = testBattery.chargeDischargeBattery(dischargedEnergy)

        self.assertEqual(testBatteryInitialEnergy + dischargedEnergy - returnedEnergy, testBattery.energy)
        
        expectedReturnedEnergy = dischargedEnergy + testBattery.maxDischargingPower / 4
        self.assertEqual(expectedReturnedEnergy, returnedEnergy)

if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    