import time
targetID = 366252
master = []
report = []# distinct IDs
targetHashes = set() #Hashes of just the primary cip-awlevels

t_start = time.time()
print("Start: ", time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(t_start)))


with open('Source Data v2.csv', 'r') as f:
    for line in f:
        unitid, cip, awlevel = map(int, line.split(','))
        cip_aw = (cip, awlevel)
        entry = {
            "unitid": unitid,
            "cip-aw": cip_aw
            }
        master.append(entry)

        if unitid == targetID:
            targetHashes.add(cip_aw)
f.close()

matches = {}
counts = {}

for entry in master:

    if entry['cip-aw'] in targetHashes:
        matchCount = 1
    else:
        matchCount = 0

    if entry['unitid'] in matches:
        matches[entry['unitid']] += matchCount
    else:
        matches[entry['unitid']] = matchCount

    if entry['unitid'] in counts:
        counts[entry['unitid']] += 1
    else:
        counts[entry['unitid']] = 1

for unit, matchcount in matches.items():
    line = {
         "targetid": targetID,
        "targetmatches": matches[targetID],
        "unitid": unit,
        "programs": counts[unit],
        "matches": matchcount,
        "pctMatch": matchcount / matches[targetID],
        "pctOfPrograms": matchcount / counts[unit]
    }
    report.append(line)

report.sort(key=lambda x: x['pctMatch'], reverse=True)

t_end = time.time()
print("End: ", time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(t_end)))


print(report[:25])
