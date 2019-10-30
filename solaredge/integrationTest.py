'''
Created on 27.10.2019

@author: Zoli
'''
import unittest
import solaredge
import datareadout
from dataplotter import DataPlotter
import sys
import batteryestimator

class IntegrationTest(unittest.TestCase):
    site_token = ''
    site_id = 0

    def setUp(self):
        self.s = solaredge.Solaredge(self.site_token)
        self.startDate = '2019-10-23 00:00:00'
        #self.startDate = '2019-10-28 16:30:00'
        self.endDate ='2019-10-30 17:00:00'


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
        plotter = DataPlotter()
        plotter.plotDetailedEnergyData(energy, readout.meterTypes, figure=1, show=False)

        # Estimate energy with a battery
        batteryEstimator = batteryestimator.BatteryEstimator()
        batteryCapacity = 9000 # Wh
        newEnergy = batteryEstimator.accumulateFeedInEnergy(energy, readout.meterTypes, batteryCapacity)
        plotter = DataPlotter()
        plotter.plotDetailedEnergyData(newEnergy, readout.meterTypes, figure=2, show=True)

if __name__ == "__main__":
    if len(sys.argv) > 1:
        IntegrationTest.site_id = sys.argv.pop()
        IntegrationTest.site_token = sys.argv.pop()
    unittest.main()
    