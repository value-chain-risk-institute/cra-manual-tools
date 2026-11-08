#!/usr/bin/env python3
"""Attach the context-builder diagrams to each example manual (as embedded SVG, so the JSON stays portable) and print the PDFs.
Rendering goes through a scratch copy of the CRA Manual Builder; the site source is never modified."""
import base64, html, json, os, re, subprocess, sys, tempfile
EX = os.path.dirname(os.path.abspath(__file__))
SITE = os.path.join(EX, "..", "cra-manual-builder", "index.html")  # the Manual Builder in this repository
CHROME = "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"
TMP = sys.argv[1]
def uri(p): return "data:image/svg+xml;base64," + base64.b64encode(open(p, "rb").read()).decode()
def chrome(*args): return subprocess.run([CHROME, "--headless=new", "--disable-gpu", f"--user-data-dir={tempfile.mkdtemp(dir=TMP)}", *args], capture_output=True, text=True, timeout=180).stdout
base = open(SITE).read()
for slug in ("openwrt-one", "keepassxc", "home-assistant-green"):
    jp = os.path.join(EX, f"{slug}.cybermanual.json"); m = json.load(open(jp)); d = os.path.join(EX, "diagrams")
    m["dia"].update(product=uri(f"{d}/{slug}-product.svg"), sp=uri(f"{d}/{slug}-sp.svg"), context=uri(f"{d}/{slug}-context.svg"))
    for n, f in enumerate(m["fc"], 1): f["dia"] = uri(f"{d}/{slug}-fc-FC{n:02d}.svg")
    json.dump(m, open(jp, "w"), indent=2, ensure_ascii=False)
    i = base.rfind("</body>"); page = os.path.join(TMP, f"{slug}-m.html")
    open(page, "w").write(base[:i] + "<script>loadJson(" + json.dumps(m).replace("</", "<\\/") + ");</script>" + base[i:])
    dom = chrome("--window-size=1600,1200", "--virtual-time-budget=6000", "--dump-dom", "file://" + page)
    styles = "".join(re.findall(r"<style[^>]*>.*?</style>", dom, re.S))
    a = dom.index('<article class="doc" id="doc">'); doc = dom[a:dom.index("</article>", a) + len("</article>")]
    pp = os.path.join(TMP, f"{slug}-print.html")
    open(pp, "w").write(f'<!doctype html><html><head><meta charset="utf-8"><title>{html.escape(m["product"]["name"])} example manual</title>{styles}'
        '<style>html,body{background:#fff!important;display:block!important;height:auto!important;overflow:visible!important}'
        '.doc{box-shadow:none!important;max-width:none!important;margin:0!important}.doc img.dia{max-width:100%!important}@page{margin:12mm}</style></head>'
        f'<body>{doc}</body></html>')
    pdf = os.path.join(EX, f"{slug}-example-manual-DRAFT.pdf")
    chrome("--virtual-time-budget=4000", "--no-pdf-header-footer", f"--print-to-pdf={pdf}", "file://" + pp)
    print(slug, "diagrams:", 3 + len(m["fc"]), "| imgs in doc:", doc.count('class="dia"'))
