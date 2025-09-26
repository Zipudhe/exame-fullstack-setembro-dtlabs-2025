import type { Route } from "./+types/device"

import { HomeIcon, ChartPieIcon } from "@heroicons/react/24/outline"
import type { IconType } from "types/external";
import { Outlet, NavLink } from "react-router";

export async function loader({ params }: Route.LoaderArgs) { } // get device statuses

type ActionsKeys = "home" | "graph"

type ActionsRecord = Record<ActionsKeys, { path: string, name: string, icon: IconType }>

export default function DeviceLayout({ loaderData, params }: Route.ComponentProps) {

  const actions: ActionsRecord = {
    home: { path: `/devices/${params.deviceId}`, name: "Home", icon: HomeIcon },
    graph: { path: `/devices/${params.deviceId}/graph`, name: "Graph", icon: ChartPieIcon }
  }

  return (
    <div className="flex w-full h-full gap-8">
      <div className="relative flex-1 h-[calc(100vh-20rem)] max-w-[20rem] flex-col border-r-2 bg-clip-border p-4 text-orange-200 w-min">
        <nav className="flex h-full min-w-[240px] flex-col gap-1 p-2 text-base font-normal items-center justify-center">
          {
            (Object.keys(actions) as ActionsKeys[]).map((action, key) => {
              const Icon = actions[action].icon
              return (
                <>
                  <NavLink
                    key={`action-${key}`}
                    to={actions[action].path}
                    className="cursor-pointer flex items-center p-3 leading-tight transition-all rounded-lg outline-none text-start hover:bg-blue-gray-50 hover:bg-opacity-80 hover:text-blue-gray-900 focus:bg-blue-gray-50 focus:bg-opacity-80 focus:text-blue-gray-900 active:bg-blue-gray-50 active:bg-opacity-80 active:text-blue-gray-900">
                    <div className="grid mr-4 place-items-center">
                      <Icon className="size-5 lg:size-8" />
                    </div>
                    {actions[action].name}
                  </NavLink>
                </>
              )
            })
          }
        </nav>
      </div>

      <Outlet />
      <article>
      </article>
    </div>
  )
}
