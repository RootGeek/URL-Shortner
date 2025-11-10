# Easy2Use URL Shortener with IP Logging

Self-hosted URL shortener with click logging & simple admin panel.  
Developed by **RootGeek**.

> ⚠️ **Disclaimer**
> Dieses Tool ist nur für **legale & autorisierte** Einsatzzwecke gedacht  
> (eigene Projekte, interne Tests, Pentests mit Erlaubnis etc.).  
> Halte dich an DSGVO & lokale Gesetze. Du trägst die volle Verantwortung.

---

## Features

- 🌑 **Dark Mode only**
  - Fester Dark Mode, kein Umschalter.
  - Minimalistisches, klares UI.

- 🔗 **URL Shortener**
  - Erstelle Kurzlinks zu beliebigen Ziel-URLs.
  - Optional eigene Slugs.
  - Übersichtliche Liste aller Links.

- 🕵️ **IP- & Request-Logging**
  Pro Klick können u.a. gespeichert werden:
  - IP-Adresse
  - Timestamp
  - User-Agent
  - Referrer
  - Accept-Language

- 📊 **Per-Link Analytics**
  - Detailansicht mit allen Klicks.
  - Geeignet für Auswertung & Monitoring.

- 🗑️ **Link-Management**
  - Links komfortabel im Panel löschen.
  - (Je nach Implementierung) zugehörige Logs mitentfernbar.

- 🗄️ **Self-Hosted & Lightweight**
  - FastAPI + SQLite
  - Keine Fremd-APIs, kein Cloud-Zwang.

---

## Quickstart (mit `start.sh`)

Das Projekt bringt ein Start-Script mit, um dir Setup & Start zu erleichtern.

### 1. Voraussetzungen

Auf z. B. Ubuntu:

```bash
sudo apt update
sudo apt install -y python3 python3-venv python3-pip git
```

### 2. Repository klonen

```bash
git clone https://github.com/DEIN_USERNAME/DEIN_REPO.git
cd DEIN_REPO
```

### 3. Script ausführbar machen

```bash
chmod +x start.sh
```

### 4. Starten

```bash
./start.sh
```

Was das Script typischerweise macht (abhängig von deiner Version):

- erstellt eine virtuelle Umgebung (.venv), falls nicht vorhanden
- installiert die Pakete aus requirements.txt
- richtet die notwendige Struktur/Dateien ein (z. B. Datenbank)
- startet die FastAPI-App über uvicorn

Nach erfolgreichem Start:

```
http://DEINE_SERVER_IP:8000
```

oder (wenn im Script konfiguriert):

```
https://DEINE_SERVER_IP:PORT
```

Schau in den Output des Scripts, dort steht:

- welche URL
- welcher Port
- ob HTTP oder HTTPS
- evtl. Hinweise auf Zertifikate / selbstsigniertes Zertifikat

---

## Manuelle Installation (ohne start.sh)

Falls du die Kontrolle lieber selbst übernimmst oder das Script nicht nutzen willst:

### 1. Virtuelle Umgebung

```bash
python3 -m venv .venv
source .venv/bin/activate
```

### 2. Dependencies

```bash
pip install --upgrade pip
pip install -r requirements.txt
```

### 3. Environment Variablen setzen (empfohlen)

```bash
export SECRET_KEY="ein-langer-zufälliger-und-geheimer-key"
export DATABASE_URL="sqlite:///./shortener.db"
```

- **SECRET_KEY**: Pflicht für Produktion – lang, zufällig, geheim.
- **DATABASE_URL**: Standard SQLite-Datei im Projektordner.

### 4. Server starten

```bash
uvicorn app.main:app --host 0.0.0.0 --port 8000
```

Dann im Browser:

```
http://DEINE_SERVER_IP:8000
```

Für Produktion:

- vor nginx/Traefik hängen
- HTTPS aktivieren
- SECRET_KEY & Cookies sicher konfigurieren

---

## Login & Admin

Das Admin-Panel ist geschützt.

Die genaue Umsetzung hängt von deinem Code ab, typischer Ablauf:

1. Beim ersten Start einen Benutzer/Account anlegen (via Setup-Route, Script oder direkt in der DB).
2. Login über die Weboberfläche.
3. Sitzungen laufen über signierte Cookies.

Empfehlungen:

- Starke Passwörter.
- Panel nur für dich / vertraute IPs (Firewall / VPN / Reverse Proxy).

---

## Nutzung

### Kurzlink erstellen

1. Einloggen.
2. Ziel-URL eintragen.
3. Optional: eigenen Slug setzen.
4. Speichern.

Du bekommst z. B.:

```
https://DEIN_HOST/abc123
```

### Klicks & Logs ansehen

In der Link-Detailansicht:

- Liste aller Aufrufe
- Datum/Uhrzeit
- IP
- User-Agent
- Referrer
- Sprache

### Links löschen

Im Panel:

- Links entfernen
- (je nach Implementierung) Logs mit löschen

---

## Deployment-Empfehlungen

Für einen sauberen produktiven Betrieb:

1. **Reverse Proxy** (nginx/Traefik) vor den Uvicorn-Server.
2. **HTTPS** erzwingen (Let's Encrypt).
3. Starker **SECRET_KEY**.
4. **Admin-Panel schützen**:
   - IP-Restriktion / VPN / zusätzliche Auth.
5. Regelmäßige **Backups** der SQLite-DB.

---

## Rechtliches

Durch IP-Logging & Tracking entstehen personenbezogene Daten.

Du solltest:

- klar informieren (Privacy-Hinweis / Disclaimer).
- nur dort einsetzen, wo du eine Rechtsgrundlage + Erlaubnis hast.
- das Tool **nicht missbrauchen** für:
  - Phishing
  - Doxxing / Stalking
  - heimliche Überwachung
  - sonstige strafbare Aktionen

---

## Credits

Entwickelt von **RootGeek**.

Technologien: FastAPI, Uvicorn, SQLite, Tailwind, Jinja2.
