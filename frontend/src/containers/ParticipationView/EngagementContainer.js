// @flow
import React, { Component } from 'react'
import { AcceptedEngagement, LoggedEngagement } from 'components'
import { withError } from 'decorators'
import { getEngagement } from 'utils/api'
import type { EngagementEvent, Student } from 'flow/types'

type Props = {
  student: Student,
  resetState: () => void
}

type State = {
  isLoading: boolean,
  isError: boolean,
  service: number,
  civilMil: number,
  engagementEvents: Array<EngagementEvent>,
}

class EngagementContainer extends Component<Props, State> {

  state = {
    isLoading: true,
    isError: false,
    service: 0,
    civilMil: 0,
    engagementEvents: []
  }

  componentDidMount () {
    getEngagement(this.props.student.id)
      .then((data) => {
        this.setState({
          service: data.acceptedService,
          civilMil: data.acceptedCivilMil,
          engagementEvents: data.loggedEvents,
          isLoading: false,
        })
      })
      .catch((error) => {
        this.setState({
          service: 0,
          civilMil: 0,
          engagementEvents: [],
          isLoading: false,
          isError: true,
        })
      })
  }

  resetState = () => this.props.resetState() // Quirk with decorators and scope of this. Don't delete.

  @withError('There was an error. Please try again.')
  render () {
    return [
      <AcceptedEngagement {...this.state} key={0} />,
      <LoggedEngagement {...this.state} key={1} />
    ]
  }
}

export default EngagementContainer