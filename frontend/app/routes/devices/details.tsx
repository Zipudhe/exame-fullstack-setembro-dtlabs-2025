import { getDevice } from "~/lib/api"
import type { Route } from "./+types/details"
import type { DetailedDevice } from "types/device"

export async function clientLoader({ params: { deviceId } }: Route.ClientLoaderArgs): Promise<DetailedDevice | void> {
  return getDevice(deviceId)
    .then(({ data }) => data)
    .catch(error => {
      console.error({ error })
    })
}


export default function DeviceDetailsPage({ loaderData }: Route.ComponentProps) {
  console.log({ loaderData })
  return <h1> Device Details Page </h1>
}
