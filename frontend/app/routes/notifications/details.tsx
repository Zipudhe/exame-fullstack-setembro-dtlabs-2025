import { useEffect, useState } from 'react'
import { useForm } from 'react-hook-form'
import { useSubmit, useNavigate, redirect } from 'react-router'

import type { threshHoldConfig, NotificationConfig, NotificationConfigPayload, threshHoldConfigFormData, WatchableKeys } from "types/notification"
import { deleteNotificationsConfig, getNotificationConfig, updateNotificationsConfig } from '../../lib/api'
import type { Route } from './+types/details'

import Loading from '~/components/loading'
import Form from '~/components/deviceForm'
import { TextInput } from '~/components/Input'
import { XCircleIcon, PencilIcon, TrashIcon } from '@heroicons/react/24/solid'

export async function clientAction({ request, params: { notificationId } }: Route.ActionArgs) {
  const formData = await request.formData()

  const form_keys = formData.get('watch_keys') as string
  const watch_keys = form_keys.split(',') as (keyof threshHoldConfig)[]

  const updatedThreshHold = {
    cpu_usage: parseInt(formData.get('cpu_usage') as string) || 0,
    ram_usage: parseInt(formData.get('ram_usage') as string) || 0,
    free_disk: parseInt(formData.get('free_disk') as string) || 0,
    temperature: parseFloat(formData.get('temperature') as string) || 0,
    latency: parseInt(formData.get('latency') as string) || 0,
    conectivity: formData.get('conectivity') === 'true',
    watch_keys
  }



  const updatedConfig = {
    threshHold: updatedThreshHold
  } as NotificationConfigPayload

  return await updateNotificationsConfig(notificationId, updatedConfig)

}

export async function clientLoader({ params }: Route.LoaderArgs): Promise<NotificationConfig | void> {
  return getNotificationConfig(params.notificationId)
    .then(response => response.data)
    .catch(err => {
      console.error({ err })
    })
}


export function HydrateFallback() {
  return <Loading />
}

