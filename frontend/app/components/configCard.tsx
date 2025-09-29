import {
  CpuChipIcon,
  ChartPieIcon,
  SunIcon,
  GlobeAltIcon,
  CircleStackIcon
} from "@heroicons/react/24/solid"
import { type NavigateFunction } from "react-router";

import type { IconType } from 'types/external'
import type { NotificationConfig } from "types/notification";

type watchingKeys = "cpu_usage" | "ram_usage" | "free_disk" | "temperature" | "conectivity"

const icons: Record<watchingKeys, IconType> = {
  cpu_usage: CpuChipIcon,
  free_disk: CircleStackIcon,
  conectivity: GlobeAltIcon,
  ram_usage: ChartPieIcon,
  temperature: SunIcon
}


const summaryKeys: Record<watchingKeys, { sufix: string, description: string }> = {
  cpu_usage: { sufix: "%", description: "CPU usage" },
  ram_usage: { sufix: "%", description: "RAM usage" },
  temperature: { sufix: "°C", description: "Temperature" },
  free_disk: { sufix: "%", description: "Armazenamento" },
  conectivity: { sufix: "", description: "Conexão" },
}

interface INotificationCard {
  notificationConfig: NotificationConfig,
  navigate: NavigateFunction
}

export const NotificationConfigCard: React.FC<INotificationCard> = ({ notificationConfig, navigate }) => {

  const handleClick = () => navigate(`/notifications/${notificationConfig.id}`, { state: notificationConfig })

  return (
    <div
      onClick={handleClick}
      className="w-max max-h-min max-w-2xs p-4 bg-white border border-gray-200 rounded-lg shadow-sm sm:p-6 dark:bg-gray-800 dark:border-gray-700 cursor-pointer">
      <h5 className="mb-3 text-base font-semibold text-gray-900 md:text-xl dark:text-white">
        Limites Configurados
      </h5>
      <ul className="my-4 space-y-3">
        {
          (Object.keys(summaryKeys) as watchingKeys[]).map((key, index) => {
            const Icon = icons[key]
            const threshHold = `${notificationConfig.threshHold[key]} ${summaryKeys[key].sufix}`

            if (!notificationConfig.threshHold[key]) {
              return
            }

            return (
              <li key={`card-item-${index}-${notificationConfig.id}`}>
                <div className="flex items-center p-3 text-base font-bold text-gray-900 rounded-lg bg-gray-50 hover:bg-gray-100 group hover:shadow dark:bg-gray-600 dark:hover:bg-gray-500 dark:text-white">
                  <Icon className="lg:size-6 size-4" />
                  <span className="flex-1 ms-3 whitespace-nowrap">{threshHold}</span>
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
