import { useContext, createContext, useState } from 'react'

export type NotificationType = "SUCCESS" | "ERROR"

type Notification = {
  notificationType: NotificationType,
  message: string
}

type INotificationContext = {
  dispatch: (notification: Notification) => void,
  clear: () => void,
  notification: Notification | null
}

const NotificationContext = createContext<INotificationContext>({} as INotificationContext)

export const NotificationProvider: React.FC<{ children: React.ReactNode }> = ({ children }) => {
  const [notification, setNotfication] = useState(null as Notification | null)
  const dismissNotification = () => {
    setNotfication(null)
  }
  const clearNotification = () => {
    console.log("Called clear notification")
    setTimeout(() => {
      console.log("dismissing notification")
      dismissNotification()
    }, 5000)
  }

  const dispatchNotification = (notification: Notification) => {
    console.log("Dispatching notification")
    setNotfication(notification)
    clearNotification()
  }

  const context = {
    clear: dismissNotification,
    dispatch: dispatchNotification,
    notification
  }

  return (
    <NotificationContext.Provider value={context} >
      {children}
    </NotificationContext.Provider>
  )

}

export const useNotification = () => {
  const context = useContext(NotificationContext)

  return context
}
