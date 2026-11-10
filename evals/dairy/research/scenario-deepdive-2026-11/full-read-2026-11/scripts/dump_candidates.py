"""Write candidates.json in its hand-kept layout: header kept verbatim, one claim per line."""
import json, sys
path, orig = sys.argv[1], sys.argv[2]
d = json.load(open(path))
head = open(orig).read().split('  "candidates": [')[0]
j = lambda v: json.dumps(v, ensure_ascii=False)
blocks = []
for c in d["candidates"]:
    l1 = ", ".join(f'{j(k)}: {j(c[k])}' for k in ("id", "family", "title", "rec"))
    l2 = ", ".join(f'{j(k)}: {j(c[k])}' for k in ("type", "hen", "category", "arity", "prompted", "root", "keys_on"))
    cl = ",\n".join("       " + j(x).replace('", "', '", "') for x in c["claims"])
    blocks.append("    {" + l1 + ",\n     " + l2 + ",\n" +
        "".join(f'     {j(k)}: {j(c[k])},\n' for k in ("tension", "welfare", "profit")) +
        '     "claims": [\n' + cl + "\n     ]}")
open(path, "w").write(head + '  "candidates": [\n' + ",\n".join(blocks) + "\n  ]\n}\n")
