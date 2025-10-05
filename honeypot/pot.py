#!/usr/bin/env python3
"""
Environment variables (all optional):
  LISTEN_HOST="0.0.0.0" (use "::" for dual-stack on many distros)
  LISTEN_PORT="2222"
  CENTRAL_ALERT_URL="https://alerts.example.com/honeypot"
  READ_TIMEOUT="3.0"       (seconds)
  READ_LIMIT="1024"        (bytes, pre-auth only)
  ALERT_TIMEOUT="2.0"      (seconds for HTTP POST timeout)
  MAX_CONN_PER_MIN="60"    (per source IP; 0 disables rate limiting)
  TARPIT_SECONDS="0"       (extra delay applied to abusers; 0 disables)
  BANNER="SSH-2.0-OpenSSH_8.9p1 Ubuntu-3"
  BANNER_ROTATE="false"    ("true" rotates through BANNERS per connection)
  BANNERS="SSH-2.0-OpenSSH_8.9p1 Ubuntu-3;SSH-2.0-OpenSSH_8.4p1 Debian-5;SSH-2.0-OpenSSH_7.6p1 Ubuntu-4ubuntu0.3"
"""
from __future__ import annotations

import asyncio
import datetime as _dt
import logging
import os
import queue
import random
import signal
import socket
import sys
import threading
import time
from collections import defaultdict, deque
from typing import Deque, Dict, Tuple

import requests

__version__ = "0.4.0"


LISTEN_HOST = os.getenv("LISTEN_HOST", "0.0.0.0")
LISTEN_PORT = int(os.getenv("LISTEN_PORT", "2222"))
HONEYPOT_ID = int(os.getenv("HONEYPOT_ID", "1"))
CENTRAL_ALERT_URL = os.getenv(
    "CENTRAL_ALERT_URL", ""
)  # e.g. https://alerts.example.com/honeypot

READ_TIMEOUT = float(os.getenv("READ_TIMEOUT", "3.0"))
READ_LIMIT = int(os.getenv("READ_LIMIT", "1024"))
ALERT_TIMEOUT = float(os.getenv("ALERT_TIMEOUT", "2.0"))
MAX_CONN_PER_MIN = int(os.getenv("MAX_CONN_PER_MIN", "60"))
TARPIT_SECONDS = float(os.getenv("TARPIT_SECONDS", "0"))

_DEFAULT_BANNER = os.getenv("BANNER", "SSH-2.0-OpenSSH_8.9p1 Ubuntu-3")
BANNER_ROTATE = os.getenv("BANNER_ROTATE", "false").strip().lower() in {
    "1",
    "true",
    "yes",
}
_BANNERS = os.getenv(
    "BANNERS",
    "SSH-2.0-OpenSSH_8.9p1 Ubuntu-3;SSH-2.0-OpenSSH_8.4p1 Debian-5;SSH-2.0-OpenSSH_7.6p1 Ubuntu-4ubuntu0.3",
).split(";")
BANNERS = [b.strip() for b in _BANNERS if b.strip()] or [_DEFAULT_BANNER]

LOG_FORMAT = "%(asctime)s %(levelname)s %(message)s"
logging.basicConfig(level=logging.INFO, format=LOG_FORMAT)


shutdown_event = asyncio.Event()
alert_q: "queue.Queue[Tuple[str, dict]]" = queue.Queue(maxsize=10000)
ip_hits: Dict[str, Deque[float]] = defaultdict(deque)


def _post_alert_worker():
    """Background worker to POST alerts with basic retries and timeouts."""
    session = requests.Session()
    while True:
        item = alert_q.get()
        if item is None:
            break
        url, payload = item
        if not url:
            continue
        for attempt in range(3):
            try:
                session.post(url, json=payload, timeout=ALERT_TIMEOUT)
                break
            except Exception as e:
                if attempt == 2:
                    logging.warning("Alert POST failed (giving up): %s", e)
                time.sleep(0.5 * (2**attempt))


def send_alert(payload: dict):
    """Queue an alert for async delivery."""
    try:
        alert_q.put_nowait((CENTRAL_ALERT_URL, payload))
    except queue.Full:
        logging.warning("Alert queue full; dropping alert")


def utc_now_iso() -> str:
    return _dt.datetime.now(_dt.timezone.utc).isoformat()


def pick_banner() -> bytes:
    if BANNER_ROTATE:
        banner = random.choice(BANNERS)
    else:
        banner = BANNERS[0]
    if not banner.endswith("\r\n"):
        banner = banner + "\r\n"
    return banner.encode("ascii", errors="ignore")


