#!/usr/bin/env python3
"""Score derive_links.py against hand-written links (build-context.py LINKS). Prints precision and recall per field."""
import json, os, sys
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
import derive_links as D
src = open(os.path.join(HERE, "build-context.py")).read(); src = src[:src.index("for s in LINKS")]
ns = {"__file__": os.path.join(HERE, "build-context.py")}; exec(src, ns); LINKS = ns["LINKS"]

def hand_links(L):
    h = {}
    for i, v in L["cc_via"].items(): h[("CC", i, "via")] = v
    for i, v in L["cp_via"].items(): h[("CP", i, "via")] = v
    for i, v in L["cz_members"].items(): h[("CZ", i, "members")] = v
    for n, v in enumerate(L["sp_on"]): h[("SP", f"SP{n+1:02d}", "on")] = v
    for n, v in enumerate(L["cu_on"]): h[("CU", f"CU{n+1:02d}", "on")] = v
    for n, f in enumerate(L["fc"]):
        for k in ("pc", "pi", "cc", "cp", "cz"): h[("FC", f"FC{n+1:02d}", k)] = f[k]
    return h

tot = [0, 0, 0]; field = {}
for slug, L in LINKS.items():
    m = json.load(open(os.path.join(HERE, f"{slug}.cybermanual.json"))); _, _, how, get = D.derive(m)
    for key, hv in hand_links(L).items():
        dv, hv = set(get(*key)), set(hv); f = key[0] + "." + key[2]; b = field.setdefault(f, [0, 0, 0])
        for j, n in enumerate((len(dv & hv), len(dv - hv), len(hv - dv))): b[j] += n; tot[j] += n
for f, (h, e, mi) in sorted(field.items()):
    print(f"{f:12s} found {h:3d}  extra {e:3d}  missed {mi:3d}  recall {h/(h+mi) if h+mi else 1:.0%}")
h, e, mi = tot
print(f"ALL          found {h}  extra {e}  missed {mi}  precision {h/(h+e):.0%}  recall {h/(h+mi):.0%}")

# held out: the working group's Engineering PC example, linked by hand in the context builder
m = json.load(open(os.path.join(HERE, "heldout-engineering-pc.cybermanual.json"))); hand = json.load(open(os.path.join(HERE, "heldout-engineering-pc.context-HAND.json")))
_, _, how, get = D.derive(m); t = [0, 0, 0]; fld = {}
def cmp(key, hv):
    dv, hv = set(get(*key)), set(hv); f = key[0] + "." + key[2]; b = fld.setdefault(f, [0, 0, 0])
    for j, n in enumerate((len(dv & hv), len(dv - hv), len(hv - dv))): b[j] += n; t[j] += n
for x in hand["CC"]: cmp(("CC", x["id"], "via"), x.get("via", []))
for x in hand["CP"]: cmp(("CP", x["id"], "via"), x.get("via", []))
for x in hand["CZ"]: cmp(("CZ", x["id"], "members"), x.get("members", []))
for x in hand["SP"]: cmp(("SP", x["id"], "on"), x.get("on", []))
for x in hand["CU"]: cmp(("CU", x["id"], "on"), x.get("on", []))
for x in hand["FC"]:
    for k in ("pc", "pi", "cc", "cp", "cz"): cmp(("FC", x["id"], k), x.get(k, []))
print("\nHELD OUT, Engineering PC (working group's own links):")
for f, (h, e, mi) in sorted(fld.items()): print(f"{f:12s} found {h:3d}  extra {e:3d}  missed {mi:3d}")
h, e, mi = t; print(f"ALL          found {h}  extra {e}  missed {mi}  precision {h/(h+e):.0%}  recall {h/(h+mi):.0%}")
