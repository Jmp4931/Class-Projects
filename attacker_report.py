#!/bin/python3
#Jake Paczkowski
#NSSA-221 Script 4

#import modules
import re
import subprocess
from datetime import datetime
from collections import Counter
from geoip import geolite2

#Color codes for text output
GREEN = '\033[92m'
RED = '\033[91m'
RESET = '\033[0m'


#clear the terminal
def clear_terminal():
    subprocess.run('clear')

#parse_log_file was search for IP addresses from syslog.log
def parse_log_file(log_file):
    ip_list = []
    with open(log_file, 'r') as file:
        for line in file:
            match = re.search(r'rhost=(\S+)', line)
            if match:
                ip_list.append(match.group(1))
    return ip_list

#get_country will find the country associated with the ip address of the failed login using geoip module
def get_country(ip_list):
    countries = []
    for ip in ip_list:
        match = geolite2.lookup(ip)
        if match:
            countries.append(match.country)
    return countries

# Generate the report listing the ip addressses, attempted logins and the country of origin
def generate_report(ip_count, ip_countries):
    print(GREEN, "Server Login Attempt Report", RESET)
    print("Date:", datetime.now().strftime('%Y-%m-%d'))
    print("\nIP Address\tCount\tCountry")
    print("===========================================")
    for ip, count in ip_count.items():
        country = ip_countries[ip]
        print(f"{ip}\t{count}\t{country}")

# Main function
def main():
    clear_terminal()
    log_file = 'syslog.log'
    ip_list = parse_log_file(log_file)
    #count the amount of times an ip is in the list
    ip_count = Counter(ip_list)
    #only gtrab ip's with 10 or more login attempts
    ip_count = {k: v for k, v in ip_count.items() if v >= 10}  
    ip_countries = {ip: get_country([ip])[0] for ip in ip_count.keys()}
    ip_count_sorted = dict(sorted(ip_count.items(), key=lambda item: item[1]))
    generate_report(ip_count_sorted, ip_countries)


main()
