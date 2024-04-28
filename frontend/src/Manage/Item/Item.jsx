import { ReactComponent as XIcon } from './xicon.svg'
import { ReactComponent as ConnectIcon } from './connect.svg'
import { Button } from 'react-bootstrap'
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
    if (name === connectTarget) {
      return 'statusBlue'
    }
    return statusMap[currentTime - polledTime < 60]
  }
  return (
    <tr className={styles.element}>
      <td className={styles.name_column}>{name}</td>
      {isDetailedView && <>
        <td>{uptime}</td>
        <td>{cpuUsage}</td>
        <td>{memoryUsage}</td>
        <td>{diskUsage}</td>
        <td>{temperature}</td>
      </>}
      <td>
        <Button
            variant='outline-success'
            disabled={!!connectTarget}
            onClick={startForward(name)}
          >
          <ConnectIcon/>
        </Button>
      </td>
        <td>
          <div className={styles[`status--${getStatusCss(currentTime, polledTime)}`]} />
        </td>
      {isDetailedView && <>
        <td>
          <Button
            variant='outline-danger'
            disabled={!!connectTarget}
            onClick={() => {deleteItem(name)}}
          >
            <XIcon />
          </Button>
        </td>
      </>}
    </tr>
  )
}
