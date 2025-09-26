import { Suspense } from 'react'
import { Await } from 'react-router'
import type { DeviceStatusSummary } from 'types/device'
import { StatusCard, StatusCardSkeleton } from './statusCard'

interface IStatusFeed {
  status: Promise<DeviceStatusSummary[]>
}

export default function StatusFeed({ status }: IStatusFeed) {

  return (
    <article
      className="hidden lg:w-[30%] lg:flex flex-col gap-y-6 p-4 overflow-y-scroll h-max"
    >
      <Suspense fallback={<StatusCardSkeleton />}>
        <Await resolve={status}>
          {
            (status) => status && status.map((stat) => <StatusCard {...stat} />)
          }
        </Await>
      </Suspense>
    </article>
  )
}
