from whoosh.fields import Schema, TEXT, ID, STORED

magnet = Schema(title=TEXT(stored=True), content=STORED, infohash=ID(stored=True))

import os.path
from whoosh.index import create_in

if not os.path.exists("index"):
    os.mkdir("index")

ix = create_in("index", magnet)

writer = ix.writer(limitmb=192)

import sys, mmap, urllib.parse

with open(sys.argv[1], 'r+') as f:
    data = mmap.mmap(f.fileno(), 0, prot=mmap.PROT_READ)
    i = 0
    m = 'magnet:?'
    lm = len(m)
    while True:
        i += 1
        line = data.readline()
        res = urllib.parse.parse_qs(line[lm:-1].decode('utf-8'))
        if i % 1000 == 0:
            print(i)
        try:
            writer.add_document(title=res["dn"][0] + " " + res["xt"][0], content=line.strip().decode('utf-8'), infohash=res["xt"][0])
        except:
            break
writer.commit()
