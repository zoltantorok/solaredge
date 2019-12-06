'''
Created on 06.12.2019

@author: Zoli
'''
from solaredge import datareadout, solaredge
import argparse
from battery import batteryestimator, battery
from report import excelreporter
import datetime
from energycost import energycost, energycostcalculator

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-t', '--site_token', type=str, help='Site token of the solaredge inverter')
    parser.add_argument('-i', '--site_id', type=int, help='Site ID of the solaredge inverter')
    parser.add_argument('-s', '--start_date', type=str, help='Start date of energy readout in YYYY-MM-DD format')
    parser.add_argument('-e', '--end_date', type=str, help='End date of energy readout in YYYY-MM-DD format')
    parser.add_argument('-o', '--report_file', type=str, default='energy.xlsx', help='Output Excel report file')
    parser.add_argument('-a', '--acc_report_file', type=str, default='energy_accumulated.xlsx', help='Output Excel report file with accumulated energy')
    args = parser.parse_args()
    
    inverter = solaredge.Solaredge(args.site_token)
    readout = datareadout.DataReadout(inverter, args.site_id)
    energy = readout.getDetailedEnergy(args.start_date, args.end_date)
    
    energyCostHigh = 0.2526
    energyCostLow = 0.1901
    highWeekdays = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday']
    highTarifHours = (datetime.time(hour=7, minute=0), datetime.time(hour=18, minute=59, second=59))
    validFrom = datetime.datetime(year=2019, month=1, day=1)
    validTo = datetime.datetime(year=2019, month=12, day=31, hour=23, minute=59, second=59)
    cost = energycost.EnergyCost()
    cost.setDualTariffEnergyCost(energyCostHigh, highWeekdays, highTarifHours[0], highTarifHours[1], energyCostLow, validFrom, validTo)
    refund = 0.093
    cost.setConstantEnergyRefundPerKWh(refund=refund, validFrom=validFrom, validTo=validTo)
    costCalculator = energycostcalculator.EnergyCostCalculator(cost)

    reporter = excelreporter.ExcelReporter(args.report_file)
    reporter.writeEnergyData(energy, readout.energyTypes(), costCalculator)

    realBattery = battery.Battery(capacity=9300, chargingLossPercent=1, dischargingLossPercent=1, maxChargingPower=5000, maxDischargingPower=7000)
    batteryEstimator = batteryestimator.BatteryEstimator(realBattery)
    accumulatedEnergy = batteryEstimator.accumulateFeedInEnergy(energy, datareadout.DataReadout.energyTypes())

    reporter = excelreporter.ExcelReporter(args.acc_report_file)
    reporter.writeEnergyData(accumulatedEnergy, readout.energyTypes(), costCalculator)


















