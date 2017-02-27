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
with open(sys.argv[1], 'r+') as f:
    data = mmap.mmap(f.fileno(), 0, prot=mmap.PROT_READ)
    i = -1
    done = False
    while True:
        i += 1
        same = []
        trs = []
        dns = []
        while True:
            line = data.readline().decode('utf-8')
            if line.strip() == '':
                break
            res = urllib.parse.parse_qs(line[lm:-1])
            if "xt" not in res.keys():
                raise Exception(res)
            res["xt"] = res["xt"][0].lower()
            if (len(same) == 0) or (res["xt"] == same[-1]["xt"]):
                same += [res]
            else:
                break
        for t in same:
            if "dn" in t.keys() and ((len(dns) == 0) or (t["dn"][0] != dns[-1])):
                dns += t["dn"]
            if "tr" in t.keys():
                trs += t["tr"]
        dn = "||".join(dns)
        joined = {"xt": same[-1]["xt"], "dn": dn, "tr": list(set(trs))}
        if joined["xt"] not in seen:
            sys.stdout.write(build_magnet(joined)+'\n')
            seen.append(joined["xt"])
        if res["xt"] not in seen:
            sys.stdout.write(build_magnet(res)+'\n')
            seen.append(res["xt"])
        if (i % 1000) == 0:
            gc.collect()
