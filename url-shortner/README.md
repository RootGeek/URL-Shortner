# Easy2Use URL Shortener with IP Logging

Self-hosted URL shortener with click logging & simple admin panel.  
Developed by **RootGeek**.

> ⚠️ **Disclaimer**
> This tool is intended for **legal & authorized** use only  
> (personal projects, internal testing, pentests with permission, etc.).  
> Comply with GDPR & local laws. You bear full responsibility.

---

## Features

- 🌑 **Dark Mode only**
  - Fixed dark mode, no toggle.
  - Minimalist, clean UI.

- 🔗 **URL Shortener**
  - Create short links to any target URLs.
  - Optional custom slugs.
  - Clear overview of all links.

- 🕵️ **IP & Request Logging**
  Per click, the following can be stored:
  - IP address
  - Timestamp
  - User-Agent
  - Referrer
  - Accept-Language

- 📊 **Per-Link Analytics**
  - Detailed view with all clicks.
  - Suitable for analysis & monitoring.

- 🗑️ **Link Management**
  - Comfortably delete links in the panel.
  - (Depending on implementation) associated logs can be removed.

- 🗄️ **Self-Hosted & Lightweight**
  - FastAPI + SQLite
  - No third-party APIs, no cloud dependency.

---

## Quickstart (with `start.sh`)

The project includes a start script to simplify setup & startup.

### 1. Prerequisites

On Ubuntu, for example:

```bash
sudo apt update
sudo apt install -y python3 python3-venv python3-pip git
```

### 2. Clone Repository

```bash
git clone https://github.com/YOUR_USERNAME/YOUR_REPO.git
cd YOUR_REPO
```

### 3. Make Script Executable

```bash
chmod +x start.sh
```

### 4. Start

```bash
./start.sh
```

What the script typically does (depending on your version):

- creates a virtual environment (.venv) if not present
- installs packages from requirements.txt
- sets up necessary structure/files (e.g., database)
- starts the FastAPI app via uvicorn

After successful start:

```
http://YOUR_SERVER_IP:8000
```

or (if configured in the script):

```
https://YOUR_SERVER_IP:PORT
```

Check the script output, which will show:

- which URL
- which port
- whether HTTP or HTTPS
- possibly hints about certificates / self-signed certificate

---

## Manual Installation (without start.sh)

If you prefer to maintain control yourself or don't want to use the script:

### 1. Virtual Environment

```bash
python3 -m venv .venv
source .venv/bin/activate
```

### 2. Dependencies

```bash
pip install --upgrade pip
pip install -r requirements.txt
```

### 3. Set Environment Variables (recommended)

```bash
export SECRET_KEY="a-long-random-and-secret-key"
export DATABASE_URL="sqlite:///./shortener.db"
```

- **SECRET_KEY**: Required for production – long, random, secret.
- **DATABASE_URL**: Standard SQLite file in project folder.

### 4. Start Server

```bash
uvicorn app.main:app --host 0.0.0.0 --port 8000
```

Then in browser:

```
http://YOUR_SERVER_IP:8000
```

For production:

- place behind nginx/Traefik
- enable HTTPS
- configure SECRET_KEY & cookies securely

---

## Login & Admin

The admin panel is protected.

The exact implementation depends on your code, typical workflow:

1. On first start, create a user/account (via setup route, script, or directly in DB).
2. Login via web interface.
3. Sessions run via signed cookies.

Recommendations:

- Strong passwords.
- Panel only for you / trusted IPs (firewall / VPN / reverse proxy).

---

## Usage

### Create Short Link

1. Log in.
2. Enter target URL.
3. Optional: set custom slug.
4. Save.

You'll get, for example:

```
https://YOUR_HOST/abc123
```

### View Clicks & Logs

In the link detail view:

- List of all visits
- Date/Time
- IP
- User-Agent
- Referrer
- Language

### Delete Links

In the panel:

- Remove links
- (depending on implementation) delete logs along with them

---

## Deployment Recommendations

For clean production operation:

1. **Reverse Proxy** (nginx/Traefik) in front of the Uvicorn server.
2. **HTTPS** enforcement (Let's Encrypt).
3. Strong **SECRET_KEY**.
4. **Protect Admin Panel**:
   - IP restriction / VPN / additional auth.
5. Regular **backups** of SQLite DB.

---

## Legal

IP logging & tracking creates personal data.

You should:

- clearly inform (privacy notice / disclaimer).
- only use where you have legal basis + permission.
- **not misuse** the tool for:
  - Phishing
  - Doxxing / Stalking
  - covert surveillance
  - other illegal actions

---

## Credits

Developed by **RootGeek**.

Technologies: FastAPI, Uvicorn, SQLite, Tailwind, Jinja2.
