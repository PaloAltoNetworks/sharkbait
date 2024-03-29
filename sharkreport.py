#!/usr/bin/env python3

import argparse
import json

parser = argparse.ArgumentParser(description='Generate sharkbait reports.')
parser.add_argument('--logfile', default='/tmp/sharkbait.log', help='The log filename')
args = parser.parse_args()
logfile = args.logfile

with open(logfile, 'r') as f:
    logs = f.readlines()

# Convert to JSON list
data = []
order = ["date", "severity", "url", "status", "message"]
for line in logs:
    details = line.split("|")
    details = [x.strip() for x in details]
    structure = {key:value for key, value in zip(order, details)}
    data.append(structure)

# Calculate totals
updates = sum(entry['status'] == '---' for entry in data)
not_found = sum(entry['status'] == '404' for entry in data)
allowed = sum(entry['status'] == '200' for entry in data)
blocked = sum(entry['status'] == '0' for entry in data)
url_blocked = sum(entry['status'] == '503' for entry in data)
unacceptable = sum(entry['status'] == '406' for entry in data)
total_blocked = blocked + url_blocked + not_found + unacceptable
total = len(data) - updates


# Print results
print('From logfile: {}'.format(logfile))
print('---------------------------------------------')
print('Malware download blocked:\t%d (%4.2f%%)' % (blocked, (blocked/total*100)))
print('Malware URL blocked:\t\t%d (%4.2f%%)' % (url_blocked, (url_blocked/total*100)))
print('Unknown Error:\t\t\t%d (%4.2f%%)' % (unacceptable, (unacceptable/total*100)))
print('Not Found:\t\t\t%d (%4.2f%%)' % (not_found, (not_found/total*100)))
print('---------------------------------------------')
print('Malware download successful:\t%d (%4.2f%%)' % (allowed, (allowed/total*100)))
print('---------------------------------------------')
print('Security Efficacy:\t\t%4.2f%%' % (total_blocked/total*100))
print('False Negative Rate:\t\t%4.2f%%' % (allowed/total*100))

