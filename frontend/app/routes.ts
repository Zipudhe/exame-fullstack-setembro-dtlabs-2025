import { type RouteConfig, index, route, layout, prefix } from "@react-router/dev/routes";

export default [
  layout("./layouts/auth.tsx", [
    index("routes/home.tsx"),

    ...prefix("devices", [
      index("routes/devices/home.tsx"),
      route(":deviceId", "routes/devices/details.tsx"),
      route("register", "routes/devices/register.tsx"),
    ]),

    ...prefix("notifications", [
      index("routes/notifications/home.tsx"),
      route(":deviceId", "routes/notifications/details.tsx"),
      route("register", "routes/notifications/register.tsx"),
    ]),
  ]),

  route("login", "routes/login.tsx"),
  route("register", "routes/register.tsx"),
] satisfies RouteConfig;
