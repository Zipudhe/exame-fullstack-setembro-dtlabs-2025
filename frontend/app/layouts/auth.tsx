import { Outlet, redirect } from "react-router";
import type { Route } from "../+types/root";
import Navbar from "../components/navbar";
import NotificationCard from "../components/notificationCard";
import { NotificationProvider } from '../context/notificationContext'

export async function loader() {
  return null
}

// Server side middleware
function authMiddleware({ request, context }: { request: Request, context: any }) {
  const cookies = request.headers.get("Cookie") || ""

  if (!cookies) {
    throw redirect('/login')
  }

  const session_id = cookies.split("; ").find(c => c.startsWith("session_id="))?.split("=")[1]

  if (!session_id) {
    throw redirect('/login')
  }
}

export const middleware: Route.MiddlewareFunction[] = [authMiddleware]

function AuthenticatedLayout() {
  return (
    <NotificationProvider>
      <NotificationCard />
      <Navbar />
      <main className="p-6 flex flex-1 flex-col justify-center items-center max-h[calc(100vh-80px)] overflow-hidden">
        <Outlet />
      </main>
    </NotificationProvider>
  )
}

export default AuthenticatedLayout;
