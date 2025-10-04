export async function getHoneypots() {
    const res = await fetch("http://127.0.0.1:5000/HoneyPots")
    const json = await res.json()
    return json
}

export async function getIncidentLogs() {
    const res = await fetch("http://127.0.0.1:5000/IncidentLogs")
    const json = await res.json()
    return json
}
