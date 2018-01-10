# Azure-Maint-Status
This is a Python Flask app I wrote that monitors the Azure Instance Metadata Service to tell whether or not an Instance is set to reboot. 

This is based on: https://docs.microsoft.com/en-us/azure/virtual-machines/windows/instance-metadata-service

When hit on :8088, it will hit the Azure Instance Metadata Service which is sitting on the APIPA address space for the Instance this is running on. If the length of the JSON result is 0, then a 200 OK is returned. Else a 503 HTTP code is returned.

This was hooked up originally to an Orion Solarwinds monitoring system which was looking for a 200 OK, and would alert on a 503.

# Install
Install using the AzureStatusInstall.yml Ansible playbook.
