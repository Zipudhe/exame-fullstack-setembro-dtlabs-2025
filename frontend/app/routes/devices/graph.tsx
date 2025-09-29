import type { Route } from './+types/graph'
import { useEffect, useMemo, useState } from 'react'
import { useNavigate } from 'react-router'
import { LineChart, Line, XAxis, YAxis, ResponsiveContainer, Tooltip, Legend } from 'recharts'

import { CheckBox, DateInput } from '../../components/Input'
import { getDeviceStatus } from '../../lib/api'

export async function clientLoader({ params: { deviceId }, request }: Route.LoaderArgs) {
  const url = new URL(request.url)
  const start_date = url.searchParams.get("start_date")
  const end_date = url.searchParams.get("end_date")

  const device_status = await getDeviceStatus(deviceId, { start_date, end_date }).then(res => res.data).catch(err => console.error({ err }))

  return { device_status }
}

type FilterState = {
  start_date: Date | null,
  end_date: Date | null
}

type Metrics = {
  cpu_usage: string,
  ram_usage: string,
  temperature: string,
  free_disk: string,
  latency: string
}

type MetricKey = keyof Metrics

export default function DevicesHome({ loaderData: { device_status }, params: { deviceId } }: Route.ComponentProps) {
  const [filters, setFilter] = useState<FilterState>({
    start_date: null,
    end_date: null
  })
  const metricColors = {
    cpu_usage: '#3B82F6',
    ram_usage: '#8B5CF6',
    temperature: '#EF4444',
    free_disk: '#22C55E',
    latency: '#EAB308'
  } as Metrics

  const navigate = useNavigate()

  const [visibleKeys, setVisibleKeys] = useState<MetricKey[]>(Object.keys(metricColors) as MetricKey[])
  const keys = ['cpu_usage', 'ram_usage', 'temperature', 'free_disk', 'latency']

  const handleKeyClick = (e: React.MouseEvent<HTMLInputElement>) => {
    const { checked, name } = e.currentTarget

    if (checked) {
      setVisibleKeys((prevState) => {
        const updatedState = [...prevState]
        updatedState.push(name as MetricKey)

        return updatedState
      })
    } else {
      setVisibleKeys((prevState) => {
        const index = prevState.indexOf(name as MetricKey)
        const updatedState = [...prevState]
        updatedState.splice(index, 1)

        return updatedState
      })
    }
  }

  useEffect(() => {
    const queryParams = new URLSearchParams()
    if (filters.start_date) {
      queryParams.append('start_date', filters.start_date.toISOString() ?? '')
    }
    if (filters.end_date) {
      queryParams.append('end_date', filters.end_date.toISOString() ?? '')
    }

    navigate(`/devices/${deviceId}/graph?${queryParams.toString()}`)

  }, [filters])

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
                  defaultChecked={visibleKeys.includes(key as MetricKey)}
                  onClick={handleKeyClick}
                />
                <span> {key} </span>
              </>
            )
          })
        }
      </div>
      <div className='w-full flex flex-row justify-evenly items-center'>
        <DateInput
          label="Data de Inicio"
          value={filters.start_date?.toISOString().split("T")[0]}
          required
          name="start_date"
          onChange={handleUpdateFilter}
        />
        <DateInput
          name="end_date"
          onChange={handleUpdateFilter}
          value={filters.end_date?.toISOString().split("T")[0]}
          label="Data de Fim"
        />
        <button
          className='border-white border rounded-2xl h-12 cursor-pointer w-fit px-3 text-center'
          type="button"
          onClick={() => setFilter({ start_date: null, end_date: null })}
        >
          Limpar Filtros
        </button>
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
