import { useNavigate } from 'react-router'
import type { Route } from "./+types/home"
import { getNotificationsConfig } from "~/lib/api"

import Loading from "~/components/loading"
import { NotificationConfigCard } from "~/components/configCard"
import { PlusIcon } from "@heroicons/react/24/solid"

export async function clientLoader() {
  const notifications = await getNotificationsConfig().then(res => res.data)

  return { notifications }
}

export function HydrateFallback() {
  return <Loading />
}

export const NotificationsPage = ({ loaderData }: Route.ComponentProps) => {
  const navigate = useNavigate()
  const { notifications } = loaderData

  if (!notifications) {
    return (
      <h1> No Notifications found... </h1>
    )
  }

  return (
    <div className="flex flex-1 flex-col justify-evenly items-center">
      <h1 className="text-3xl" > Notificações </h1>
      <div className="flex-1 grid grid-cols-4 place-items-center gap-3" >
        {
          notifications.map(notification => (
            <NotificationConfigCard notificationConfig={notification} navigate={navigate} />
          ))
        }
        <div
          onClick={() => navigate("/notifications/register")}
          className="absolute bg-orange-400 cursor-pointer grid place-items-center rounded-full w-20 h-20 bottom-20 right-20 ">
          <PlusIcon className="size-12" />
        </div>
      </div>
    </div>
  )

}

export default NotificationsPage
