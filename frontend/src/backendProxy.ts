import type { HoneypotType, IncidentLogType } from "./types"
import { BACKEND_ROOT_URL } from './config';

export async function getHoneypots() {
    const res = await fetch(BACKEND_ROOT_URL + "/HoneyPots")
    const json = await res.json()
    return json as HoneypotType[]
}

export async function getIncidentLogs() {
    const res = await fetch(BACKEND_ROOT_URL + "/IncidentLogs")
    const json = await res.json()
    return json as IncidentLogType[]
}
