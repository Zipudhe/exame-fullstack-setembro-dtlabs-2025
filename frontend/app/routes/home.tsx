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
    <div className="flex flex-1 flex-col justify-evenly items-center" >
      <h1 className="text-3xl" > Dispositivos </h1>
      <div className="w-full grid grid-cols-1 md:grid-cols-3 lg:grid-cols-5 auto-cols-min place-items-center gap-x-4" >
        {
          loaderData && loaderData.map(device => <DeviceCard key={device.id} device={device} navigate={navigate} />)
        }
        <div
          onClick={() => navigate("/devices/register")}
          className="absolute bg-orange-400 cursor-pointer grid place-items-center rounded-full w-20 h-20 bottom-20 right-20 ">
          <PlusIcon className="size-12" />
        </div>
      </div>
    </div>
  );
}
