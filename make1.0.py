#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
InvoiceText v1.0 - lightweight text-based invoicing tool
(c) 2025 Carsten Hilbert - MIT License
--------------------------------------------------------

EN:
InvoiceText converts plain text order files into HTML invoices, offers or delivery notes.
It works fully offline, requires no database, and can be edited with any text editor.
Perfect for craftsmen and freelancers who prefer simplicity and transparency.

DE:
InvoiceText wandelt einfache Textdateien in HTML-Rechnungen, Angebote oder Lieferscheine um.
Es arbeitet komplett offline, benoetigt keine Datenbank und kann in jedem Editor bearbeitet werden.
Ideal fuer Handwerker und Selbststaendige, die Uebersicht und Kontrolle schaetzen.
"""

#!/usr/bin/env python3
import sys, datetime, re, pathlib

root = pathlib.Path(__file__).parent
outdir = root / "out"
outdir.mkdir(exist_ok=True)
today = datetime.date.today().isoformat()

inv_file = root / "inv.txt"
inv_file.touch()
inv_lines = inv_file.read_text().splitlines()

# =========================================================
# 1. CFG laden (kompaktes flaches Schema)
# =========================================================
def read_cfg_flat(path):
    """Liest einfache Key=Value-Struktur in flaches Dict."""
    cfg = {}
    for line in pathlib.Path(path).read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if not line or line.startswith("#"):
            continue
        if "=" in line:
            k, v = [x.strip() for x in line.split("=", 1)]
            cfg[k.lower()] = v
    return cfg


# =========================================================
# 2. Template-Füller (flach)
# =========================================================
def fill_html_placeholders(template_html, data):
    """Ersetzt {{...}}-Platzhalter flach mit Werten aus dict."""
    keys = set(re.findall(r"{{\s*([^{}]+?)\s*}}", template_html))
    for k in keys:
        val = str(data[k]) if k in data else f"{{{{{k}}}}}"
        template_html = re.sub(r"{{\s*" + re.escape(k) + r"\s*}}", val, template_html)
    return template_html


# =========================================================
# 3. Hilfsfunktionen
# =========================================================
def split_orders(txt):
    return [b.strip().splitlines() for b in txt.split("\n\n") if b.strip()]

def save_orders(blocks, path):
    with open(path, "w") as f:
        f.write("\n\n".join("\n".join(b) for b in blocks) + "\n")

def find_order(id, blocks):
    for b in blocks:
        if b and b[0].strip() == id:
            return b
    return None

def shortname(typ, key, desc, num=None):
    name = re.sub(r"[^a-z0-9_]", "", key.lower())
    shortdesc = re.sub(r"[^a-z0-9]", "", desc.lower())[:8]
    prefix = f"{num}_" if num else ""
    return f"{prefix}{typ}_{name}_{shortdesc}.html"

def base_name(typ, key, desc):
    name = re.sub(r"[^a-z0-9_]", "", key.lower())
    shortdesc = re.sub(r"[^a-z0-9]", "", desc.lower())[:8]
    return f"{typ}_{name}_{shortdesc}.html"

def files_for_base(base):
    candidates = []
    pure = outdir / base
    if pure.exists():
        candidates.append(pure)
    patt = re.compile(rf"^\d+_{re.escape(base)}$")
    for p in outdir.iterdir():
        if p.is_file() and patt.match(p.name):
            candidates.append(p)
    return candidates


# =========================================================
# 4. Duplikatsprüfung
# =========================================================
def invoice_exists_in_invtxt(order_id, cust_key, title_short, gross_val, inv_lines):
    patt = re.compile(
        rf"^\d+\s+_{re.escape(order_id)}\s+{re.escape(cust_key)}\s+{re.escape(title_short)}\s+{gross_val:.2f}\b"
    )
    return any(patt.match(l) for l in inv_lines)


# =========================================================
# 5. Hauptlogik
# =========================================================
cfg = read_cfg_flat(root / "cfg.txt")
tpl = (root / "inv.html").read_text(encoding="utf-8")
txt_ord = (root / "ord.txt").read_text().strip()
blocks = split_orders(txt_ord)
inv_lines = inv_file.read_text().splitlines()

if len(sys.argv) < 2:
    print("Verwendung: make25.py <Befehl> (z.B. i001 oder e002)")
    sys.exit(0)

cmd = sys.argv[1]
typ, id = cmd[0].lower(), cmd[1:]
print(f"→ {typ.upper()} {id}")

block = find_order(id, blocks)
if not block:
    sys.exit(f"Kein Auftrag {id} gefunden.")

# ---------------------------------------------------------
# Statusdatum eintragen falls fehlt
# ---------------------------------------------------------
if not any(l.startswith(typ + " ") for l in block):
    insert_at = 3
    while insert_at < len(block) and not re.match(r"^[0-9]", block[insert_at]):
        insert_at += 1
    block.insert(insert_at, f"{typ} {today}")
    save_orders(blocks, root / "ord.txt")
    print(f"↳ {typ.upper()}-Datum hinzugefügt: {today}")

if typ == "p":
    sys.exit(0)

# ---------------------------------------------------------
# Daten aus Auftrag
# ---------------------------------------------------------
key, title = block[1], block[2]
ref, deliver_date = "", ""
items, total = [], 0.0
for l in block[3:]:
    if l.startswith("d "):
        deliver_date = l.split()[1]
    elif not re.match(r"^[0-9]|[ecdip]\s", l):
        ref = l
    elif re.match(r"^[0-9]", l):
        p = l.split()
        q = float(p[0]); u = p[1]
        pr = float(p[2].replace(",", "."))
        desc = " ".join(p[3:])
        items.append((q, u, pr, desc))
        total += q * pr
tax = total * 0.19
gross = total + tax

# ---------------------------------------------------------
# Adresse (nur Kunde)
# ---------------------------------------------------------
adr_text = (root / "adr.txt").read_text()
blocks_adr = [b.strip().splitlines() for b in adr_text.split("\n\n") if b.strip()]
addrs, firmalinks = {}, {}
for b in blocks_adr:
    k = b[0].strip()
    addrs[k] = [l.strip() for l in b[1:] if l.strip()]
    if k.count("_") == 2:
        firmalinks[k] = "_".join(k.split("_")[:2])

adrblock = addrs.get(key, [])
contact_name = ""
if key in firmalinks:
    firmakey = firmalinks[key]
    firmablock = addrs.get(firmakey, [])
    adrblock = firmablock.copy() if firmablock else []
    contact_lines = addrs.get(key, [])
    if contact_lines:
        contact_name = contact_lines[0].strip()
        if contact_name:
            adrblock.insert(1, contact_name)
adr_full = "<br>".join(adrblock)

# =========================================================
# 6. Rechnungsnummer & Duplikatsprüfung
# =========================================================
base = base_name(typ, key, title)
existing_files = files_for_base(base)
next_num = None
title_short = title[:15]

if typ == "i":
    content_dup = invoice_exists_in_invtxt(id, key, title_short, gross, inv_lines)
    file_dup = len(existing_files) > 0
    if content_dup or file_dup:
        why = []
        if content_dup: why.append("inv.txt")
        if file_dup: why.append("Datei")
        ans = input(f"⚠️ Duplikat erkannt ({' & '.join(why)}). Trotzdem neue Rechnung anlegen? (j/n) ").strip().lower()
        if ans != "j":
            print("↳ Abgebrochen – keine neue Rechnung erzeugt.")
            sys.exit(0)
    last_num = 0
    if inv_lines:
        m = re.match(r"^(\d+)", inv_lines[-1])
        if m:
            last_num = int(m.group(1))
    next_num = last_num + 1
    line = f"{next_num} _{id} {key} {title_short} {gross:.2f} i{today}"
    inv_lines.append(line)
    inv_file.write_text("\n".join(inv_lines) + "\n", encoding="utf-8")
    print(f"↳ Neue Rechnung Nr. {next_num} für Auftrag {id} angehängt.")

# =========================================================
# 7. Daten fürs Template (komplett flach)
# =========================================================
# =========================================================
# 7. Daten fürs Template (komplett flach)
# =========================================================
data = {
    # Basiswerte aus cfg.txt
    **cfg,

    # Laufzeitdaten
    "id": id,
    "typ": typ,
    "adr_full": adr_full,
    "ord": title,
    "ref": ref,
    "d": deliver_date or today,
    "d_doc": today,
    "totals.net_eur": f"{total:.2f}",
    "totals.tax_eur": f"{tax:.2f}",
    "totals.gross_eur": f"{gross:.2f}",

    # Dokumentabhängiger Titel und Footer
    "doc": cfg.get(f"d{typ}", ""),   # ✅ Titel (di, de, dc, dd)
    "f": cfg.get(f"f{typ}", ""),     # ✅ Footer (fi, fe, fc, fd)

    # Alias für Logo
    "com": cfg.get("co", ""),
}


# =========================================================
# 8. Positionstabelle einsetzen ({{#its}}…{{/its}})
# =========================================================
if items:
    rows = "\n".join(
        f"<tr><td class='num'>{q:.0f}</td><td>{u}</td><td>{desc}</td>"
        f"<td class='num'>{pr:.2f}</td><td class='num'>{q*pr:.2f}</td></tr>"
        for q, u, pr, desc in items
    )
else:
    rows = "<tr><td colspan='5'>(keine Positionen)</td></tr>"

tpl = re.sub(r"{{#its}}[\s\S]*?{{/its}}", rows, tpl, flags=re.MULTILINE)

# =========================================================
# 9. Template füllen & Datei schreiben
# =========================================================
html = fill_html_placeholders(tpl, data)
outfile = outdir / shortname(typ, key, title, next_num if typ == "i" else None)
outfile.write_text(html, encoding="utf-8")
print("→", outfile)
