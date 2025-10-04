import type { HoneypotType, IncidentLogType } from "./types"

export async function getHoneypots() {
    const res = await fetch("api/HoneyPots")
    const json = await res.json()
    return json as HoneypotType[]
}

export async function getIncidentLogs() {
    const res = await fetch("api/IncidentLogs")
    const json = await res.json()
    return json as IncidentLogType[]
}
