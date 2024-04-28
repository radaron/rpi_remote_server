import { ReactComponent as XIcon } from './xicon.svg'
import { ReactComponent as ConnectIcon } from './connect.svg'
import { Button, Row, Col } from 'react-bootstrap'
import { useContext } from 'react'
import { DataContext } from '../Manage'
import styles from './Item.module.scss'

export const Item = ({
  name,
  polledTime,
  currentTime,
  uptime,
  cpuUsage,
  memoryUsage,
  diskUsage,
  temperature,

}) => {
  const { connectTarget, setConnectTarget, isDetailedView, deleteItem } = useContext(DataContext)
  const startForward = (name) => () => {
    setConnectTarget(name)
  }

  const getStatusCss = (currentTime, polledTime) => {
    const statusMap = {
      true: 'statusGreen',
      false: 'statusRed'
    }
    return statusMap[currentTime - polledTime < 60]
  }
  return (
    <Row className={styles.element} >
      <Col className={styles.name_column}>{name}</Col>
      {isDetailedView && <>
        <Col>{uptime}</Col>
        <Col>{cpuUsage}</Col>
        <Col>{memoryUsage}</Col>
        <Col>{diskUsage}</Col>
        <Col>{temperature}</Col>
      </>}
      <Col>
        <Button
            variant='outline-success'
            disabled={!!connectTarget}
            onClick={startForward(name)}
          >
          <ConnectIcon/>
        </Button>
      </Col>
      {isDetailedView && <>
        <Col>
          <div className={styles[`status--${getStatusCss(currentTime, polledTime)}`]} />
        </Col>
        <Col className={styles.xbutton}>
          <Button
            variant='outline-danger'
            disabled={!!connectTarget}
            onClick={() => {deleteItem(name)}}
          >
            <XIcon />
          </Button>
        </Col>
      </>}
    </Row>
  )
}
