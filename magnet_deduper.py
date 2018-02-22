import sys, os, mmap, gc, re, urllib.parse

m = 'magnet:?'
lm = len(m)

def build_magnet(res):
    if "dn" in res.keys():
        magnet = m+urllib.parse.urlencode({"xt": res["xt"], "dn": res['dn']})
    else:
        magnet = m+urllib.parse.urlencode({"xt": res["xt"]})
    magnet = magnet.replace("urn%3Abtih%3A", "urn:btih:")
    if 'tr' in res.keys():
        for tr in res['tr']:
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
                line_data = data.readline()
                try:
                    line = line_data.decode('utf-8')
                except:
                    break
            else:
                line = lastline
                lastline = None
            if line.strip() == '':
                break
            if ' ' in line:
                xt, dn = line.split(' ', 1)
            else:
                print("ABADIDEA", line)
            xt = xt.lower()
            if (len(same) == 0) or (xt == same[-1][0]):
                same += [(xt,dn)]
            else:
                lastline = line
                break
        if len(same) == 0:
            break
        dns = [x[1].strip(' \n') for x in same]
        dn = "||".join(list(set(dns)))
        trs = common_trackers
        joined = {"xt": same[-1][0], "dn": dn, "tr": trs[0:4]}
        if joined["xt"] not in seen:
            sys.stdout.write(build_magnet(joined)+'\n')
            sys.stdout.flush()
        if (i % 1000) == 0:
            gc.collect()

#open('trs', 'w').write('\n'.join(['\t'.join(reversed([str(y) for y in x])) for x in trz.items()]))
