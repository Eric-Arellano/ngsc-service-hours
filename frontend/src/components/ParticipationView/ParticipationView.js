// @flow
import React from 'react'
import { Demographics } from 'components'
import { AttendanceContainer, EngagementContainer } from 'containers'
import type { Student } from 'types'

type Props = {
  student: Student,
  resetState: () => void
}

const ParticipationView = ({student, resetState}: Props) => [
  <Demographics student={student} key={0} />,
  <AttendanceContainer student={student} resetState={resetState} key={1} />,
  <EngagementContainer student={student} resetState={resetState} key={2} />
]

export default ParticipationView
