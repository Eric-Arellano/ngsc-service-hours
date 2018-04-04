// @flow
import * as React from 'react'
import { Route, Switch } from 'react-router-dom'
import { Footer, Header, PrivateRoute } from 'components'
import { AdminView, ContactUsView, EventsViewContainer, InternshipView, ParticipationView } from 'views'
import type { Student } from 'types'
import s from './AppView.module.css'

type Props = {
  isLoggedIn: boolean,
  student: ?Student,
  resetState: () => void,
  login: (Student) => void
}

const AppView = ({isLoggedIn, student, login, resetState}: Props) => (
  <div className={s.outerContainer}>
    <Header />
    <div className={s.mainContent}>
      <Switch>
        <PrivateRoute exact path='/' isLoggedIn={isLoggedIn} component={ParticipationView} student={student}
                      resetState={resetState} login={login} />
        <Route exact path='/admin' component={AdminView} />
        <Route exact path='/events' component={EventsViewContainer} />
        <Route exact path='/internships' component={InternshipView} />
        <Route exact path='/leadership' component={ContactUsView} />
      </Switch>
    </div>
    <Footer />
  </div>
)

export default AppView