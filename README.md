# InvoiceText
*"The charm of text - the precision of numbers."*

> **The Text-Based Invoicing Tool** - minimal, portable, database-free  
> 🇩🇪 Das textbasierte Rechnungs- und Angebots-System - leicht, portabel, datenbankfrei  

---

## ✨ Overview / Überblick

InvoiceText is a lightweight, local invoicing and quotation tool that works entirely with plain text files.
No database. No server. No dependencies. You can edit everything using your favourite text editor - even on a smartphone.

InvoiceText ist ein ultraleichtes Rechnungs- und Angebotsprogramm, das vollständig mit einfachen Textdateien arbeitet.
Keine Datenbank. Kein Server. Keine Installation. Alles kann mit einem beliebigen Text-Editor bearbeitet werden - selbst mobil.

---

## 🧱 Core Idea

> "Write, calculate, and send - all from plain text."

You write your offers or orders directly as text blocks in `ord.txt`,
and the program turns them into HTML invoices, quotations or delivery notes based on your own `inv.html` template.

---

## 🧾 Features

| Feature | Description |
|----------|--------------|
| Text-based | Works with plain `.txt` files (`ord.txt`, `adr.txt`, `cfg.txt`) |
| No database | Fully local - no SQL, no dependencies |
| Portable | Works from USB stick or any folder |
| Cross-platform | Linux, Windows, macOS - only Python 3 required |
| Offline | 100 % offline - ideal for workshops, travel, laptops |
| Custom templates | Edit `inv.html` to change layout or language |
| Accurate syntax | Strict, minimal, predictable format |
| Multi-staff support | Several employees per company via extended key |

---

## ⚙️ Configuration (`cfg.txt`)

Example:

```
# Company data
co = Hilbert Holzdesign
st = Teststrasse 12
pl = 77777 Teststadt
ci = Deutschland
ib = DE12 3456 7890 0000 1234 56
tx = 123/456/78901
mail = info@hilbertcnc.de

# Document titles
di = Rechnung
de = Kostenvoranschlag
dc = Auftragsbestaetigung
dd = Lieferschein

# Footers
fi = Bitte ueberweisen Sie den Betrag nach Erhalt dieser Rechnung.
fe = Bitte erteilen Sie den Auftrag per E-Mail.
fc = Ihr Auftrag wird bearbeitet. Bitte pruefen Sie die Positionen.
fd = Lieferung erfolgt wie besprochen.
```

All values are flat key=value pairs and can be referenced in the HTML template as `{{co}}`, `{{st}}`, `{{f}}`, etc.

---

## 🧮 Syntax Rules

### Orders (`ord.txt`)

```
1
meier_max
kitchen board oak
1 pcs 120.00 oak plate
```

Every block starts with an ID, then customer key, title, and one or more positions.
Empty lines separate orders.

### Customer ID Rules

Customer keys follow this pattern:

```
<lastname:5>_<firstname:4>
```

Example:
```
meier_max
bohr_pete
```

Multiple employees of one company can be referenced like this:

```
muster_gmbh_bohr
muster_gmbh_meier
```

The program automatically links them to the base company key `muster_gmbh`.

---

## 🧠 Philosophy

InvoiceText is not a database system.  
It is a tool for people who value structure and transparency.  
Every order and invoice is a visible text block you can back up, edit, or reuse.

---

## 💚 Advantages

| | |
|-|-|
| No database | ✅ |
| No server | ✅ |
| Runs offline | ✅ |
| Works in any text editor | ✅ |
| Transparent data | ✅ |
| Fully portable | ✅ |

---

## 🧑‍💻 Author

**Carsten Hilbert**  
Schreinerwissen / C3CAD Furniture Designer  
📧 info@hilbertcnc.de  
🌐 https://c3cad.de

---

## 🤖 Acknowledgements / Danksagung

Developed with research, structuring and documentation assistance by ChatGPT (OpenAI) -  
used for bilingual documentation and consistency review.

Entwickelt mit redaktioneller und technischer Unterstuetzung durch ChatGPT (OpenAI) -  
fuer Sprachfeinschliff, zweisprachige Dokumentation und Konsistenzpruefung.

---

## 📜 License

MIT License

---

*"InvoiceText - The charm of text, the precision of numbers."*


## 🧾 Abkürzungsverzeichnis / Abbreviations

---

### 🇩🇪 Deutsch

| Abkürzung | Bedeutung | Beschreibung |
|------------|------------|---------------|
| adr | **Adressdatei** (`adr.txt`) | Enthält Kundendaten, z. B. Name, Anschrift, Ansprechpartner |
| cfg | **Konfigurationsdatei** (`cfg.txt`) | Enthält Firmendaten, Dokumenttitel, Fußtexte, E-Mail usw. |
| doc | **Dokumenttyp** | Kennzeichnet die Art des Dokuments: Rechnung, Angebot, Lieferschein … |
| html | **HyperText Markup Language** | Standard-Dateiformat für erzeugte Ausgabedokumente |
| id | **Kennung (Identifier)** | Eindeutiger Schlüssel für Kunden, Aufträge oder Mitarbeiter |
| inv | **Rechnung** | Abkürzung für erzeugte Rechnungsdokumente |
| ord | **Auftragsdatei** (`ord.txt`) | Enthält Positionen, Mengen, Preise und Beschreibungen |
| out | **Ausgabeverzeichnis** (`out/`) | Ordner für alle generierten HTML-Dokumente |
| pat | **Personal Access Token** | Zugriffstoken zur Authentifizierung bei GitHub |
| repo | **Repository** | Git-Projektordner mit allen Quelldateien |
| stk | **Stück (Unit)** | Mengeneinheit für Positionen, z. B. 1 Stk = 1 Teil |
| tpl | **Vorlage (Template)** (`tpl.html`) | HTML-Vorlage mit Platzhaltern für die Dokumentausgabe |
| txt | **Textdatei** | Reines Textformat für Konfiguration, Aufträge und Adressen |
| url | **Uniform Resource Locator** | Webadresse, z. B. Link zum GitHub-Repository |
| vat | **Mehrwertsteuer (Value Added Tax)** | Umsatzsteuerbetrag in Prozent oder Euro |

---

### 🇬🇧 English

| Abbrev. | Meaning | Description |
|----------|----------|-------------|
| adr | **Address file** (`adr.txt`) | Contains client data such as name, address, contact person |
| cfg | **Configuration file** (`cfg.txt`) | Contains company data, document titles, footers, email info, etc. |
| doc | **Document type** | Indicates the document category: invoice, offer, delivery note, etc. |
| html | **HyperText Markup Language** | Standard file format for generated output documents |
| id | **Identifier** | Unique key for customers, orders or employees |
| inv | **Invoice** | Short form for generated invoice documents |
| ord | **Order file** (`ord.txt`) | Contains line items, quantities, prices and descriptions |
| out | **Output folder** (`out/`) | Directory for all generated HTML documents |
| pat | **Personal Access Token** | Access token used for GitHub authentication |
| repo | **Repository** | Git project folder containing all source files |
| stk | **Piece (Unit)** | Quantity unit for order positions, e.g. 1 stk = 1 item |
| tpl | **Template** (`tpl.html`) | HTML layout template containing placeholders |
| txt | **Text file** | Plain text format for configuration, orders and addresses |
| url | **Uniform Resource Locator** | Web address, e.g. link to the GitHub repository |
| vat | **Value Added Tax** | Sales tax value in percent or currency |

---
