import { useForm } from 'react-hook-form'
import { useSubmit, useNavigate } from 'react-router'

import type { NotificationConfigPayload, threshHoldConfigFormData, threshHoldConfig } from "types/notification"
import { createNotificationsConfig } from '../../lib/api'
import type { Route } from './+types/register'
import Form from '~/components/deviceForm'
import { TextInput } from '~/components/Input'

export async function clientAction({ request }: Route.ActionArgs) {
  const formData = await request.formData()

  const form_keys = formData.get('watch_keys') as string
  const watch_keys = form_keys.split(',') as (keyof threshHoldConfig)[]

  const threshHold = {
    cpu_usage: parseInt(formData.get('cpu_usage') as string) || 0,
    ram_usage: parseInt(formData.get('ram_usage') as string) || 0,
    free_disk: parseInt(formData.get('free_disk') as string) || 0,
    temperature: parseFloat(formData.get('temperature') as string) || 0,
    latency: parseInt(formData.get('latency') as string) || 0,
    conectivity: formData.get('conectivity') === 'true',
    watch_keys
  }

  return createNotificationsConfig(threshHold)
}


export default function NotificationConfigRegisterPage() {
  const navigate = useNavigate()
  const submit = useSubmit()


  const notificationDefaults = {
    watch_keys: [],
    cpu_usage: 0,
    free_disk: 0,
    conectivity: false,
    ram_usage: 0,
    temperature: 0,
    latency: 0
  } as threshHoldConfigFormData


  const methods = useForm({ defaultValues: notificationDefaults })
  const { register, setValue, getValues, watch } = methods

  const handleCreate = async (data: threshHoldConfigFormData) => {

    await submit(data, { method: "post" })
      .then(() => navigate('/notifications'))
      .catch(err => {
        console.error({ err })
      })

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
      <h1 className="text-3xl" > Nova Configuração da Notificação </h1>
      <Form
        methods={methods}
        submitHandler={handleCreate}
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
              />
              <div className="sm:col-span-2 flex">
                <TextInput
                  id="cpu_usage"
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
                type="checkbox"
              />
              <div className="sm:col-span-2 flex">
                <TextInput
                  id="free_disk"
                  type="text"
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
                defaultChecked={watch("watch_keys")?.indexOf("temperature") != -1}
                name="temperature"
                onClick={handleCheckboxClick}
                id="temperature-checkbox"
                type="checkbox"
              />
              <div className="sm:col-span-2 flex">
                <TextInput
                  id="temperature"
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
                defaultChecked={watch("watch_keys")?.indexOf("conectivity") != -1}
                onClick={handleCheckboxClick}
                id="conectivity-checkbox"
                type="checkbox"
              />
              <div className="sm:col-span-2 flex">
                <TextInput
                  id="conectivity"
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
                name="latency"
                id="latencia-checkbox"
                defaultChecked={watch("watch_keys")?.indexOf("latency") != -1}
                onClick={handleCheckboxClick}
                type="checkbox"
              />
              <div className="sm:col-span-2 flex">
                <TextInput
                  id="latency"
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
          >
            Criar
          </button>
        </div>

      </Form>
    </div>
  )
}
