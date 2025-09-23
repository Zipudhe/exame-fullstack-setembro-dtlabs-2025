import { createContext } from 'react-router'

type UserContextType = {
  username: string
}

export const userContext = createContext<UserContextType | null>(null)
