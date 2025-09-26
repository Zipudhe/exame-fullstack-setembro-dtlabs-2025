'use client'

import { useState } from 'react'
import { NavLink, redirect } from 'react-router'
import {
  Dialog,
  DialogPanel,
  PopoverGroup,
} from '@headlessui/react'
import {
  Bars3Icon,
  ArrowLeftStartOnRectangleIcon,
  XMarkIcon,
} from '@heroicons/react/24/outline'

import { logOut } from '../lib/api'

const links = [
  { href: "/", name: "Tela Inicial" },
  { href: "/devices", name: "Dispositivos" },
  { href: "/notifications", name: "Notificações" },
]

function Navbar() {
  const [mobileMenuOpen, setMobileMenuOpen] = useState(false)

  const handleLogout = () => {
    logOut()
      .then(() => {
        return redirect('/login')
      })
      .catch(err => {
        console.error(err)
      })
  }

  return (
    <header className="bg-gray-900">
      <nav aria-label="Global" className="mx-auto flex max-w-7xl items-center justify-between p-6 lg:px-8">
        <div className="flex lg:flex-1">
          <NavLink to="/" className="-m-1.5 p-1.5">
            <span className="sr-only">Exame dt labs</span>
            <img
              alt="dtlabs logo"
              src="/dtlabs.svg"
              className="h-8 w-auto"
            />
          </NavLink>
        </div>
        <div className="flex lg:hidden">
          <button
            type="button"
            onClick={() => setMobileMenuOpen(true)}
            className="-m-2.5 inline-flex items-center justify-center rounded-md p-2.5 text-gray-700 dark:text-gray-400"
          >
            <span className="sr-only">Open main menu</span>
            <Bars3Icon aria-hidden="true" className="size-6" />
          </button>
        </div>
        <PopoverGroup className="hidden lg:flex lg:gap-x-12">
          {
            links.map(({ href, name }) => (
              <NavLink to={href} key={name} className="text-sm/6 font-semibold text-white decoration-orange-500 hover:underline">
                {name}
              </NavLink>
            ))
          }
        </PopoverGroup>
        <div className="hidden lg:flex lg:flex-1 lg:justify-end lg:items-center lg:gap-x-4 lg:cursor-pointer">
          <button
            onClick={handleLogout}
            className="text-sm/6 font-semibold text-white cursor-pointer">
            Log out
          </button>
          <ArrowLeftStartOnRectangleIcon aria-hidden="true" className="size-6" />
        </div>
      </nav>
      <Dialog open={mobileMenuOpen} onClose={setMobileMenuOpen} className="lg:hidden">
        <div className="fixed inset-0 z-50" />
        <DialogPanel className="fixed inset-y-0 right-0 z-50 w-full overflow-y-auto bg-gray-900 p-6 sm:max-w-sm sm:ring-1 sm:ring-gray-100/10">
          <div className="flex items-center justify-between">
            <a href="#" className="-m-1.5 p-1.5">
              <span className="sr-only">Exame dt labs</span>
              <img
                alt="company log"
                src="/dtlabs.svg"
                className="h-8 w-auto"
              />
            </a>
            <button
              type="button"
              onClick={() => setMobileMenuOpen(false)}
              className="-m-2.5 rounded-md p-2.5 text-gray-400"
            >
              <span className="sr-only">Close menu</span>
              <XMarkIcon aria-hidden="true" className="size-6" />
            </button>
          </div>
          <div className="mt-6 flow-root">
            <div className="-my-6 divide-y divide-white/10">
              <div className="space-y-2 py-6">
                {
                  links.map(({ href, name }) => (
                    <NavLink to={href} key={name}
                      className="-mx-3 block rounded-lg px-3 py-2 text-base/7 font-semibold text-gray-900 hover:bg-gray-50 dark:text-white dark:hover:bg-white/5">
                      {name}
                    </NavLink>
                  ))
                }
              </div>
              <div className="py-6">
                <button
                  onClick={handleLogout}
                  className=" items-center flex gap-x-2 -mx-3 w-fit-content rounded-lg px-3 py-2.5 text-base/7 font-semibold text-white hover:bg-white/5"
                >
                  <ArrowLeftStartOnRectangleIcon aria-hidden="true" className="size-4" />
                  Log in
                </button>
              </div>
            </div>
          </div>
        </DialogPanel>
      </Dialog>
    </header>
  )
}


export default Navbar;
