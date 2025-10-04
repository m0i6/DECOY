#!/usr/bin/env python3
"""
Safe SSH-banner honeypot (no credential harvesting).

- Reads LISTEN_PORT and CENTRAL_ALERT_URL from environment.
- Sends SSH banner, reads a bit, then closes.
- Sends an alert (client IP, port, timestamp, raw bytes length) to CENTRAL_ALERT_URL via HTTP POST.
- Does NOT parse or store usernames/passwords.
"""
import os
import socket
import threading
import datetime
import logging
import signal
import sys
import requests

LISTEN_PORT = int(os.getenv("LISTEN_PORT", "2222"))
CENTRAL_ALERT_URL = os.getenv("CENTRAL_ALERT_URL", "")  # e.g. https://alerts.example.com/honeypot
BANNER = b"SSH-2.0-OpenSSH_7.6p1 Ubuntu-4ubuntu0.3\r\n"
LOG_FORMAT = "%(asctime)s %(levelname)s %(message)s"
logging.basicConfig(level=logging.INFO, format=LOG_FORMAT)

shutdown_flag = threading.Event()

def send_alert(payload):
    if not CENTRAL_ALERT_URL:
        logging.info("CENTRAL_ALERT_URL not set — skipping HTTP alert.")
        return
    requests.post(CENTRAL_ALERT_URL, json=payload)

def handle_client(conn, addr):
    client_ip, client_port = addr[0], addr[1]
    ts = datetime.datetime.utcnow().isoformat() + "Z"
    logging.info("Connection from %s:%d", client_ip, client_port)
    try:
        # Send SSH banner
        conn.sendall(BANNER)
        # Try to read up to 1024 bytes (do not interpret as credentials)
        conn.settimeout(5.0)
        try:
            data = conn.recv(1024)
            received_len = len(data) if data is not None else 0
        except socket.timeout:
            received_len = 0
        # Close connection
        conn.close()
        logging.info("Closed connection from %s (received %d bytes)", client_ip, received_len)

        # Build minimal alert (no credentials)
        alert = {
            "timestamp": ts,
            "severity": "moderate",
            "description": f"Login from {client_ip}:{client_port}",
            "title": "Suspicious login attempt",
        }
        # Send alert asynchronously (thread)
        threading.Thread(target=send_alert, args=(alert,), daemon=True).start()

    except Exception as e:
        logging.exception("Error handling client %s: %s", client_ip, e)
        try:
            conn.close()
        except Exception:
            pass

def serve():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        s.bind(("0.0.0.0", LISTEN_PORT))
        s.listen(100)
        logging.info("Listening on 0.0.0.0:%d", LISTEN_PORT)
        while not shutdown_flag.is_set():
            try:
                s.settimeout(1.0)
                conn, addr = s.accept()
                t = threading.Thread(target=handle_client, args=(conn, addr), daemon=True)
                t.start()
            except socket.timeout:
                continue
            except OSError:
                break

def on_signal(sig, frame):
    logging.info("Shutting down (signal %s)", sig)
    shutdown_flag.set()

if __name__ == "__main__":
    signal.signal(signal.SIGINT, on_signal)
    signal.signal(signal.SIGTERM, on_signal)
    try:
        serve()
    except Exception:
        logging.exception("Server error")
        sys.exit(1)
