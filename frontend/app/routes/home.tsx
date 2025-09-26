import type { Route } from "./+types/home"
import { getDevices } from "../lib/api"
import { DeviceCard } from "../components/devicecard"
import Loading from "../components/loading"
import type { Device } from 'types/device'

import { PlusIcon } from '@heroicons/react/24/solid'

import { useNavigate } from 'react-router'

export async function clientLoader(): Promise<Device[]> {
  return await getDevices()
    .then(response => {
      if (response.data) {
        return response.data
      }
    })
    .catch(error => {
      console.error({ error })
    })
}

export function HydrateFallback() {
  return (
    <Loading />
  )
}

export default function Home({ loaderData }: Route.ComponentProps) {
  const navigate = useNavigate()
  return (
    <div className="relative w-full max-w-3/4 grid grid-cols-2 md:grid-cols-4 3xl:grid-cols-6 place-items-center gap-x-2 gap-y-4 overflow-scroll" >
      {
        loaderData && loaderData.map(device => <DeviceCard key={device.id} device={device} navigate={navigate} />)
      }
      <div
        onClick={() => navigate("/devices/register")}
        className="absolute bg-orange-400 cursor-pointer grid place-items-center rounded-full w-20 h-20 bottom-10 right-20 ">
        <PlusIcon className="size-12" />
      </div>
    </div>
  );
}
