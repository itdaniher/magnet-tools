import sys
from whoosh.index import open_dir
from whoosh.qparser import QueryParser
import urllib.parse

ix = open_dir("index")

results = None
searcher = ix.searcher()
parser = QueryParser("title", ix.schema)
query = parser.parse(" ".join(sys.argv[1:]))
print(query)
results = searcher.search(query, limit=None)
print(results)
for result in results:
    print(result['title'], '\n\t', urllib.parse.unquote(result['content']))
