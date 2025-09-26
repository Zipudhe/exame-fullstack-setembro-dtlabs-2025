import type { Route } from "./+types/device"

import { HomeIcon, ChartPieIcon } from "@heroicons/react/24/outline"
import type { IconType } from "types/external";
import { Outlet, NavLink } from "react-router";

import { getDeviceStatus } from '../lib/api'
import StatusFeed from "~/components/statusFeed";

type ActionsKeys = "home" | "graph"

type ActionsRecord = Record<ActionsKeys, { path: string, name: string, icon: IconType }>

export async function clientLoader({ params: { deviceId } }: Route.LoaderArgs) {
  const device_status = await getDeviceStatus(deviceId).then(res => res.data).catch(err => console.error({ err }))

  return { device_status }
}

const SideBarMenu: React.FC<{ deviceId: string }> = ({ deviceId }) => {
  const actions: ActionsRecord = {
    home: { path: `/devices/${deviceId}`, name: "Device", icon: HomeIcon },
    graph: { path: `/devices/${deviceId}/graph`, name: "Graph", icon: ChartPieIcon }
  }

  return (
    <div className="relative flex-1 h-full max-w-[10rem] flex-col border-r-1 border-r-orange-100 bg-clip-border p-4 text-orange-200 ">
      <nav className="flex h-full flex-col gap-1 p-2 text-base font-normal items-center justify-center">
        {
          (Object.keys(actions) as ActionsKeys[]).map((action, key) => {
            const Icon = actions[action].icon
            return (
              <div key={`action-${key}`}>
                <NavLink
                  to={actions[action].path}
                  className="cursor-pointer flex items-center p-3 leading-tight transition-all rounded-lg outline-none text-start hover:bg-blue-gray-50 hover:bg-opacity-80 hover:text-blue-gray-900 focus:bg-blue-gray-50 focus:bg-opacity-80 focus:text-blue-gray-900 active:bg-blue-gray-50 active:bg-opacity-80 active:text-blue-gray-900">
                  <div className="grid mr-4 place-items-center">
                    <Icon className="size-5 lg:size-8" />
                  </div>
                  {actions[action].name}
                </NavLink>
              </div>
            )
          })
        }
      </nav>
    </div>

  )
}

export default function DeviceLayout({ loaderData, params }: Route.ComponentProps) {
  const { device_status } = loaderData

  return (
    <div className="flex w-full h-full gap-8 lg:gap-10">
      <SideBarMenu deviceId={params.deviceId} />
      <Outlet />
      <StatusFeed status={device_status} />
    </div>
  )
}
