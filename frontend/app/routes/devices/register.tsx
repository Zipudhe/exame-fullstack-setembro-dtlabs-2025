import { useForm } from 'react-hook-form'
import { useSubmit, useNavigate, redirect } from 'react-router'

import type { UpdateDevice } from "types/device"
import { createDevice } from '../../lib/api'
import type { Route } from './+types/register'

import Loading from '~/components/loading'
import Form from '~/components/deviceForm'

export async function clientAction({ request }: Route.ActionArgs) {
  const content = await request.formData()
  return await createDevice(content)
    .then(() => redirect("/"))
    .catch(err => {
      console.error({ err })
    })
}

export function HydrateFallback() {
  return <Loading />
}

export default function DeviceRegister() {
  const navigate = useNavigate()
  const submit = useSubmit()

  const defaultValues = {
    name: '',
    location: '',
    sn: '',
    description: '',
  } as UpdateDevice

  const methods = useForm({ defaultValues })
  const { register, formState: { isSubmitting } } = methods

  const handleCreate = async (data: UpdateDevice) => {
    await submit(data, { method: "post" })
  }

  return (
    <div className="w-full justify-center items-center flex">
      <Form
        methods={methods}
        submitHandler={handleCreate}
      >
        <div className="grid gap-4 mb-4 sm:grid-cols-2 sm:gap-6 sm:mb-5 w-full min-w-fit md:min-w-xl lg:min-w-4xl">
          <div className="sm:col-span-2">
            <label htmlFor="name" className="block mb-2 text-sm font-medium text-gray-900 dark:text-white">Nome do Dispositivo</label>
            <input
              className="disabled:cursor-not-allowed disabled:block disabled:text-gray-400 bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-primary-600 focus:border-primary-600 block w-full p-2.5 dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400 dark:text-white dark:focus:ring-primary-500 dark:focus:border-primary-500"
              disabled={isSubmitting}
              {...register('name')}
              type="text"
              name="name"
              id="name"
              placeholder="Digite o nome do dispositivo"
              required />
          </div>
          <div className="w-full">
            <label htmlFor="location" className="block mb-2 text-sm font-medium text-gray-900 dark:text-white">Localização</label>
            <input
              className="disabled:cursor-not-allowed disabled:block disabled:text-gray-400 bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-orange-600 focus:border-orange-600 block w-full p-2.5 dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400 dark:text-white dark:focus:ring-primary-500 dark:focus:border-primary-500"
              disabled={isSubmitting}
              {...register('location')}
              type="text"
              name="location"
              id="loc"
              placeholder="Localização"
              required />
          </div>
          <div className="w-full">
            <label htmlFor="sn" className="block mb-2 text-sm font-medium text-gray-900 dark:text-white">Numero Serial (Serial number)</label>
            <input
              className="disabled:cursor-not-allowed disabled:text-gray-400 bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-primary-600 focus:border-primary-600 block w-full p-2.5 dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400 dark:text-white dark:focus:ring-primary-500 dark:focus:border-primary-500"
              disabled={isSubmitting}
              {...register('sn')}
              type="text"
              name="sn"
              id="sn"
              placeholder="Digite o numero serial do dispositivo"
              required />
          </div>
          <div className="sm:col-span-2">
            <label htmlFor="description" className="block mb-2 text-sm font-medium text-gray-900 dark:text-white">Descrição</label>
            <textarea
              id="description"
              rows={3}
              {...register('description')}
              disabled={isSubmitting}
              className="disabled:cursor-not-allowed disabled:block disabled:text-gray-400 block p-2.5 w-full text-sm text-gray-900 bg-gray-50 rounded-lg border border-gray-300 focus:ring-primary-500 focus:border-primary-500 dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400 dark:text-white dark:focus:ring-primary-500 dark:focus:border-primary-500"
              placeholder="Escreva uma breve descrição para o produto"
            >
            </textarea>
          </div>
        </div>
        <div className="flex items-center space-x-4">
          <button
            className="text-white bg-green-600 hover:bg-green-700 focus:ring-4 focus:outline-none focus:ring-primary-300 font-medium rounded-lg text-sm px-5 py-2.5 text-center dark:bg-primary-600 dark:hover:bg-primary-700 dark:focus:ring-primary-800 disabled:bg-gray-700 disabled:border-none disabled:text-gray-600"
            type="submit"
            disabled={isSubmitting}
          >
            Adicionar +
          </button>
        </div>
      </Form>
    </div>
  )
}
