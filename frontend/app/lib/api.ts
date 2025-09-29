import axios from 'axios';
import type { DetailedDevice, UpdateDevice } from 'types/device'
import type { NotificationConfig, NotificationConfigPayload, threshHoldConfig } from 'types/notification'

const api = axios.create({
  baseURL: "http://localhost:8000/api",
  withCredentials: true
})

const deviceBaseUrl = "/devices"
const notificationsBaseUrl = "/notifications"

export type LoginData = {
  email: string,
  password: string
}

export const login = (payload: FormData) => {
  return api.post('/users/login', payload, {
    headers: {
      "Content-Type": "application/x-www-form-urlencoded"
    }
  })
}

export const logOut = () => {
  return api.delete('/users/logout')
}


export const getDevices = () => {
  return api.get(deviceBaseUrl)
}

export const getDevice = (device_id: string) => {
  return api.get<DetailedDevice>(`${deviceBaseUrl}/${device_id}`)
}

export const getDeviceStatus = (device_id: string) => {
  return api.get(`${deviceBaseUrl}/${device_id}/status`)
}

export const updateDevice = (device_id: string, payload: UpdateDevice) => {
  return api.put(`/${deviceBaseUrl}/${device_id}`, payload)
}

export const deleteDevice = (device_id: string) => {
  return api.delete(`${deviceBaseUrl}/${device_id}`)
}

export const createDevice = (payload: FormData) => {
  return api.post(deviceBaseUrl, payload, {
    headers: {
      "Content-Type": "application/x-www-form-urlencoded"
    }
  })
}

export const getNotificationsConfig = () => {
  return api.get<NotificationConfig[]>(`${notificationsBaseUrl}/config`)
}

export const createNotificationsConfig = (payload: threshHoldConfig) => {
  return api.post(`${notificationsBaseUrl}/config`, payload, {
    headers: {
      'Content-Type': 'application/json'
    }
  })
}

export const updateNotificationsConfig = (notificationId: string, payload: NotificationConfigPayload) => {
  return api.put(`${notificationsBaseUrl}/config/${notificationId}`, payload, { headers: { 'Content-Type': 'application/json' } })
}

export const deleteNotificationsConfig = (notificationId: string) => {
  return api.delete(`${notificationsBaseUrl}/config/${notificationId}`)
}

export const getNotificationConfig = (notificationId: string) => {
  return api.get<NotificationConfig>(`${notificationsBaseUrl}/config/${notificationId}`)
}
