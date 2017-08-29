import sys, mmap, gc, urllib.parse

m = 'magnet:?'
lm = len(m)

def build_magnet(res):
    if "dn" in res.keys():
        magnet = m+urllib.parse.urlencode({"xt": res["xt"], "dn": ''.join(res["dn"])})
    else:
        magnet = m+urllib.parse.urlencode({"xt": res["xt"]})
    magnet = magnet.replace("urn%3Abtih%3A", "urn:btih:")
    if 'tr' in res.keys():
        for tr in res['tr']:
            magnet += "&"+urllib.parse.urlencode({"tr":tr})
    return magnet


seen = []
trz = {}
with open(sys.argv[1], 'r+') as f:
    data = mmap.mmap(f.fileno(), 0, prot=mmap.PROT_READ)
    i = -1
    done = False
    lastline = None
    break_count = 0
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
                break_count += 1
            res = urllib.parse.parse_qs(line[lm:-1])
            if "xt" not in res.keys():
                raise Exception(res)
            res["xt"] = res["xt"][0].lower()
            if (len(same) == 0) or (res["xt"] == same[-1]["xt"]):
                same += [res]
            else:
                lastline = line
                break
        for t in same:
            if "dn" in t.keys() and ((len(dns) == 0) or (t["dn"][0] != dns[-1])):
                dns += t["dn"]
            if "tr" in t.keys():
                trs += t["tr"]
        dns = list(set(dns))
        dn = "||".join(dns)
        trs = list(set(trs))
        for tr in trs:
            if tr in trz.keys():
                trz[tr] += 1
            else:
                trz[tr] = 1
        joined = {"xt": same[-1]["xt"], "dn": dn, "tr": trs}
        if joined["xt"] not in seen:
            sys.stdout.write(build_magnet(joined)+'\n')
            sys.stdout.flush()
        if (i % 1000) == 0:
            gc.collect()
        if break_count > 10:
            break

open('trs', 'w').write('\n'.join(['\t'.join(reversed([str(y) for y in x])) for x in trz.items()]))
