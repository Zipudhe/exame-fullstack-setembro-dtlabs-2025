import type { updateDevice } from "~/lib/api"

export type DeviceStatus = {
  cpu_usage: Number,
  ram_usage: Number,
  free_disk: Number,
  temperature: Number,
  conectivity: boolean,
  boot_date: Date
  created_at: Date
}

export type DeviceStatusSummary = {
  cpu_usage: Number,
  ram_usage: Number,
  temperature: Number,
}

export type Device = {
  id: string,
  name: string,
  location: string,
  sn: string,
  description: string,
  status?: DeviceStatus
}

export type UpdateDevice = Omit<Device, "id" | "status">

export type DetailedDevice = {
  id: string,
  name: string,
  location: string,
  sn: string,
  description: string,
  status: DeviceStatus[]
  created_at: Date,
  update_at: Date
}
