import sys, mmap, gc, re, urllib.parse

m = 'magnet:?'
lm = len(m)

dead_regex = '|'.join([x.strip() for x in open('trz_dead').read().split('\n') if x and '#' not in x]).replace('.','\\.')
dead_regex = re.compile(dead_regex)

def build_magnet(res):
    if "dn" in res.keys():
        magnet = m+urllib.parse.urlencode({"xt": res["xt"]})+"&"+urllib.parse.urlencode({"dn": ''.join(res["dn"])})
    else:
        magnet = m+urllib.parse.urlencode({"xt": res["xt"]})
    magnet = magnet.replace("urn%3Abtih%3A", "urn:btih:")
    for tr in res["tr"]:
        if 'tr' in res.keys():
            magnet += "&"+urllib.parse.urlencode({"tr":tr})
    return magnet


seen = []
trz = {}
common_trackers = [x for x in open('trz').read().split('\n') if x]

with open(sys.argv[1], 'r+') as f:
    data = mmap.mmap(f.fileno(), 0, prot=mmap.PROT_READ)
    i = -1
    done = False
    lastline = None
    while True:
        i += 1
        same = []
        dns = []
        trs = []
        while True:
            if lastline == None:
                line = data.readline().decode('utf-8')
            else:
                line = lastline
                lastline = None
            if line.strip() == '':
                break
            res = urllib.parse.parse_qs(line[lm:-1])
            if "xt" not in res.keys():
                break
            res["xt"] = res["xt"][0].lower()
            if (len(same) == 0) or (res["xt"] == same[-1]["xt"]):
                same += [res]
            else:
                lastline = line
                break
        for t in same:
            if "dn" in t.keys() and ((len(dns) == 0) or (t["dn"][0] != dns[-1])):
                if "||" in t["dn"][0]:
                    for dn in t["dn"][0].split("||"):
                        dns += dn
                else:
                    dns += t["dn"]
            if "tr" in t.keys():
                trs += t["tr"]
        dn = "||".join(list(set(dns)))
        trs = list(set(trs))
        trs_ok = []
        for tr in trs:
            if dead_regex.findall(tr) != []:
                trs_ok.append(tr)
                if tr in trz.keys():
                    trz[tr] += 1
                else:
                    trz[tr] = 1
        if len(same) == 0:
            break
        trs_ok += common_trackers
        joined = {"xt": same[-1]["xt"], "dn": dn, "tr": trs_ok[0:4]}
        if joined["xt"] not in seen:
            sys.stdout.write(build_magnet(joined)+'\n')
            sys.stdout.flush()
        if (i % 1000) == 0:
            gc.collect()

open('trs', 'w').write('\n'.join(['\t'.join(reversed([str(y) for y in x])) for x in trz.items()]))
