#!/usr/bin/env python3
"""Turn each example manual into a Context & Conditions of Use Builder file (vcri context JSON) by adding the links
the diagrams need: which components and interfaces each function uses, who and what sits in which zone, where each
security property and condition of use applies. The links are modelling choices made from the manual text, not new facts.
Cairn Viktor for the Value Chain Risk Institute, 2026-11-08."""
import json, os, re
HERE = os.path.dirname(os.path.abspath(__file__))
P = "PRODUCT"
def ids(prefix, n): return [f"{prefix}{i:02d}" for i in range(1, n + 1)]

LINKS = {
 "openwrt-one": {
  "cc_via": {"CC01": ["PI01"], "CC02": ["PI02"], "CC03": ["PI03"], "CC04": ["PI02"], "CC05": ["PI01"], "CC06": ["PI04"], "CC07": ["PI05", "PI02"]},
  "cp_via": {"CP01": ["PI09"], "CP02": [], "CP03": ["PI08", "PI09", "PI05"]},
  "cz_members": {"CZ01": ["CC02", "CC03", "CC04", "CP01", "CP02"], "CZ02": ["CC01", "CC05"], "CZ03": ["CC06", "CC07", "CP03"]},
  "sp_on": [["PC05"], [P], ["PC06"], ["PC06"]],
  "cu_on": [["CP01"], ["CC01"], [P], ["CC03"], ["CZ02"], ["CZ01"], ["CZ03"], ["CC05"], ["PC05"]],
  "fc": [
   dict(pc=["PC01", "PC06"], pi=["PI01", "PI02", "PI03"], cc=["CC01", "CC02", "CC03"], cp=["CP02"], cz=["CZ01", "CZ02"], path=["CC01", "PI01", "PC01", "PI02", "CC02"]),
   dict(pc=["PC02", "PC06"], pi=["PI03"], cc=["CC03"], cp=["CP02"], cz=["CZ01"], path=["CC03", "PI03", "PC02"]),
   dict(pc=["PC06"], pi=["PI02"], cc=["CC04"], cp=["CP01"], cz=["CZ01"], path=["CP01", "CC04", "PI02", "PC06"]),
   dict(pc=["PC04", "PC05"], pi=["PI02", "PI04", "PI05", "PI08", "PI09"], cc=["CC06", "CC07"], cp=["CP03"], cz=["CZ03"], path=["CP03", "CC06", "PI04", "PC05", "PC04"]),
   dict(pc=["PC04", "PC06"], pi=["PI01", "PI02", "PI04"], cc=["CC05", "CC04", "CC06"], cp=["CP01"], cz=["CZ01", "CZ02"], path=["CC05", "PI01", "PC06", "PC04"])]},
 "keepassxc": {
  "cc_via": {"CC01": ["PI01", "PI02"], "CC02": ["PI02"], "CC03": ["PI01"], "CC04": ["PI03"], "CC05": [], "CC06": ["PI01"]},
  "cp_via": {"CP01": ["PI01"], "CP02": []},
  "cz_members": {"CZ01": ["CC01", "CC03", "CC04", "CC06", "CP01"], "CZ02": ["CC02"]},
  "sp_on": [[P], [P], ["PC01"], ["PC01"], [P], [P]],
  "cu_on": [["CP01"], ["CC02"], ["CC01"], ["CC03"], ["CP01"], ["CZ01"], ["CZ02"], ["CC05"]],
  "fc": [
   dict(pc=["PC01", "PC02"], pi=["PI01", "PI02"], cc=["CC01", "CC02"], cp=["CP01"], cz=["CZ01", "CZ02"], path=["CP01", "PI01", "PC01", "PI02", "CC02"]),
   dict(pc=["PC01", "PC03"], pi=["PI01"], cc=["CC03"], cp=["CP01"], cz=["CZ01"], path=["CC03", "PC03", "PC01"]),
   dict(pc=["PC01"], pi=["PI01"], cc=["CC06"], cp=["CP01"], cz=["CZ01"], path=["PC01", "PI01", "CC06"]),
   dict(pc=["PC01"], pi=["PI01", "PI03"], cc=["CC01", "CC04"], cp=["CP01"], cz=["CZ01"], path=["CP01", "PI01", "PC01", "PI03", "CC04"]),
   dict(pc=["PC01"], pi=["PI02"], cc=["CC02"], cp=["CP01"], cz=["CZ02"], path=["PC01", "PI02", "CC02"]),
   dict(pc=["PC01", "PC02", "PC03"], pi=["PI02"], cc=["CC05", "CC01"], cp=["CP01"], cz=["CZ01"], path=["CC05", "CC01", "PI02", "PC01"])]},
 "home-assistant-green": {
  "cc_via": {"CC01": ["PI01"], "CC02": [], "CC03": ["PI02"], "CC04": ["PI01"], "CC05": [], "CC06": [], "CC07": ["PI03", "PI02"]},
  "cp_via": {"CP01": [], "CP02": []},
  "cz_members": {"CZ01": ["CC01", "CC02", "CC03", "CC04", "CP01", "CP02"], "CZ02": ["CC05", "CC06"], "CZ03": ["CC07"]},
  "sp_on": [["PC04"], [P], ["PC04"], ["PC03"]],
  "cu_on": [["CP01"], ["CC01"], ["CP01"], ["CC03"], ["CC06"], ["CZ03"], ["PC04"], ["CC05"]],
  "fc": [
   dict(pc=["PC01", "PC04"], pi=["PI01", "PI02"], cc=["CC01", "CC02", "CC03"], cp=["CP02"], cz=["CZ01"], path=["CC02", "CC03", "PI02", "PC04"]),
   dict(pc=["PC04"], pi=["PI01"], cc=["CC01", "CC04"], cp=["CP01"], cz=["CZ01"], path=["CP01", "CC04", "CC01", "PI01", "PC04"]),
   dict(pc=["PC03", "PC04"], pi=["PI01"], cc=["CC06"], cp=["CP01"], cz=["CZ02"], path=["PC03", "PC04", "PI01", "CC06"]),
   dict(pc=["PC04"], pi=["PI02", "PI03"], cc=["CC07"], cp=["CP01"], cz=["CZ03"], path=["CP01", "CC07", "PI02", "PC04"]),
   dict(pc=["PC03", "PC04"], pi=["PI01"], cc=["CC05", "CC01"], cp=["CP01"], cz=["CZ01", "CZ02"], path=["CC05", "CC01", "PI01", "PC04"]),
   dict(pc=["PC03", "PC04"], pi=["PI01", "PI04"], cc=["CC05"], cp=["CP01"], cz=["CZ02"], path=["CC05", "PI01", "PC03"])]},
}

