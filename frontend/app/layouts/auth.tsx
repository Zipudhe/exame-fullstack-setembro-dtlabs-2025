import { Outlet, redirect } from "react-router";
import type { Route } from "../+types/root";
import Navbar from "../components/navbar";

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
    <>
      <Navbar />
      <main className="p-8">
        <Outlet />
      </main>
    </>
  )
}

export default AuthenticatedLayout;
