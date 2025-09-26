import axios, { type AxiosResponse } from 'axios';
import type { DetailedDevice, UpdateDevice } from 'types/device'

const api = axios.create({
  baseURL: "http://localhost:8000/api",
  withCredentials: true
})

export type LoginData = {
  email: string,
  password: string
}

export const login = (payload: FormData) => {
  return api.post('/users/login', payload, {
    headers: {
      "Content-Type": "application/x-www-form-urlencoded"
    },
    withCredentials: true,
  })
}

export const logOut = () => {
  return api.delete('/users/logout', {
    withCredentials: true,
  })
}


export const getDevices = () => {
  return api.get("/devices")
}

export const getDevice = (device_id: string): Promise<AxiosResponse<DetailedDevice>> => {
  return api.get(`/devices/${device_id}`, {
    withCredentials: true,
  })
}

export const getDeviceStatus = (device_id: string) => {
  return api.get(`/devices/${device_id}/status`)
}

export const updateDevice = (device_id: string, payload: UpdateDevice) => {
  return api.put(`/devices/${device_id}`, payload, {
    withCredentials: true,
  })
}

export const deleteDevice = (device_id: string) => {
  return api.delete(`/devices/${device_id}`)
}

export const createDevice = (payload: FormData) => {
  return api.post('/devices', payload, {
    headers: {
      "Content-Type": "application/x-www-form-urlencoded"
    },
    withCredentials: true,
  })
}