SHORT_MODEL = {"openwrt-one": "OpenWrt 25.12.6", "keepassxc": "2.8.0", "home-assistant-green": "NC-GREEN-9703"}
def short(proto):
    """Diagram label: drop the parenthetical, keep it under about 26 characters at a word boundary."""
    t = re.sub(r"\s*\(.*?\)", "", proto).strip()
    if len(t) <= 26: return t
    return t[:26].rsplit(" ", 1)[0] + "..."
def refs(s): return [x.strip() for x in (s or "").split(",") if x.strip()]
def firstid(s, kind): m = re.match(rf"\s*({kind}\d\d)", s or ""); return m.group(1) if m else ""

def convert(slug):
    m = json.load(open(os.path.join(HERE, f"{slug}.cybermanual.json"))); L = LINKS[slug]
    c = {"product": {"name": m["product"]["name"], "model": SHORT_MODEL[slug], "version": "illustrative example v0.1, 8 Nov 2026, template v0.39", "family": ""},
         "layout": {}, "fig": {}}
    c["PC"] = [{"id": i, "title": x["title"], "desc": ""} for i, x in zip(ids("PC", len(m["pc"])), m["pc"])]
    c["PI"] = [{"id": i, "title": x["title"], "desc": ""} for i, x in zip(ids("PI", len(m["pi"])), m["pi"])]
    c["LI"] = [{"proto": short(x["proto"]), "url": "", "pi": firstid(x["pi"], "PI"), "port": x["port"], "dir": "both", "enabled": x["enabled"],
                "fc": re.findall(r"FC\d\d", x["fc"])} for x in m["pp"]]
    c["SP"] = [{"id": i, "annex": refs(x["refs"]), "title": x["title"], "desc": x["desc"], "on": on} for i, x, on in zip(ids("SP", len(m["sp"])), m["sp"], L["sp_on"])]
    c["CC"] = [{"id": i, "title": x["title"], "desc": x["desc"], "via": L["cc_via"][i]} for i, x in zip(ids("CC", len(m["cc"])), m["cc"])]
    c["CP"] = [{"id": i, "title": x["title"], "desc": x["desc"], "skill": x["skill"], "via": L["cp_via"][i]} for i, x in zip(ids("CP", len(m["cp"])), m["cp"])]
    c["CZ"] = [{"id": i, "title": x["title"], "desc": x["desc"], "type": x["type"], "access": x["access"], "members": L["cz_members"][i]} for i, x in zip(ids("CZ", len(m["cz"])), m["cz"])]
    c["CU"] = [{"id": i, "annex": refs(x["refs"]), "title": x["title"], "desc": x["desc"], "on": on} for i, x, on in zip(ids("CU", len(m["cu"])), m["cu"], L["cu_on"])]
    c["FC"] = [dict({"id": i, "title": x["title"], "desc": x["desc"], "rfu": x["rfu"], "core": x["kind"], "use": "intended", "cu": re.findall(r"CU\d\d", x["cus"])}, **lk)
               for i, x, lk in zip(ids("FC", len(m["fc"])), m["fc"], L["fc"])]
    c["RI"] = [{"id": i, "title": x["title"], "desc": x["desc"], "damage": x["risk"], "fc": re.findall(r"FC\d\d", x["fc"]), "cu": re.findall(r"CU\d\d", x["cu"]), "path": []}
               for i, x in zip(ids("CR", len(m["ri"])), m["ri"])]
    # every id a link names must exist
    known = {P} | {x["id"] for k in ("PC", "PI", "CC", "CP", "CZ", "CU", "FC") for x in c[k]}
    used = [v for k in ("SP", "CU") for x in c[k] for v in x["on"]] + [v for x in c["FC"] for k in ("pc", "pi", "cc", "cp", "cz", "path", "cu") for v in x[k]] \
         + [v for x in c["CC"] + c["CP"] for v in x["via"]] + [v for x in c["CZ"] for v in x["members"]] + [v for x in c["RI"] for v in x["fc"] + x["cu"]]
    bad = sorted(set(v for v in used if v not in known)); assert not bad, (slug, bad)
    out = os.path.join(HERE, f"{slug}.context.json"); json.dump(c, open(out, "w"), indent=2, ensure_ascii=False); return out

for s in LINKS: print(convert(s))
