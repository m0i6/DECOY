
## Files
- `honeypot.py`: TCP server that sends an SSH banner, reads up to `READ_LIMIT` bytes, classifies the client, and closes.
- `probe.py`: Tiny client that reads the server banner and sends a custom `SSH-2.0-...` identification line.


## Quick Start

### 1) Run the honeypot

```bash
export LISTEN_HOST=0.0.0.0
export LISTEN_PORT=2222
export CENTRAL_ALERT_URL="https://alerts.example.com/honeypot"   # or leave empty to skip POSTing
# optional:
export READ_TIMEOUT=3.0
export READ_LIMIT=1024
export MAX_CONN_PER_MIN=60
export TARPIT_SECONDS=0
export BANNER="SSH-2.0-OpenSSH_8.9p1 Ubuntu-3"
python3 honeypot.py
```

### 2) Use the probe

```bash
# usage: python3 probe.py <HOST> <PORT> "<SSH_IDENT>"
python3 probe.py 127.0.0.1 2222 "SSH-2.0-OpenSSH_9.6"
```

What you’ll see as the “attacker”: the server’s banner printed to stderr; then the connection closes.



## Probe “attacks” (what each simulates)

> All examples assume `<HOST>` is your honeypot and `<PORT>` is `LISTEN_PORT`.

| Probe command                                                                                                             | What it simulates (short)                  | Expected classification                                 | Severity |
| ------------------------------------------------------------------------------------------------------------------------- | ------------------------------------------ | ------------------------------------------------------- | ---------------- |
| `python3 probe.py <HOST> <PORT> "SSH-2.0-OpenSSH_9.6"`                                                                    | A normal OpenSSH client touching the port  | `OpenSSH / ssh_ident`                                   | moderate         |
| `python3 probe.py <HOST> <PORT> "SSH-2.0-Paramiko_2.11.0"`                                                                | Scripted/automation scanner using Paramiko | `Paramiko / ssh_ident`                                  | moderate         |
| `python3 probe.py <HOST> <PORT> "SSH-2.0-libssh_0.10.6"`                                                                  | Tools using libssh                         | `libssh / ssh_ident`                                    | moderate         |
| `python3 probe.py <HOST> <PORT> "SSH-2.0-libssh2_1.11.0"`                                                                 | Tools using libssh2                        | `libssh2 / ssh_ident`                                   | moderate         |
| `python3 probe.py <HOST> <PORT> "SSH-2.0-Go"`                                                                             | Go‑based SSH libraries/scanners            | `Go / ssh_ident`                                        | moderate         |
| `python3 probe.py <HOST> <PORT> "SSH-2.0-Nmap"`                                                                           | A scan that identifies as Nmap             | `Nmap / ssh_ident` (may add small delay)                | moderate         |
| `python3 probe.py <HOST> <PORT> "SSH-2.0-Test"`                                                                           | Generic/unknown SSH client string          | `generic / ssh_ident`                                   | moderate         |
| **Rate‑limit test:**<br>`for i in {1..80}; do python3 probe.py <HOST> <PORT> "SSH-2.0-Test" >/dev/null 2>&1 & done; wait` | Bursty scans from one IP                   | `family varies`, `rate_limited: true` if over threshold | **high**         |

**Client experience:** In all cases, the client first sees the honeypot’s SSH banner; the connection then closes shortly after the probe sends its identification line. No authentication is attempted or captured.


## Alerts & Logs

* Logs (stdout): one line per connection summarizing source, classification, bytes, and rate status.
* HTTP alert (if `CENTRAL_ALERT_URL` is set) includes:

  * `@timestamp`, `source.ip/port`, `destination.ip/port`
  * `ssh.client.ident`, `ssh.server.banner`
  * `classification.family/reason`, `network.bytes`
  * `rate.count_last_min`, `rate.rate_limited`
  * `severity` and `severity_number`


