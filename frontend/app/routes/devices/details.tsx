import { useState, useEffect } from 'react'
import { useForm } from 'react-hook-form'
import { useSubmit, useNavigate } from 'react-router'
import { TrashIcon, PencilIcon, XCircleIcon } from '@heroicons/react/24/outline'

import type { DetailedDevice, Device, UpdateDevice } from "types/device"
import { deleteDevice, getDevice, updateDevice } from '../../lib/api'
import type { Route } from './+types/details'
import Loading from '~/components/loading'
import Form from '~/components/deviceForm'
import { useNotification } from '../../context/notificationContext'

export async function clientLoader({ params }: Route.LoaderArgs): Promise<DetailedDevice | void> {
  return getDevice(params.deviceId)
    .then(response => response.data)
    .catch(err => {
      console.error({ err })
    })
}

export async function clientAction({ request, params: { deviceId } }: Route.ActionArgs) {
  const content = Object.fromEntries(await request.formData()) as UpdateDevice
  await updateDevice(deviceId, content)
    .catch(err => {
      console.error({ err })
    })
  return
}

export function HydrateFallback() {
  return <Loading />
}

export default function DeviceDetailsPage({ loaderData }: Route.ComponentProps) {
  const navigate = useNavigate()
  const { dispatch } = useNotification()
  const submit = useSubmit()

  if (!loaderData) {
    return <Loading />
  }


  const deviceSummary = {
    id: loaderData.id,
    name: loaderData.name,
    location: loaderData.location,
    sn: loaderData.sn,
    description: loaderData.description,
  } as Device

  const [isEditing, setIsEditing] = useState(false)
  const methods = useForm({ defaultValues: deviceSummary })
  const { register, reset, formState: { isSubmitting, isDirty } } = methods

  useEffect(() => {
    loaderData && setIsEditing(false)
  }, [loaderData])


  const handleUpdate = async (data: UpdateDevice) => {
    if (!isDirty) {
      toggleEdit()
      return
    }

    await submit(data, { method: "put" })
      .catch(() => toggleEdit())
  }

  const handleDelete = async () => {
    toggleEdit()
    await deleteDevice(deviceSummary.id)
      .then(() => {
        dispatch({ message: "Dispositivo removido com sucesso", notificationType: "SUCCESS" })
        navigate("/")
      })
      .catch(err => {
        dispatch({ message: "Falha ao remover dispositivo", notificationType: "SUCCESS" })
        toggleEdit()
      })
  }
  const toggleEdit = () => {
    isEditing && reset(deviceSummary)
    setIsEditing((prevState) => !prevState)
  }

  const disabled = isSubmitting || !isEditing

  return (
    <div className="flex-1 flex-col justify-evenly relative w-full items-center flex">
      <h1 className="text-3xl" > Detalhes do Dispositivo </h1>
      <button
        onClick={toggleEdit}
        className="absolute top-0 right-4 p-2 rounded-full text-gray-300 hover:bg-gray-700 hover:text-white transition-colors"
        aria-label="Edit form"
      >
        {
          isEditing ?
            <XCircleIcon className="size-5" /> :
            <PencilIcon className="size-5" />
        }
      </button>
      <Form
        methods={methods}
        submitHandler={handleUpdate}
      >
        <div className="grid gap-4 mb-4 sm:grid-cols-2 sm:gap-6 sm:mb-5 w-full min-w-fit md:min-w-xl lg:min-w-4xl">
          <div className="sm:col-span-2">
            <label htmlFor="name" className="block mb-2 text-sm font-medium text-gray-900 dark:text-white">Nome do Dispositivo</label>
            <input
              className="disabled:cursor-not-allowed disabled:block disabled:text-gray-400 bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-primary-600 focus:border-primary-600 block w-full p-2.5 dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400 dark:text-white dark:focus:ring-primary-500 dark:focus:border-primary-500"
              disabled={disabled}
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
              disabled={disabled}
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
              disabled={disabled}
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
              disabled={disabled}
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
            disabled={disabled}
          >
            Salvar
          </button>
          <button
            className="text-red-600 inline-flex items-center hover:text-white border border-red-600 hover:bg-red-600 focus:ring-4 focus:outline-none focus:ring-red-300 font-medium rounded-lg text-sm px-5 py-2.5 text-center disabled:bg-gray-700 disabled:border-none disabled:text-gray-600"
            disabled={disabled}
            type="button"
            onClick={handleDelete}
          >
            <TrashIcon className="size-5 mr-1" />
            Remover
          </button>
        </div>

      </Form>
    </div>
  )
}
