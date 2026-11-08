#!/usr/bin/env python3
"""derive_links.py: derive Context & Conditions of Use Builder links from a CRA Manual Builder file.

What a manual already says, read mechanically:
  R1  protocol rows (2.1.4)          -> logical interfaces, and FC.pi (the interfaces a function's protocols use)
  R2  function CU list (3.3)         -> FC.cu
  R3  CU "affects" field             -> CU.on (IDs named there; "Product boundary" -> the product)
  R4  SP "component" field           -> SP.on (ID named there; "Product: ..." -> the product)
  R5  a function's CUs' targets      -> FC.cc / FC.cp / FC.cz (a condition on X for function F means F involves X)
  R6  CR rows                        -> RI.fc / RI.cu
  R7  titles named in text           -> suggestions: FC.pc, FC.cc, FC.cp, CC.via, CP.via, CZ.members
  R8  path                           -> CP, CC, PI, PC order of what the function involves
  R9  processor and software         -> take part in every function (FC.pc)
  R10 a function with one interface  -> its context components are reached through it (CC.via)
  R11 zones holding a function's CC/CP -> FC.cz
  R12 as R10, for persons            -> CP.via
Measured by score_links.py; on the working group's Engineering PC example (held out): 76% precision, 67% recall (8 Nov 2026).
Everything R7 proposes is marked "suggested"; anything no rule reaches is listed as a gap for a person.
Cairn Viktor for the Value Chain Risk Institute, 2026-11-08. CC BY 4.0."""
import re

P = "PRODUCT"
STOP = {"the", "and", "with", "for", "from", "used", "uses", "a", "an", "of", "to", "or", "in", "on", "by", "via", "by default", "x1", "only"}

def ids(prefix, n): return [f"{prefix}{i:02d}" for i in range(1, n + 1)]
def named(s, kinds): return re.findall(r"\b(?:%s)\d\d\b" % "|".join(kinds), s or "")

def keywords(title):
    """Distinctive words of an element title, for spotting it in prose."""
    t = re.sub(r"\(.*?\)", " ", title.lower())
    return [w for w in re.findall(r"[a-z0-9][a-z0-9\-\.]+", t) if w not in STOP and len(w) > 2]

def mentions(text, title):
    kw = keywords(title)
    if not kw: return False
    text = (text or "").lower()
    hits = sum(1 for w in kw if re.search(r"\b%s\b" % re.escape(w), text))
    return hits >= max(1, min(2, len(kw)))  # one distinctive word for short titles, two for longer ones

def derive(m):
    E = {k: list(zip(ids(k, len(m[src])), m[src])) for k, src in
         (("PC", "pc"), ("PI", "pi"), ("SP", "sp"), ("CC", "cc"), ("CP", "cp"), ("CZ", "cz"), ("CU", "cu"), ("FC", "fc"))}
    how = {}  # (kind, id, field) -> {target: rule}
    def put(kind, i, field, target, rule):
        how.setdefault((kind, i, field), {}).setdefault(target, rule)

    # R1 logical interfaces and FC.pi
    LI = []
    for row in m["pp"]:
        pis, fcs = named(row["pi"], ["PI"]), named(row["fc"], ["FC"])
        LI.append({"proto": row["proto"], "url": "", "pi": pis[0] if pis else "", "port": row["port"], "dir": "both", "enabled": row["enabled"], "fc": fcs})
        for f in fcs:
            for p in pis: put("FC", f, "pi", p, "R1")
    # R3 / R4
    for i, cu in E["CU"]:
        tg = named(cu["affected"], ["CC", "CP", "CZ", "PC", "PI"]) + ([P] if re.search(r"product boundary", cu["affected"], re.I) else [])
        for t in tg: put("CU", i, "on", t, "R3")
    for i, sp in E["SP"]:
        tg = named(sp["comp"], ["PC", "PI"]) or ([P] if re.match(r"\s*product\b", sp["comp"], re.I) else [])
        for t in tg: put("SP", i, "on", t, "R4")
    # R2 / R5
    for i, f in E["FC"]:
        for u in named(f["cus"], ["CU"]):
            put("FC", i, "cu", u, "R2")
            for t in how.get(("CU", u, "on"), {}):
                k = t[:2]
                if k in ("CC", "CP", "CZ"): put("FC", i, k.lower(), t, "R5")
    # R7 suggestions from prose
    for i, f in E["FC"]:
        text = " ".join([f["title"], f["desc"], f.get("rfu", "")])
        for k in ("PC", "CC", "CP"):
            for j, x in E[k]:
                if mentions(text, x["title"]): put("FC", i, k.lower(), j, "R7")
    for k in ("CC", "CP"):
        for i, x in E[k]:
            for j, pi in E["PI"]:
                if mentions(x["desc"] + " " + x["title"], pi["title"]): put(k, i, "via", j, "R7")
    for i, z in E["CZ"]:
        for k in ("CC", "CP"):
            for j, x in E[k]:
                if mentions(z["desc"] + " " + z["title"], x["title"]): put("CZ", i, "members", j, "R7")
    # a zone also holds what a CU places in it together with that zone (CU affects "CZ01 ..., CC01 ...")
    for i, cu in E["CU"]:
        tg = list(how.get(("CU", i, "on"), {}))
        for z in [t for t in tg if t.startswith("CZ")]:
            for t in tg:
                if t[:2] in ("CC", "CP"): put("CZ", z, "members", t, "R3")
    get = lambda kind, i, field: list(how.get((kind, i, field), {}))
    # R9 every function runs on the processor and the software
    core = [j for j, x in E["PC"] if re.search(r"\b(cpu|soc|processor|firmware|operating system|application|software)\b", x["title"], re.I)]
    for i, f in E["FC"]:
        for j in core: put("FC", i, "pc", j, "R9")
    # R10 / R12 a function with one interface reaches its context through it
    for i, f in E["FC"]:
        pis = get("FC", i, "pi")
        if len(pis) == 1:
            for t in get("FC", i, "cc"): put("CC", t, "via", pis[0], "R10")
            for t in get("FC", i, "cp"): put("CP", t, "via", pis[0], "R12")
    # R11 a function sits in the zones that hold what it involves
    for i, f in E["FC"]:
        mine = set(get("FC", i, "cc") + get("FC", i, "cp"))
        for z, _ in E["CZ"]:
            if mine & set(get("CZ", z, "members")): put("FC", i, "cz", z, "R11")
    return E, LI, how, get

