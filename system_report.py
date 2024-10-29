#!/bin/python3
#Jake Paczkowski
#NSSA 221 Script 2

#Import modules
import platform
import subprocess
import os
import datetime
import sys

#Color codess for text output
GREEN = '\033[92m'
RED = '\033[91m'
RESET = '\033[0m'

#retrieve host name
def get_hostname():
    return platform.node().split('.')[0]
#retrieve the domain
def get_domain():
    return platform.node().split('.')[1]

#Get_network_info will retrieve the ip address, default gateway and network mask
def get_network_info():
    try:
        output = os.popen('ifconfig').read()

        for line in output.split('\n'):
            if 'inet ' in line:
                ipAddress = line.split()[1]
                break
    except Exception as e:
        print("Error:" , e)
    try:
        read = os.popen('ip route | grep default').read()
        defaultGw = read.split()[2]
    except Exception as e:
        print("Error: ", e)

    try:
        getMask = os.popen('ip addr').read()

        for line in getMask.split('\n'):
            if 'inet ' in line:
                netMask = line.split()[4]
                break
    except Exception as e:
        print("Error:" , e)
    
    




    return ipAddress, defaultGw, netMask

#get_dns function will retreive the systems 2 dns modules
def get_dns():
    dns1 = None
    dns2 = None
    try:
        with open('/etc/resolv.conf' , 'r') as f:
            for line in f:
                if line.startswith('nameserver'):
                    if dns1 is None:
                        dns1 = line.split()[1]
                    else:
                        dns2 = line.split()[1]
                        break
    except Exception as e:
        print("Error: " , e)

    return dns1, dns2
#get_os_info will retrieve the systems operating system information
def get_os_info():
    osName, osVersion, _ = platform.linux_distribution()
    kernel = os.uname().release

    return osName, osVersion, kernel

#get_disk_info will retrieve the systems hard drive information
def get_disk_info():
    try:
        output = os.popen('df -k').read()
        lines = output.split('\n')[1:]
        initCap = 0
        initSpace = 0
        totalCap = 0
        totalSpace = 0

        for line in lines:
            if line:
                parts = line.split()
                initCap += int(parts[1])
                initSpace += int(parts[3])
        totalCap = round(initCap / (1024 * 1024))
        totalSpace = round(initSpace / (1024 * 1024))


    except Exception as e:
        print("Error: ", e)
    return totalCap, totalSpace

#get_cpu_info will retrieve information about the systems processing unit
def get_cpu_info():
    cpu_name = "Unknown"
    num_processors = 0
    num_cores = 0

    try:
        with open('/proc/cpuinfo', 'r') as cpuinfo_file:
            cpuinfo_data = cpuinfo_file.read()

        # Search for CPU name
        for line in cpuinfo_data.split('\n'):
            if line.startswith("model name"):
                cpu_name = line.split(":")[1].strip()
                break

        # Count the number of processors
        for line in cpuinfo_data.split('\n'):
            if line.startswith("processor"):
                num_processors = 1

        # Count the number of cores
        for line in cpuinfo_data.split('\n'):
            if line.startswith("cpu cores"):
                num_cores = int(line.split(":")[1].strip())
                break

    except Exception as e:
        print("Error:", e)

    return cpu_name, num_processors, num_cores

#get ram will retireve info about the systems RAM storage
def get_ram():
    totalRam = None
    freeRam = None

    try:
        output = os.popen('free -h').read()

        lines = output.split("\n")

        for line in lines:
            if line.startswith("Mem:"):
                parts = line.split()
                totalRam = parts[1]
                freeRam = parts[6]
                break
    except Exception as e:
        print("Error: ", e)

    return totalRam, freeRam

def main():
    #Assign variables
    host = get_hostname()
    domain = get_domain()
    ipAddress, defaultgw, netmask  = get_network_info()
    dns1, dns2 = get_dns()
    osName, osVersion, kernel = get_os_info()
    totalCap, space = get_disk_info()
    model, processors, cores = get_cpu_info()
    totalRam, freeRam = get_ram()
   
    date = datetime.datetime.now()
    #Output info to the user
    print(RED + "Date: " + RESET, date)
   
    print(GREEN + "Device Information" + RESET)
    print("Hostname: " + host)
    print("Domain: " + domain)

    print(GREEN + "Network Information" + RESET)
    print("IP Address:      " + ipAddress)
    print("Gateway:         " + defaultgw)
    print("Network Mask:    " + netmask)
    print("DNS1:            " + dns1)
    print("DNS2:            " + dns2)

    print(GREEN + "OS Information" + RESET)
    print("Operating System:        " + osName)
    print("Operating Version:       " + osVersion)
    print("Kernel Version:          " + kernel)


    print(GREEN + "Storage Information" + RESET)
    print("Hard Drive Capacity:       ", totalCap )
    print("Available Space            ", space )

    print(GREEN + "Processor Information" + RESET)
    print("CPU Model:                   "+ model)
    print("Number of Processors:        ", processors)
    print("Number of Cores:             ", cores)

    print(GREEN + "Memory Information" + RESET)
    print("Total RAM:                " + totalRam)
    print("Available RAM:            " + freeRam)

#Call the main function
main()

host = get_hostname()

logfilePath = os.path.join(os.path.expanduser("~"),f"{host}_system_report.log")

with open(logfilePath, 'w') as logFile:
    sys.stdout = logFile

    main()




