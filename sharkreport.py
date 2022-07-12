#!/usr/bin/env python3

import argparse
import json

parser = argparse.ArgumentParser(description='Generate sharkbait reports.')
parser.add_argument('logfile', help='The log filename')
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
total = len(data)
allowed = sum(entry['status'] == '200' for entry in data)
blocked = sum(entry['status'] == '0' for entry in data)
url_blocked = sum(entry['status'] == '503' for entry in data)
not_found = sum(entry['status'] == '404' for entry in data)
unacceptable = sum(entry['status'] == '406' for entry in data)
total_blocked = blocked + url_blocked + not_found + unacceptable

# Print results
print('---')
print('Malware download blocked: %d (%4.2f%%)' % (blocked, (blocked/total*100)))
print('Malware URL blocked: %d (%4.2f%%)' % (url_blocked, (url_blocked/total*100)))
print('Unknown Error: %d (%4.2f%%)' % (unacceptable, (unacceptable/total*100)))
print('Not Found: %d (%4.2f%%)' % (not_found, (not_found/total*100)))
print('---')
print('Malware download successful: %d (%4.2f%%)' % (allowed, (allowed/total*100)))
print('---')
print('Security Efficacy: %4.2f%%' % (total_blocked/total*100))
print('False Negative Rate: %4.2f%%' % (allowed/total*100))









# for entry in data:
#     print(json.dumps(entry, indent = 4))
