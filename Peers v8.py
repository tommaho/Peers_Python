import time
targetID = 366252
master = []
units = []# distinct IDs
targetHashes = set() #Hashes of just the primary cip-awlevels

t_start = time.time()
print("Start: ", time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(t_start)))

def updateExistingUnit(unitid, matchCount):
    for line in units:
         if line['unitid'] == unitid:
            line['programs'] += 1
            line['matches'] += matchCount
            return True
    return False

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

for entry in master:

    if entry['cip-aw'] in targetHashes:
        matchCount = 1
    else:
        matchCount = 0

    if not updateExistingUnit(entry['unitid'], matchCount):
        unit = {
            "unitid": entry['unitid'],
            "programs": 1,
            "matches": matchCount,
            "pctMatch": 0.0,
            "pctOfPrograms": 0.0
        }
        units.append(unit)

#units.sort(key=lambda x: x['matches'], reverse=True)

t_end = time.time()
print("End: ", time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(t_end)))