export default function NotificationConfigDetailsPage({ loaderData, params }: Route.ComponentProps) {
  const [isEditing, setIsEditing] = useState(false)
  const navigate = useNavigate()
  const submit = useSubmit()

  if (!loaderData) {
    return <Loading />
  }

  const { threshHold } = loaderData

  useEffect(() => {
    loaderData && setIsEditing(false)
    reset(notificationDefaults)
  }, [threshHold])


  const notificationDefaults = {
    watch_keys: threshHold.watch_keys,
    cpu_usage: threshHold.cpu_usage,
    free_disk: threshHold.free_disk,
    conectivity: threshHold.conectivity,
    ram_usage: threshHold.ram_usage,
    temperature: threshHold.temperature,
    latency: threshHold.latency
  } as threshHoldConfigFormData

  const methods = useForm({ defaultValues: notificationDefaults })
  const { register, reset, setValue, getValues, watch, formState: { isDirty } } = methods

  const handleUpdate = async (data: threshHoldConfigFormData) => {
    if (!isDirty) {
      toggleEdit()
      return
    }

    await submit(data, { method: "put" })
      .then(() => toggleEdit())
      .catch(err => {
        console.error({ err })
      })
  }

  const handleDelete = async () => {
    toggleEdit()
    await deleteNotificationsConfig(params.notificationId)
      .then(() => {
        navigate("/")
      })
      .catch(err => {
        console.error({ err })
        toggleEdit()
      })
  }

  const toggleEdit = () => {
    isEditing && reset(notificationDefaults)
    setIsEditing((prevState) => !prevState)
  }

  const handleCheckboxClick = ({ currentTarget: { name } }: React.MouseEvent<HTMLInputElement>) => {

    let currentKeys = getValues("watch_keys")
    const index = currentKeys.indexOf(name)

    if (index == -1) {
      currentKeys = currentKeys.concat([name])
    } else {
      currentKeys.splice(index, 1)
    }


    setValue("watch_keys", currentKeys)
  }

  return (
    <div className="flex-1 flex-col justify-evenly relative w-full items-center flex">
      <h1 className="text-3xl" > Configuraçoes da Notificação </h1>
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
          <div className="flex flex-col items-start mb-4 gap-4">
            <label htmlFor={"cpu_usage"} className="block text-sm font-medium text-gray-900 dark:text-white">Uso de CPU</label>
            <div className="flex items-center gap-4" >
              <input
                className="w-6 h-6 text-blue-600 bg-gray-100 border-gray-300 rounded-sm focus:ring-blue-500 dark:focus:ring-blue-600 dark:ring-offset-gray-800 focus:ring-2 dark:bg-gray-700 dark:border-gray-600"
                id="cpu-checkbox"
                onClick={handleCheckboxClick}
                defaultChecked={watch("watch_keys")?.indexOf("cpu_usage") != -1}
                name="cpu_usage"
                type="checkbox"
                disabled={!isEditing}
              />
              <div className="sm:col-span-2 flex">
                <TextInput
                  id="cpu_usage"
                  disabled={!isEditing}
                  type="text"
                  {...register('cpu_usage')}
                  className="disabled:cursor-not-allowed disabled:block disabled:text-gray-400 bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-primary-600 focus:border-primary-600 block w-full p-2.5 dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400 dark:text-white dark:focus:ring-primary-500 dark:focus:border-primary-500"
                />
              </div>
            </div>
          </div>
          <div className="flex flex-col items-start mb-4 gap-4">
            <label htmlFor={"ram_usage"} className="block text-sm font-medium text-gray-900 dark:text-white">RAM Disponível</label>
            <div className="flex items-center gap-4" >
              <input
                className="w-6 h-6 text-blue-600 bg-gray-100 border-gray-300 rounded-sm focus:ring-blue-500 dark:focus:ring-blue-600 dark:ring-offset-gray-800 focus:ring-2 dark:bg-gray-700 dark:border-gray-600"
                disabled={!isEditing}
                defaultChecked={watch("watch_keys")?.indexOf("ram_usage") != -1}
                name="ram_usage"
                onClick={handleCheckboxClick}
                id="ram-checkbox"
                type="checkbox"
              />
              <div className="sm:col-span-2 flex">
                <TextInput
                  id="ram_usage"
                  type="text"
                  disabled={!isEditing}
                  {...register('ram_usage')}
                  className="disabled:cursor-not-allowed disabled:block disabled:text-gray-400 bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-primary-600 focus:border-primary-600 block w-full p-2.5 dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400 dark:text-white dark:focus:ring-primary-500 dark:focus:border-primary-500"
                />
              </div>
            </div>
          </div>
          <div className="flex flex-col items-start mb-4 gap-4">
            <label htmlFor={"free_disk"} className="block text-sm font-medium text-gray-900 dark:text-white">Uso de armazenamento</label>
            <div className="flex items-center gap-4" >
              <input
                className="w-6 h-6 text-blue-600 bg-gray-100 border-gray-300 rounded-sm focus:ring-blue-500 dark:focus:ring-blue-600 dark:ring-offset-gray-800 focus:ring-2 dark:bg-gray-700 dark:border-gray-600"
                id="disk-checkbox"
                defaultChecked={watch("watch_keys")?.indexOf("free_disk") != -1}
                name="free_disk"
                onClick={handleCheckboxClick}
                disabled={!isEditing}
                type="checkbox"
              />
              <div className="sm:col-span-2 flex">
                <TextInput
                  id="free_disk"
                  type="text"
                  disabled={!isEditing}
                  {...register('free_disk')}
                  className="disabled:cursor-not-allowed disabled:block disabled:text-gray-400 bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-primary-600 focus:border-primary-600 block w-full p-2.5 dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400 dark:text-white dark:focus:ring-primary-500 dark:focus:border-primary-500"
                />
              </div>
            </div>
          </div>
          <div className="flex flex-col items-start mb-4 gap-4">
            <label htmlFor={"temperature"} className="block text-sm font-medium text-gray-900 dark:text-white">Temperatura</label>
            <div className="flex items-center gap-4" >
              <input
                className="w-6 h-6 text-blue-600 bg-gray-100 border-gray-300 rounded-sm focus:ring-blue-500 dark:focus:ring-blue-600 dark:ring-offset-gray-800 focus:ring-2 dark:bg-gray-700 dark:border-gray-600"
                disabled={!isEditing}
                defaultChecked={watch("watch_keys")?.indexOf("temperature") != -1}
                name="temperature"
                onClick={handleCheckboxClick}
                id="temperature-checkbox"
                type="checkbox"
              />
              <div className="sm:col-span-2 flex">
                <TextInput
                  id="temperature"
                  disabled={!isEditing}
                  type="text"
                  {...register('temperature')}
                  className="disabled:cursor-not-allowed disabled:block disabled:text-gray-400 bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-primary-600 focus:border-primary-600 block w-full p-2.5 dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400 dark:text-white dark:focus:ring-primary-500 dark:focus:border-primary-500"
                />
              </div>
            </div>
          </div>
          <div className="flex flex-col items-start mb-4 gap-4">
            <label htmlFor={"conectivity"} className="block text-sm font-medium text-gray-900 dark:text-white">Conexão</label>
            <div className="flex items-center gap-4" >
              <input
                className="w-6 h-6 text-blue-600 bg-gray-100 border-gray-300 rounded-sm focus:ring-blue-500 dark:focus:ring-blue-600 dark:ring-offset-gray-800 focus:ring-2 dark:bg-gray-700 dark:border-gray-600"
                name="conectivity"
                disabled={!isEditing}
                defaultChecked={watch("watch_keys")?.indexOf("conectivity") != -1}
                onClick={handleCheckboxClick}
                id="conectivity-checkbox"
                type="checkbox"
              />
              <div className="sm:col-span-2 flex">
                <TextInput
                  id="conectivity"
                  disabled={!isEditing}
                  type="text"
                  {...register('conectivity')}
                  className="disabled:cursor-not-allowed disabled:block disabled:text-gray-400 bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-primary-600 focus:border-primary-600 block w-full p-2.5 dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400 dark:text-white dark:focus:ring-primary-500 dark:focus:border-primary-500"
                />
              </div>
            </div>
          </div>
          <div className="flex flex-col items-start mb-4 gap-4">
            <label htmlFor={"latency"} className="block text-sm font-medium text-gray-900 dark:text-white">Latência</label>
            <div className="flex items-center gap-4" >
              <input
                className="w-6 h-6 text-blue-600 bg-gray-100 border-gray-300 rounded-sm focus:ring-blue-500 dark:focus:ring-blue-600 dark:ring-offset-gray-800 focus:ring-2 dark:bg-gray-700 dark:border-gray-600"
                disabled={!isEditing}
                name="latency"
                id="latencia-checkbox"
                defaultChecked={watch("watch_keys")?.indexOf("latency") != -1}
                onClick={handleCheckboxClick}
                type="checkbox"
              />
              <div className="sm:col-span-2 flex">
                <TextInput
                  id="latency"
                  disabled={!isEditing}
                  type="text"
                  {...register('latency')}
                  className="disabled:cursor-not-allowed disabled:block disabled:text-gray-400 bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-primary-600 focus:border-primary-600 block w-full p-2.5 dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400 dark:text-white dark:focus:ring-primary-500 dark:focus:border-primary-500"
                />
              </div>
            </div>
          </div>
        </div>

        <div className="flex items-center space-x-4">
          <button
            className="text-white bg-green-600 hover:bg-green-700 focus:ring-4 focus:outline-none focus:ring-primary-300 font-medium rounded-lg text-sm px-5 py-2.5 text-center dark:bg-primary-600 dark:hover:bg-primary-700 dark:focus:ring-primary-800 disabled:bg-gray-700 disabled:border-none disabled:text-gray-600"
            type="submit"
            disabled={!isEditing}
          >
            Salvar
          </button>
          <button
            className="text-red-600 inline-flex items-center hover:text-white border border-red-600 hover:bg-red-600 focus:ring-4 focus:outline-none focus:ring-red-300 font-medium rounded-lg text-sm px-5 py-2.5 text-center disabled:bg-gray-700 disabled:border-none disabled:text-gray-600"
            type="button"
            onClick={handleDelete}
            disabled={!isEditing}
          >
            <TrashIcon className="size-5 mr-1" />
            Remover
          </button>
        </div>

      </Form>
    </div>
  )
}
