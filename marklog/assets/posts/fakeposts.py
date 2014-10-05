import sys

# Python 2.x vs. 3.x
try:
    from urllib.request import urlopen
except ImportError:
    from urllib2 import urlopen 

import random

# tybg for restful-like apis
md_url = r'http://jaspervdj.be/lorem-markdownum/markdown.txt'
text_url = r'http://loripsum.net/api/plaintext/short/1'
image_url = r'http://hhhhold.com/l'

try:
    i = int(sys.argv[1])
except IndexError:
    i = 1

for j in range(i):
    md = str(urlopen(md_url).read())

    meta = {
        "title": str(urlopen(text_url).read())[57:].split(".")[0],
        "date": "2014-" + str(random.randint(1, 12)) + "-" + str(random.randint(1, 28)),
        "previewtext": str(urlopen(text_url).read())[57:].strip(),
        "previewimage": image_url if random.choice([True, False]) else None,
    }

    f = open("fakepost_" + str(random.randint(1000, 9999)) + '.md', 'w')

    for k, v in meta.items():
        if v is not None:
            f.write(k + ": " + v + "\n")

    f.write('\n' + md)
    f.close()
