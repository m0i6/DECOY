export async function getHoneypots() {
    const res = await fetch("http://localhost:5000/HoneyPots")
    const json = await res.json()
    return json
}

export async function getIncidentLogs() {
    const res = await fetch("http://localhost:5000/IncidentLogs")
    const json = await res.json()
    return json
}
