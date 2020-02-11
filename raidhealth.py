#!/usr/bin/python
#
# Import the required modules
import textfsm
import csv
import EndaceDevices
from netmiko import ConnectHandler

def print_output_to_csv(output, filename, templateFilename):
    with open(templateFilename, "r") as template:
        re_table = textfsm.TextFSM(template)
    data = re_table.ParseText(output)
    with open(filename, 'a', newline='') as csvfile:
        writer = csv.writer(csvfile, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
        for row in data:
            writer.writerow(row)
        csvfile.close()
    return

def getRaidStatus(connection):
    connection.enable()
    #output device name
    output = connection.find_prompt()
    output += "\n"
    output += connection.send_command("show raid status")
    return output

def getDiskHealth(connection):
    connection.enable()
    #output device name
    output = connection.find_prompt()
    output += "\n"
    output += connection.send_command("terminal length 999")
    output +=  connection.send_command("show raid disk health")
    return output

raidcsvName = 'RaidStatus.csv'
raidTemplate = 'TextFSMTemplates/raidStatusTemplate.txt'
#diskcsvName = 'DiskHealth.csv'
#diskTemplate = 'TextFSMTemplates/diskHealthTemplate.txt'

with open(raidcsvName, "w", newline='') as raidcsv:
    writer = csv.writer(raidcsv, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
    writer.writerow(['Device', 'RAID Status', 'RAID Type', 'Capacity (GB)', 'Hotspare'])
    raidcsv.close()

#with open(diskcsvname, "w", newline = '') as diskcsv:
#    writer = csv.writer(rotcsv, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
#    writer.writerow(['Device', 'Serial Number', 'Health', 'Reallocated Sector', 'Current Pending Sector'
#        , 'Offline Uncorrectable', 'Overall State'])
#    diskcsv.close()

for device in EndaceDevices.staging_probes:
    connection = ConnectHandler(**device)
    raidStatus = getRaidStatus(connection)
#    diskHealth = getDiskHealth(connection)
    connection.disconnect()
    print_output_to_csv(raidStatus, raidcsvName, raidTemplate)
