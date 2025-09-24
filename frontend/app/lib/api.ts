import axios from 'axios';

const api = axios.create({
  baseURL: "http://localhost:8000/api",
  withCredentials: true
})

export type LoginData = {
  email: string,
  password: string
}

export const login = (payload: FormData) => {
  return api.post('/users/login', payload, {
    headers: {
      "Content-Type": "application/x-www-form-urlencoded"
    },
    withCredentials: true,
  })
}

export const logOut = () => {
  return api.post('/users/logout', { withCredentias: true })
}

