# Decoy
*Decoy* is a cyber security defense tool, that accumulates and visualizes information about potential attackers on a centralised dashboard to streamline defense coordination.

## Frontend

## Backend
The backend is built using python and flask.
### Setup
- setup the virtual environment for the first time:
```bash
python3 -m venv .venv
source .venv/bin/activate
pip3 install -r requirements.txt
```
- for starting the server you only need to run the main.py file


{
  "name": "asdf",
  "server_category": "database",
  "description": "string",
  "creation_date": "2025-10-04T19:09:03.796Z",
  "status": "critical",
  "geolocation": "string"
}

## Honeypot

### Setup

```bash
cd honeypot
python3 -m venv .venv
source .venv/bin/activate
pip3 install -r requirements.txt
```

### Running

To run honeypot:

```bash
HONEYPOT_ID=test123 CENTRAL_ALERT_URL=http://localhost:5000/IncidentLogs/ LISTEN_PORT=2222 python pot.py
```

Then when attacker does `ssh -p 2222 root@localhost`, honeypot alerts server
