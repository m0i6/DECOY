#!/usr/bin/env python3
import socket, sys, time

host = sys.argv[1]
port = int(sys.argv[2])
honeypot_id = sys.argv[3]
ident = (sys.argv[4] if len(sys.argv) > 4 else "SSH-2.0-Paramiko_2.11.0") + "\r\n"

s = socket.create_connection((host, port), timeout=3)
# read the server banner (optional)
try:
    s.settimeout(1.0)
    banner = s.recv(128)
    sys.stderr.write(f"server banner: {banner!r}\n")
except Exception:
    pass

# send our fake client identification
s.sendall(ident.encode("ascii", "ignore"))
time.sleep(0.2)
s.close()
