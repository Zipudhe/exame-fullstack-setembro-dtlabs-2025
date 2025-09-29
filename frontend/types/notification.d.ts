export type WatchableKeys = {
  cpu_usage: number,
  ram_usage: number,
  free_disk: number,
  conectivity: boolean
  latency: number,
  temperature: number
}

export type DeviceKeys = keyof typeof WatchableKeys

export type threshHoldConfig = WatchableKeys & {
  watch_keys: DeviceKeys[],
}

export type threshHoldConfigFormData = WatchableKeys & {
  watch_keys: string[]
}

export type NotificationConfig = {
  id: string,
  threshHold: threshHoldConfig,
  created_at: Date,
  update_at: Date,
}

export type NotificationConfigPayload = Omit<NotificationConfig, "id" | "created_at" | "update_at">
