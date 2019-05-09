import requests, re, json, io

url_patt="https://www.genealogy.math.ndsu.nodak.edu/id.php?id=%d&fChrono=1"

NOETHER = 6967

patt_student = re.compile(
    "<[\s]*tr[\s]*[^>]*>" + "[\s]*" + "<[\s]*td[^>]*>" + "[\s]*" + \
    '<[\s]*a[\s]*href[\s]*=[\s]*"id.php\?id=([0-9]+)"[^>]*>' + "[\s]*" + \
    "([^<]+)" + "[\s]*" + "<[\s]*/a[^>]*>" + "<[\s]*/td[^>]*>" + "[\s]*" + \
    "<[\s]*td[\s]*[^>]*>" + "[\s]*" + "[^>]+" + "[\s]*" + "<[\s]*/td[^>]*>" + "[\s]*" + \
    "<[\s]*td[\s]*[^>]*>" + "[\s]*" + "([0-9]*)" + "[\s]*" + \
    "<[\s]*/td[^>]*>" + "[\s]*" + "<[\s]*td[\s]*[^>]*>" + "[\s]*" + "([0-9]*)"
)

data = { 6967 : (1, '6967', 'Noether, Emmy', '1907', '1405') }
edges = []

enc = json.JSONEncoder(ensure_ascii=False)
out = open("output.txt", 'a')

def loop(ident, lvl):
    lvl += 1
    #print("lvl=", lvl)
    res = requests.get(url_patt % ident)
    html = res.content.decode()
    mm = re.findall(patt_student, html)
    for m in mm:
        if m[0] not in data:
            data[m[0]] = tuple([lvl] + list(m))
            #print(data[m[0]])
        out.write(m[1] + "\n")
        edges.append((str(ident), m[0]))
        print(len(data), len(edges))
        io.open('data.json', 'w', encoding='utf8').write(enc.encode(data))
        open("edges.json", 'w').write(enc.encode(edges))
    for m in mm:
        loop(int(m[0]), lvl)
    lvl -= 1

loop(NOETHER, 1)
