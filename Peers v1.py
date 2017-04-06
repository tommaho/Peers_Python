import time
#targetID = 366252
meta = []
master = []


with open('School Metadata.psv', 'r') as f:
    for line in f:
        unitid, name, url, city, state, control, degree, locale, size = line.split('|')
        entry = {
            "unitid": int(unitid),
            "name": name.replace("'"," "),
            "url": "<a href=http://" + url + " target=new>" + url + "</a>",
            "city": city.replace("'"," "),
            "state": state.replace("'"," "),
            "control": control.replace("'"," "),
            "degree": degree.replace("'"," "),
            "locale": locale.replace("'"," "),
            "size": size.replace("'"," ")
            }
        meta.append(entry)

f.close()

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

f.close()

units = []

for r in meta:
    units.append(r['unitid'])


for targetID in units:

    #targetHashes = [] #set()
    report = []
    matches = {}
    counts = {}

    targetHashes = [a['cip-aw'] for a in master if a['unitid'] == targetID]

    # for entry in master:
    #     if unitid == targetID:
    #         print(unitid)
    #         targetHashes.add(cip_aw)
    #     else:
    #         print("unit: ", unitid)
    #         print("target: ", targetID)
    #         print('not match')


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

    for key, value in matches.items():
        exdata = [m for m in meta if m['unitid'] == key]

        pctMatch = 0 if matches[targetID] == 0 else value / matches[targetID]
        pctOfPrograms = 0 if counts[key] == 0 else value / counts[key]
        #pct of programs with div / 0 handling

        line = {
             "targetid": targetID,
            "targetmatches": matches[targetID],
            "unitid": key,
            #
            "name": exdata[0]['name'],
            "url": exdata[0]['url'],
            "city": exdata[0]['city'],
            "state": exdata[0]['state'],
            "control": exdata[0]['control'],
            "degree": exdata[0]['degree'],
            "locale": exdata[0]['locale'],
            "size": exdata[0]['size'],
            #
            "programs": counts[key],
            "matches": value,
            "pctMatch": '{:.0%}'.format(pctMatch),
            "pctOfPrograms": '{:.0%}'.format(pctOfPrograms)
        }
        report.append(line)

    report.sort(key=lambda x: x['matches'], reverse=True)

    target = open('output.txt', 'a') # need to append
    target.write(str(report[:25]) + ", \n")
    target.close

    t_end = time.time()
    print(time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(t_end)), "Wrote target: ", targetID)

## next school