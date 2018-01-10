# Azure-Maint-Status
This is a Python Flask app I wrote that monitors the Azure Instance Metadata Service to tell whether or not an Instance is set to reboot. 

This is based on: https://docs.microsoft.com/en-us/azure/virtual-machines/windows/instance-metadata-service

The idea is to extend this into another monitoring solution such as Orion Solarwinds. In the event that the JSON response is populated, you would then alert or send some type of notification of that event. This would help RCA investigations as to why a service was interrupted or why a machine was down for an amount of time.