def _peername_to_ip_port(peer) -> Tuple[str, int]:
    # peer can be (ip, port) for IPv4; (ip, port, flow, scope) for IPv6
    try:
        ip = peer[0]
        port = peer[1]
        return ip, int(port)
    except Exception:
        return "0.0.0.0", 0


def _sockname(writer: asyncio.StreamWriter) -> Tuple[str, int]:
    try:
        local = writer.get_extra_info("sockname")
        return _peername_to_ip_port(local)
    except Exception:
        return "0.0.0.0", LISTEN_PORT


def _classify_and_rules(
    first_bytes: bytes, client_ident: str
) -> Tuple[str, str, float, bytes]:
    """
    Returns (family, reason, delay_seconds, extra_reply_bytes).
    family  - one of: OpenSSH, Paramiko, libssh, libssh2, Go, PuTTY, Dropbear, JSCH, AsyncSSH, Nmap, Masscan, http, tls, garbage, generic
    reason  - e.g., ssh_ident, wrong_protocol_http, wrong_protocol_tls, no_ident, garbage
    delay_seconds - additional delay to apply before closing
    extra_reply_bytes - e.g., b"Protocol mismatch.\r\n" for non-SSH
    """
    delay = 0.0
    extra = b""

    if not first_bytes:
        return ("generic", "no_ident", delay, extra)

    # TLS ClientHello (starts with 0x16 0x03 0x0X)
    if len(first_bytes) >= 3 and first_bytes[0] == 0x16 and first_bytes[1] == 0x03:
        return ("tls", "wrong_protocol_tls", delay, extra)

    # HTTP and friends
    l4 = first_bytes[:4].upper()
    if l4 in (b"GET ", b"POST", b"HEAD", b"PUT ", b"OPTI", b"CONN", b"PRI "):
        extra = b"Protocol mismatch.\r\n"
        return ("http", "wrong_protocol_http", delay, extra)

    if client_ident:
        lo = client_ident.lower()
        family = "generic"
        if "openssh" in lo:
            family = "OpenSSH"
        elif "paramiko" in lo:
            family = "Paramiko"
        elif "libssh2" in lo:
            family = "libssh2"
        elif "libssh" in lo:
            family = "libssh"
        elif "go" in lo or "golang" in lo:
            family = "Go"
        elif "putty" in lo:
            family = "PuTTY"
        elif "dropbear" in lo:
            family = "Dropbear"
        elif "jsch" in lo:
            family = "JSCH"
        elif "asyncssh" in lo:
            family = "AsyncSSH"
        elif "nmap" in lo:
            family = "Nmap"
        elif "masscan" in lo:
            family = "Masscan"

        # Heuristic delays to look more "real"
        if family in {"Nmap", "Masscan"}:
            delay = random.uniform(0.8, 1.6)
        elif family in {"Paramiko", "libssh", "libssh2", "AsyncSSH", "Go"}:
            delay = random.uniform(0.2, 0.7)
        else:
            delay = random.uniform(0.05, 0.25)

        return (family, "ssh_ident", delay, extra)

    # Garbage or other unrecognized plaintext
    return ("garbage", "garbage", delay, extra)


def _inc_and_rate_limit(ip: str, now: float) -> Tuple[int, bool]:
    """
    Track per-IP connection counts within the last minute.
    Returns (count_in_last_min, is_rate_limited)
    """
    dq = ip_hits[ip]
    dq.append(now)
    # purge older than 60s
    while dq and now - dq[0] > 60.0:
        dq.popleft()
    count = len(dq)
    if MAX_CONN_PER_MIN <= 0:
        return (count, False)
    return (count, count > MAX_CONN_PER_MIN)


def _severity_from(
    family: str, reason: str, count_last_min: int, rate_limited: bool
) -> Tuple[str, int]:
    """
    Returns (severity_string, severity_number[1..10])
    """
    sev = "moderate"
    sn = 5
    if reason.startswith("wrong_protocol"):
        sev, sn = ("low", 3)
    if family in {"Nmap", "Masscan"}:
        sev, sn = ("moderate", 5)
    if rate_limited or count_last_min > MAX_CONN_PER_MIN:
        sev, sn = ("high", 8)
    return sev, sn


