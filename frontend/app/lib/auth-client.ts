import { createAuthClient } from 'better-auth/react'

const serverUrl = process.env.AUTH_SERVER_URL ?? 'http://localhost:8000'
export const authClient = createAuthClient({ baseURL: serverUrl })
