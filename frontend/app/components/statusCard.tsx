import {
  CpuChipIcon,
  ChartPieIcon,
  SunIcon
} from "@heroicons/react/24/solid"

import type { DeviceStatusSummary } from 'types/device'
import type { IconType } from "types/external";

type summaryMetricsKeys = "cpu_usage" | "ram_usage" | "temperature"


const icons: Record<summaryMetricsKeys, IconType> = {
  cpu_usage: CpuChipIcon,
  ram_usage: ChartPieIcon,
  temperature: SunIcon
}


const summaryKeys: Record<summaryMetricsKeys, { sufix: string, description: string }> = {
  cpu_usage: { sufix: "%", description: "CPU usage" },
  ram_usage: { sufix: "%", description: "RAM usage" },
  temperature: { sufix: "°C", description: "Temperature" },
}


export const StatusCard = (status: DeviceStatusSummary) => {

  return (
    <div className="lg:w-min w-full max-w-2xs p-4 bg-white border border-gray-200 rounded-lg shadow-sm sm:p-4 dark:bg-gray-800 dark:border-gray-700 cursor-pointer">
      <ul className="my-4 space-y-3">
        {
          (Object.keys(summaryKeys) as summaryMetricsKeys[]).map(key => {
            const Icon = icons[key]
            const description = status[key] + " " + summaryKeys[key].sufix

            return (
              <li>
                <div className="flex items-center p-3 text-base font-bold text-gray-900 rounded-lg bg-gray-50 hover:bg-gray-100 group hover:shadow dark:bg-gray-600 dark:hover:bg-gray-500 dark:text-white">
                  <Icon className="lg:size-6 size-4" />
                  <span className="flex-1 ms-3 whitespace-nowrap">{description}</span>
                  <span className="inline-flex items-center justify-center px-2 py-0.5 ms-3 text-xs font-medium text-gray-500 bg-gray-200 rounded-sm dark:bg-gray-700 dark:text-gray-400">{summaryKeys[key].description}</span>
                </div>
              </li>
            )
          })
        }
      </ul>
    </div>
  )
}

export const StatusCardSkeleton = () => {
  return (
    <div role="status" className="max-w-sm animate-pulse">
      <div className="w-full max-w-2xs p-4 bg-white border border-gray-200 rounded-lg shadow-sm sm:p-6 dark:bg-gray-800 dark:border-gray-700 cursor-pointer" />
      <div className="w-full max-w-2xs p-4 bg-white border border-gray-200 rounded-lg shadow-sm sm:p-6 dark:bg-gray-800 dark:border-gray-700 cursor-pointer" />
      <div className="w-full max-w-2xs p-4 bg-white border border-gray-200 rounded-lg shadow-sm sm:p-6 dark:bg-gray-800 dark:border-gray-700 cursor-pointer" />
      <span className="sr-only">Loading...</span>
    </div>
  )
}
