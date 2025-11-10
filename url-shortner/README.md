# RootGeek - Self-Hosted Tracking & Link Intelligence

Modern, UI/UX-focused short-link and click intelligence tool for **authorized security testing**.

Dieses Projekt ist so gedacht, dass es problemlos auf einem **Ubuntu-Server (z.B. Hetzner)** läuft,
ohne scary Fehlermeldungen wie `externally-managed-environment` zu erzeugen.

## TL;DR Deployment auf Ubuntu (z.B. Hetzner)

**Alles wird in einem eigenen Virtual Environment installiert.**  
Keine System-Python-Zerstörung, keine Warnungen, keine Panik.

### 1. Voraussetzung (als root oder mit sudo)

```bash
apt update
apt install -y python3 python3-venv python3-pip git
```

### 2. Benutzer für RootGeek anlegen (empfohlen, optional)

```bash
useradd -m -s /bin/bash linkscope
su - linkscope
```

### 3. Projekt holen

```bash
git clone <DEIN_REPO_LINK> linkscope_app
cd linkscope_app
```

### 4. Virtual Environment erstellen (verhindert PEP-668 Fehlermeldung)

```bash
python3 -m venv .venv
source .venv/bin/activate
```

### 5. Requirements installieren (jetzt ohne Fehlermeldung)

```bash
pip install --upgrade pip
pip install -r requirements.txt
```

### 6. Server starten

```bash
uvicorn app.main:app --host 0.0.0.0 --port 8000
```

Beim ersten Start erscheint im Terminal:

```text
[RootGeek] Initial admin created:
  Username: admin
  Password: <RANDOM_PASSWORD>
```

Im Browser aufrufen:

```text
http://DEINE_SERVER_IP:8000
```

### 7. HTTPS (empfohlen, kurz)

Setze RootGeek hinter einen Reverse Proxy wie nginx oder Caddy und aktiviere Let's Encrypt.  
Beispiel-Setup kannst du in der Doku oder Präsentation zeigen.

---

## Warum keine `externally-managed-environment` Meldung mehr?

- Diese Meldung kommt nur, wenn du versuchst, global mit `pip` in das System-Python von Ubuntu zu installieren.
- In unserer Anleitung nutzen wir konsequent ein **Virtual Environment in deinem Projektordner**:
  - `python3 -m venv .venv`
  - `source .venv/bin/activate`
- Innerhalb des Venv ist `pip install -r requirements.txt` komplett sauber und zeigt diese Meldung nicht.

---

## Features (Kurzfassung)

- FastAPI + SQLite, komplett self-hosted
- Auto-Admin beim ersten Start (Zugangsdaten im Terminal)
- Login mit sicheren Cookies
- Dashboard:
  - Total Links, Total Clicks, Clicks Today, Unique IPs
  - Mini-Chart der letzten 7 Tage
  - Recent Click Stream
- Links:
  - Erstellen mit Target-URL, Custom Slug, Tags, Ablaufdatum, Max Clicks
  - Detailseite mit allen Klick-Daten
- Tracking:
  - `/r/{slug}` leitet weiter und loggt IP, User-Agent, Client-Typ, Referrer, Accept-Language & Timestamp
- UI/UX:
  - Dark, modern, Tailwind, Karten, Copy-Buttons
- Hinweistexte zu Legal/Ethik integriert

Nur für autorisierte Tests. Du bist für den Einsatz verantwortlich.


## Schnellstart (empfohlen)

Auf einem frischen Ubuntu-Server (z.B. Hetzner):

```bash
apt update
apt install -y python3 python3-venv python3-pip git
git clone <DEIN_REPO_LINK> linkscope_app
cd linkscope_app
bash start.sh
```

Danach erreichst du die Oberfläche unter:

```text
http://DEINE_SERVER_IP:8000
```

Beim ersten Start werden die Admin-Zugangsdaten im Terminal angezeigt.


## Auto-Start & HTTPS

Empfohlene Nutzung auf Ubuntu:

```bash
apt update
apt install -y python3 python3-venv python3-pip git openssl
unzip linkscope_app_final.zip -d linkscope_app
cd linkscope_app
bash start.sh
```

Das Script:

- erstellt `.venv`
- installiert Dependencies
- erzeugt beim ersten Start ein selbstsigniertes Zertifikat (`cert.pem`, `key.pem`, gültig 10 Jahre)
- startet den Server via HTTPS auf Port `8443`

Aufruf im Browser:

```text
https://DEINE_SERVER_IP:8443
```

(Browser-Warnung wegen selbstsigniertem Zertifikat ist normal.)

## Link-Verwaltung

- Links können jetzt in der Links-Liste über einen **Delete-Button** gelöscht werden.
- Auf der Detailseite eines Links kannst du eine Auto-Refresh-Periode wählen (z.B. alle 5 Sekunden), damit neue Klicks automatisch erkannt werden.
