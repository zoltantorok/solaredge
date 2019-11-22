'''
Created on 27.10.2019

@author: Zoli
'''
import unittest
import solaredge
from solaredge import datareadout
from visualise import dataplotter
import sys
from battery import batteryestimator
from battery import battery

class IntegrationTest(unittest.TestCase):
    site_token = ''
    site_id = 0

    def setUp(self):
        self.s = solaredge.Solaredge(self.site_token)
        self.startDate = '2019-10-23 00:00:00'
        #self.startDate = '2019-10-28 16:30:00'
        self.endDate ='2019-11-22 18:45:00'


    def tearDown(self):
        pass

    def testBasicCommunication(self):
        site_details = self.s.get_details(self.site_id)
        #overview = s.get_overview(self.site_id)
        timeUnit = 'QUARTER_OF_AN_HOUR'
        energy = self.s.get_energyDetails(self.site_id, self.startDate, self.endDate, None, timeUnit)
        
        print(site_details)
        print(energy)

    def testDetailedEnergyReadout(self):
        readout = datareadout.DataReadout(self.s, self.site_id)
        
        print('Header: ' + ' '.join(readout.meterTypes))
        energy = readout.getDetailedEnergy(self.startDate, self.endDate)
        print(energy)
        energyLabel = 'Energy * 15 minutes (Wh)'
        plotter = dataplotter.DataPlotter()
        plotter.plotDetailedEnergyData(energy, energyLabel, readout.meterTypes, figure=1, show=False)

        # Estimate energy with a battery
        realBattery = battery.Battery(capacity=9300, chargingLossPercent=1, dischargingLossPercent=1, maxChargingPower=5000, maxDischargingPower=7000)
        batteryEstimator = batteryestimator.BatteryEstimator(realBattery)
        newEnergy = batteryEstimator.accumulateFeedInEnergy(energy, readout.meterTypes)
        plotter = dataplotter.DataPlotter()
        plotter.plotDetailedEnergyData(newEnergy, energyLabel, readout.meterTypes, figure=2, show=True)

if __name__ == "__main__":
    if len(sys.argv) > 1:
        IntegrationTest.site_id = sys.argv.pop()
        IntegrationTest.site_token = sys.argv.pop()
    unittest.main()
    