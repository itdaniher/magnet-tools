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


trs = [x for x in open('trz').read().split('\n') if x]
with open(sys.argv[1], 'r+') as f:
    data = mmap.mmap(f.fileno(), 0, prot=mmap.PROT_READ)
    i = 0
    while True:
        i += 1
        res = {}
        line = data.readline()
        try:
            line = line.decode('utf-8')
            if line.strip() == '':
                break
            ih, dn = line.split(' ', maxsplit=1)
            res["xt"] = "urn:btih:"+ih.lower()
            res["dn"] = dn
            res['tr'] = trs
            sys.stdout.write(build_magnet(res)+'\n')
            if (i % 1000) == 0:
                gc.collect()
        except:
            pass
