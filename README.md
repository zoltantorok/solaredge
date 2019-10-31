# Solaredge
Using API wrapper for Solaredge monitoring service from bertouttier/solaredge.

See https://www.solaredge.com/sites/default/files/se_monitoring_api.pdf

I have a photovoltaic system with a Solaredge inverter but currently without a battery.
I would like to estimate how much money I could save if I installed a battery with a certain capacity.
The aim of this repository is to develop python tools which allow one to
* read out all relevant energy data from the inverter for a certain time period
* visualise the energy data
* simulate the existence of a battery with a given capacity (charging and discharging losses, limitation of the maximum charging and discharging powers)
* calculate energy costs (next step)
