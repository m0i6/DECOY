export interface HoneypotType {
    id: number,
    name: string,
    server_category: string,
    description: string,
    creation_date: string,
    status: string,
    geolocation: string,
    behaviors: string
}

export interface IncidentLogType {
    id: number,
    title: string,
    category: string,
    description: string,
    timestamp: string,
    severity: string,
    honeypot_id: number
}