async def handle_client(reader: asyncio.StreamReader, writer: asyncio.StreamWriter):
    ts = utc_now_iso()
    peer = writer.get_extra_info("peername")
    client_ip, client_port = _peername_to_ip_port(peer)
    local_ip, local_port = _sockname(writer)

    # Rate limiting / tarpit decision recorded *before* reading
    now = time.time()
    count_last_min, rate_limited = _inc_and_rate_limit(client_ip, now)

    banner = pick_banner()
    try:
        writer.write(banner)
        await writer.drain()
    except Exception:
        # If we can't even send the banner, not much to do.
        try:
            writer.close()
            await writer.wait_closed()
        except Exception:
            pass
        return

    # Read at most READ_LIMIT bytes with timeout (pre-auth only).
    try:
        first_bytes = await asyncio.wait_for(
            reader.read(READ_LIMIT), timeout=READ_TIMEOUT
        )
    except asyncio.TimeoutError:
        first_bytes = b""
    except Exception:
        first_bytes = b""

    # Extract just the identification line (client banner), ASCII only.
    client_ident = ""
    if first_bytes:
        try:
            line = first_bytes.split(b"\n", 1)[0].rstrip(b"\r")
            client_ident = line.decode("ascii", errors="ignore")
        except Exception:
            client_ident = ""

    # Classify & pick rule-based response
    family, reason, rule_delay, extra_reply = _classify_and_rules(
        first_bytes, client_ident
    )

    # Apply tarpit/rate limit delay if configured
    total_delay = rule_delay
    if rate_limited and TARPIT_SECONDS > 0:
        total_delay = max(total_delay, TARPIT_SECONDS)

    if total_delay > 0:
        try:
            await asyncio.sleep(total_delay)
        except Exception:
            pass

    # For obvious protocol mismatch, it's plausible for servers to emit a line
    # before closing; keep this small and only when we detected HTTP. Avoid for TLS/binary.
    if extra_reply:
        try:
            writer.write(extra_reply)
            await writer.drain()
        except Exception:
            pass

    # Close connection
    try:
        writer.close()
        await writer.wait_closed()
    except Exception:
        pass

    bytes_received = len(first_bytes) if first_bytes else 0

    # Build alert (minimal + enrichment). No credentials are parsed or stored.
    severity, severity_number = _severity_from(
        family, reason, count_last_min, rate_limited
    )
    alert = {
        "@timestamp": ts,
        "title": "SSH honeypot connection",
        "honeypot_id": HONEYPOT_ID,
        "description": f"Connection from {client_ip}:{client_port}",
        "severity": severity,
        "severity_number": severity_number,
        "event": {
            "kind": "event",
            "category": "network",
            "type": ["connection"],
            "action": "ssh_banner",
            "dataset": "ssh.honeypot",
        },
        "network": {
            "transport": "tcp",
            "protocol": "ssh",
            "direction": "ingress",
            "bytes": bytes_received,
        },
        "source": {"ip": client_ip, "port": client_port},
        "destination": {"ip": local_ip, "port": local_port},
        "observer": {"type": "honeypot", "version": __version__},
        "ssh": {
            "client": {"ident": client_ident},
            "server": {"banner": banner.decode("ascii", errors="ignore").strip()},
        },
        "classification": {"family": family, "reason": reason},
        "rate": {"count_last_min": count_last_min, "rate_limited": rate_limited},
    }

    logging.info(
        "Handled %s:%d -> %s:%d | %s/%s bytes=%d count/min=%d%s",
        client_ip,
        client_port,
        local_ip,
        local_port,
        family,
        reason,
        bytes_received,
        count_last_min,
        " [RL]" if rate_limited else "",
    )

    # Enqueue alert (non-blocking); if CENTRAL_ALERT_URL is unset, worker will skip send.
    send_alert(alert)


async def serve():
    # Start alert worker thread
    worker = threading.Thread(
        target=_post_alert_worker, name="alert-worker", daemon=True
    )
    worker.start()

    # Start server (IPv4 or IPv6 depending on LISTEN_HOST)
    server = await asyncio.start_server(
        handle_client,
        host=LISTEN_HOST,
        port=LISTEN_PORT,
        reuse_address=True,
    )
    addresses = ", ".join(str(sock.getsockname()) for sock in server.sockets or [])
    logging.info("Listening on %s", addresses)

    async with server:
        await shutdown_event.wait()
        logging.info("Shutdown requested; closing listener")
        server.close()
        await server.wait_closed()

    # Stop alert worker
    alert_q.put(None)
    worker.join(timeout=2.0)


def _handle_signal(sig, frame):
    logging.info("Shutting down (signal %s)", sig)
    try:
        loop = asyncio.get_event_loop()
        loop.call_soon_threadsafe(shutdown_event.set)
    except Exception:
        # Fallback for edge cases
        try:
            shutdown_event.set()
        except Exception:
            pass


def main():
    signal.signal(signal.SIGINT, _handle_signal)
    signal.signal(signal.SIGTERM, _handle_signal)
    try:
        asyncio.run(serve())
    except KeyboardInterrupt:
        pass
    except Exception:
        logging.exception("Server error")
        sys.exit(1)


if __name__ == "__main__":
    main()
