import { useNotification } from '../context/notificationContext'
import { CheckCircleIcon, XCircleIcon } from '@heroicons/react/24/outline'

const SuccessNotification = ({ message }: { message: string }) => (
  <div
    className="border-green-500 text-green-500 border absolute right-10 top-15 flex w-full max-w-xs space-x-4 rounded-xl bg-gray-700 p-4 shadow rtl:space-x-reverse rtl:divide-x-reverse space-x mx-2"
  >
    <CheckCircleIcon className="size-6" />
    <div className="ps-4 text-sm font-normal">{message}</div>
  </div>
)

const ErrorNotificaiton = ({ message }: { message: string }) => (
  <div
    className="border-red-500 text-red-500 border absolute right-10 top-15 flex w-full max-w-xs space-x-4 divide-x rounded-xl bg-gray-700 p-4 shadow rtl:space-x-reverse rtl:divide-x-reverse space-x mx-2"
  >
    <XCircleIcon className="size-6" />
    <div className="ps-4 text-sm font-normal">
      {message}
    </div>
  </div>
)

export const NotificationCard = () => {
  const { notification } = useNotification()

  if (notification) {
    return notification.notificationType == "SUCCESS" ?
      <SuccessNotification message={notification.message} />
      :
      <ErrorNotificaiton message={notification.message} />
  }

  return
}

export default NotificationCard
