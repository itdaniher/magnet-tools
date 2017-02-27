import re, mmap, sys

with open(sys.argv[1], 'r+') as f:
    data = mmap.mmap(f.fileno(), 0)
    magnet_matcher = re.compile(b'\[\".+(magnet:\?xt=urn:[A-Za-z0-9]+:[A-Za-z0-9]+)(\&[A-Za-z0-9%./&=]+)')
    i = 0
    for match in magnet_matcher.finditer(data):
        print(match.groups()[0])
