# this file is run once to create some initial data in the database

from database.db import db
from database.models.HoneyPotModel import HoneyPotModel
from database.models.IncidentLogModel import IncidentLogModel
from main import create_app

app = create_app()
with app.app_context():
    db.create_all()

    result = db.session.add(HoneyPotModel(
        name="Engie Deutschland AG - SFTP Honeypot",
        server_category="sftp",
        description="A test SFTP honeypot",
        geolocation="52.5200,13.4050",  # Berlin
        behaviors="ssh,ftp"
    ))
    print("Result of add operation:", result)
    db.session.add(HoneyPotModel(
        name="PGE Group - Database Honeypot",
        server_category="database",
        description="A test database honeypot",
        geolocation="52.2297,21.0122",  # Warsaw
        behaviors="mysql,postgres"
    ))
    db.session.add(HoneyPotModel(
        name="PGE Group - SSH Honeypot",
        server_category="ssh",
        description="A test SSH honeypot with open port",
        geolocation="52.4064,16.9252",  # Poznań
        behaviors="ssh"
    ))
    db.session.add(HoneyPotModel(
        name="Enel SpA - Web Honeypot",
        server_category="web",
        description="Web server honeypot for Enel SpA",
        geolocation="41.9028,12.4964",  # Rome
        behaviors="http,https"
    ))
    db.session.add(HoneyPotModel(
        name="EDF Group - SCADA Honeypot",
        server_category="scada",
        description="SCADA honeypot for EDF Group",
        geolocation="48.8566,2.3522",  # Paris
        behaviors="modbus,dnp3"
    ))
    db.session.add(HoneyPotModel(
        name="Duke Energy - FTP Honeypot",
        server_category="ftp",
        description="FTP honeypot for Duke Energy",
        geolocation="50.1109,8.6821",  # Frankfurt
        behaviors="ftp"
    ))
    db.session.add(HoneyPotModel(
        name="E.ON SE - RDP Honeypot",
        server_category="rdp",
        description="RDP honeypot for E.ON SE",
        geolocation="51.2277,6.7735",  # Düsseldorf
        behaviors="rdp"
    ))
    db.session.add(HoneyPotModel(
        name="Southern Company - Email Honeypot",
        server_category="email",
        description="Email honeypot for Southern Company",
        geolocation="48.1351,11.5820",  # Munich
        behaviors="smtp,imap"
    ))
    db.session.add(HoneyPotModel(
        name="National Grid plc - API Honeypot",
        server_category="api",
        description="API endpoint honeypot for National Grid plc",
        geolocation="51.5074,-0.1278",  # London
        behaviors="rest,graphql"
    ))
    db.session.add(HoneyPotModel(
        name="Iberdrola SA - IoT Honeypot",
        server_category="iot",
        description="IoT device honeypot for Iberdrola SA",
        geolocation="40.4168,-3.7038",  # Madrid
        behaviors="mqtt,coap"
    ))
    db.session.add(HoneyPotModel(
        name="Exelon Corporation - DNS Honeypot",
        server_category="dns",
        description="DNS honeypot for Exelon Corporation",
        geolocation="59.3293,18.0686",  # Stockholm
        behaviors="dns"
    ))
    
    db.session.add(HoneyPotModel(
        name="NextEra Energy - Telnet Honeypot",
        server_category="telnet",
        description="Telnet honeypot for NextEra Energy",
        geolocation="45.4642,9.1900",  # Milan
        behaviors="telnet"
    ))
    db.session.add(HoneyPotModel(
        name="Vattenfall AB - MQTT Honeypot",
        server_category="iot",
        description="MQTT honeypot for Vattenfall AB",
        geolocation="59.3326,18.0649",  # Stockholm
        behaviors="mqtt"
    ))
    db.session.add(HoneyPotModel(
        name="Fortum Oyj - Web Honeypot",
        server_category="web",
        description="Web server honeypot for Fortum Oyj",
        geolocation="60.1699,24.9384",  # Helsinki
        behaviors="http,https"
    ))
    db.session.add(HoneyPotModel(
        name="CEZ Group - SSH Honeypot",
        server_category="ssh",
        description="SSH honeypot for CEZ Group",
        geolocation="50.0755,14.4378",  # Prague
        behaviors="ssh"
    ))
    db.session.add(HoneyPotModel(
        name="Statkraft AS - Database Honeypot",
        server_category="database",
        description="Database honeypot for Statkraft AS",
        geolocation="63.4305,10.3951",  # Trondheim
        behaviors="mysql,postgres"
    ))
    db.session.add(HoneyPotModel(
        name="Iberdrola SA - FTP Honeypot",
        server_category="ftp",
        description="FTP honeypot for Iberdrola SA",
        geolocation="43.2630,-2.9350",  # Bilbao
        behaviors="ftp"
    ))
    db.session.add(HoneyPotModel(
        name="EnBW Energie Baden-Württemberg AG - SCADA Honeypot",
        server_category="scada",
        description="SCADA honeypot for EnBW",
        geolocation="48.7758,9.1829",  # Stuttgart
        behaviors="modbus,dnp3"
    ))
    
    print("Added initial honeypots.")

    db.session.add(IncidentLogModel(
        title="Unauthorized SSH Access",
        category="network",
        description="Multiple failed SSH login attempts detected.",
        severity="moderate",
        honeypot_id=1
    ))
    db.session.add(IncidentLogModel(
        title="SQL Injection Attempt",
        category="software",
        description="Detected SQL injection attempt on login form.",
        severity="critical",
        honeypot_id=2
    ))
    db.session.add(IncidentLogModel(
        title="FTP Brute Force Attack",
        category="network",
        description="Repeated failed FTP login attempts.",
        severity="moderate",
        honeypot_id=6
    ))
    db.session.add(IncidentLogModel(
        title="Malware Upload Detected",
        category="software",
        description="Suspicious file uploaded to web honeypot.",
        severity="moderate",
        honeypot_id=4
    ))
    db.session.add(IncidentLogModel(
        title="Phishing Email Received",
        category="email",
        description="Phishing attempt detected in incoming email.",
        severity="moderate",
        honeypot_id=8
    ))
    db.session.add(IncidentLogModel(
        title="RDP Unauthorized Access",
        category="network",
        description="Unauthorized RDP connection attempt.",
        severity="critical",
        honeypot_id=7
    ))
    db.session.add(IncidentLogModel(
        title="SCADA Protocol Scan",
        category="network",
        description="Modbus protocol scan detected.",
        severity="moderate",
        honeypot_id=5
    ))
    db.session.add(IncidentLogModel(
        title="DNS Amplification Attempt",
        category="network",
        description="DNS query pattern matches amplification attack.",
        severity="moderate",
        honeypot_id=11
    ))
    db.session.add(IncidentLogModel(
        title="IoT Device Enumeration",
        category="iot",
        description="Multiple connection attempts to IoT honeypot.",
        severity="low",
        honeypot_id=10
    ))
    db.session.add(IncidentLogModel(
        title="Telnet Default Credentials Used",
        category="network",
        description="Login attempt with default credentials on Telnet.",
        severity="moderate",
        honeypot_id=12
    ))
    db.session.add(IncidentLogModel(
        title="GraphQL Introspection Query",
        category="api",
        description="Suspicious introspection query on API endpoint.",
        severity="low",
        honeypot_id=9
    ))
    db.session.add(IncidentLogModel(
        title="SMTP Relay Attempt",
        category="email",
        description="Attempt to use SMTP server as open relay.",
        severity="moderate",
        honeypot_id=8
    ))
    db.session.add(IncidentLogModel(
        title="SSH Port Scan",
        category="network",
        description="Port scan targeting SSH honeypot detected.",
        severity="low",
        honeypot_id=3
    ))
    db.session.add(IncidentLogModel(
        title="Web Directory Traversal",
        category="software",
        description="Directory traversal attempt on web honeypot.",
        severity="moderate",
        honeypot_id=4
    ))
    db.session.add(IncidentLogModel(
        title="Database Credential Stuffing",
        category="software",
        description="Multiple credential stuffing attempts on database.",
        severity="moderate",
        honeypot_id=2
    ))
    db.session.add(IncidentLogModel(
        title="SCADA Unauthorized Command",
        category="network",
        description="Unauthorized Modbus command sent to SCADA honeypot.",
        severity="moderate",
        honeypot_id=5
    ))
    db.session.add(IncidentLogModel(
        title="FTP Anonymous Login",
        category="network",
        description="Anonymous login to FTP honeypot detected.",
        severity="low",
        honeypot_id=6
    ))
    db.session.add(IncidentLogModel(
        title="IoT Firmware Exploit Attempt",
        category="iot",
        description="Exploit attempt targeting IoT device firmware.",
        severity="moderate",
        honeypot_id=10
    ))
    db.session.add(IncidentLogModel(
        title="API Rate Limit Exceeded",
        category="api",
        description="Excessive requests to API endpoint.",
        severity="low",
        honeypot_id=9
    ))
    db.session.add(IncidentLogModel(
        title="DNS Tunneling Detected",
        category="network",
        description="Suspicious DNS tunneling activity.",
        severity="critical",
        honeypot_id=11
    ))
    db.session.add(IncidentLogModel(
        title="RDP Brute Force",
        category="network",
        description="Multiple failed RDP login attempts.",
        severity="moderate",
        honeypot_id=7
    ))
    db.session.add(IncidentLogModel(
        title="Web Honeypot XSS Attempt",
        category="software",
        description="Cross-site scripting attempt detected.",
        severity="moderate",
        honeypot_id=4
    ))
    db.session.add(IncidentLogModel(
        title="SSH Credential Harvesting",
        category="network",
        description="Attempt to harvest SSH credentials.",
        severity="moderate",
        honeypot_id=3
    ))
    db.session.commit()
    print("Added initial incident logs.")