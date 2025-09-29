import type { Route } from './+types/graph'
import { useState } from 'react'
import { LineChart, Line, XAxis, YAxis, ResponsiveContainer, Tooltip, Legend } from 'recharts'

import { CheckBox, DateInput } from '../../components/Input'
import { getDeviceStatus } from '../../lib/api'

export async function clientLoader({ params: { deviceId } }: Route.LoaderArgs) {
  const device_status = await getDeviceStatus(deviceId).then(res => res.data).catch(err => console.error({ err }))

  return { device_status }
}

export default function DevicesHome({ loaderData: { device_status } }: Route.ComponentProps) {
  const keys = ['cpu_usage', 'ram_usage', 'temperature', 'free_disk', 'latency']
  const [filters, setFilter] = useState({
    start_date: new Date(),
    end_date: null
  })
  const [visibleKeys, setVisibleKeys] = useState<string[]>(keys)
  const metricColors = {
    cpu_usage: '#3B82F6',
    ram_usage: '#8B5CF6',
    temperature: '#EF4444',
    free_disk: '#22C55E',
    latency: '#EAB308'
  } as Record<typeof keys, string>

  const handleKeyClick = (e: React.MouseEvent<HTMLInputElement>) => {
    const { checked, name } = e.currentTarget

    if (checked) {
      setVisibleKeys((prevState) => {
        const updatedState = [...prevState]
        updatedState.push(name)

        return updatedState
      })
    } else {
      setVisibleKeys((prevState) => {
        const index = prevState.indexOf(name)
        const updatedState = [...prevState]
        updatedState.splice(index, 1)

        return updatedState
      })
    }
  }

  const handleUpdateFilter = (e: React.ChangeEvent<HTMLInputElement>) => {

    const { value, name } = e.currentTarget
    const updateDate = new Date(`${value}T10:00`)
    setFilter((prevFilter) => {
      const updatedFilter = { ...prevFilter, [name]: updateDate }

      return updatedFilter
    })

  }

  return (
    <div className='w-full flex-col max-h-7xl' >
      <div className='w-full flex-row gap-3 flex m-8 justify-center'>
        {
          keys.map((key, index) => {
            return (
              <>
                <CheckBox
                  id={`filter_key-${index}`}
                  name={key}
                  defaultChecked={visibleKeys.includes(key)}
                  onClick={handleKeyClick}
                />
                <span> {key} </span>
              </>
            )
          })
        }
      </div>
      <div className='w-full flex flex-row justify-evenly'>
        <DateInput
          label="Data de Inicio"
          value={filters.start_date.toISOString().split("T")[0]}
          required
          name="start_date"
          onChange={handleUpdateFilter}
        />
        <DateInput
          name="end_date"
          onChange={handleUpdateFilter}
          value={filters.end_date && filters.end_date.toISOString().split("T")[0]}
          label="Data de Fim"
        />
      </div>
      <ResponsiveContainer width={'100%'} height={'80%'} >
        <LineChart
          data={device_status}
          title='Histórico de status'
        >
          <XAxis dataKey={'created_at'} />
          <YAxis />
          <Tooltip />
          <Legend />
          {
            visibleKeys.map(key => {
              return (
                <Line
                  stroke={metricColors[key]}
                  type="monotone"
                  dataKey={key} />
              )
            })
          }
        </LineChart>
      </ResponsiveContainer>
    </div>
  )
}