def to_context(m, overrides=None, short_model=None):
    """Context JSON from a manual. overrides: {(kind,id,field): [targets]} written by a person where derivation has a gap."""
    E, LI, how, get = derive(m); overrides = overrides or {}
    def val(kind, i, field):
        return list(overrides[(kind, i, field)]) if (kind, i, field) in overrides else get(kind, i, field)
    c = {"product": {"name": m["product"]["name"], "model": short_model or m["product"]["tmv"], "version": "illustrative example v0.1, 8 Nov 2026, template v0.39", "family": ""}, "layout": {}, "fig": {}}
    c["PC"] = [{"id": i, "title": x["title"], "desc": ""} for i, x in E["PC"]]
    c["PI"] = [{"id": i, "title": x["title"], "desc": ""} for i, x in E["PI"]]
    c["LI"] = LI
    refs = lambda s: [x.strip() for x in (s or "").split(",") if x.strip()]
    c["SP"] = [{"id": i, "annex": refs(x["refs"]), "title": x["title"], "desc": x["desc"], "on": val("SP", i, "on")} for i, x in E["SP"]]
    c["CC"] = [{"id": i, "title": x["title"], "desc": x["desc"], "via": val("CC", i, "via")} for i, x in E["CC"]]
    c["CP"] = [{"id": i, "title": x["title"], "desc": x["desc"], "skill": x["skill"], "via": val("CP", i, "via")} for i, x in E["CP"]]
    c["CZ"] = [{"id": i, "title": x["title"], "desc": x["desc"], "type": x["type"], "access": x["access"], "members": val("CZ", i, "members")} for i, x in E["CZ"]]
    c["CU"] = [{"id": i, "annex": refs(x["refs"]), "title": x["title"], "desc": x["desc"], "on": val("CU", i, "on")} for i, x in E["CU"]]
    c["FC"] = []
    for i, x in E["FC"]:
        f = {"id": i, "title": x["title"], "desc": x["desc"], "rfu": x["rfu"], "core": x["kind"], "use": "intended"}
        for k in ("pc", "pi", "cc", "cp", "cz", "cu"): f[k] = val("FC", i, k)
        f["path"] = val("FC", i, "path") if ("FC", i, "path") in overrides else f["cp"] + f["cc"] + f["pi"] + f["pc"]  # R8
        c["FC"].append(f)
    c["RI"] = [{"id": i, "title": x["title"], "desc": x["desc"], "damage": x["risk"], "fc": named(x["fc"], ["FC"]), "cu": named(x["cu"], ["CU"]), "path": []}
               for i, x in zip(ids("CR", len(m["ri"])), m["ri"])]  # R6
    gaps = []
    for f in c["FC"]:
        for k in ("pc", "pi"):
            if not f[k]: gaps.append(f"{f['id']} {f['title']}: no {k.upper()} derivable")
    for k, fld in (("CC", "via"), ("CP", "via")):
        for x in c[k]:
            if not x[fld] and (k, x["id"], fld) not in overrides: gaps.append(f"{x['id']} {x['title']}: {fld} not derivable")
    placed = {t for z in c["CZ"] for t in z["members"]}
    for k in ("CC", "CP"):
        for x in c[k]:
            if x["id"] not in placed: gaps.append(f"{x['id']} {x['title']}: in no zone")
    return c, how, gaps
