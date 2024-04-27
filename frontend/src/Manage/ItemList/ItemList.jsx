
import { Row, Col } from 'react-bootstrap'
import  Item  from '../Item'
import { useContext } from 'react'
import { DataContext } from '../Manage'
import styles from './ItemList.module.scss'


export const ItemList = ({ data }) => {
  const { isDetailedView } = useContext(DataContext)
  return (
    <>
      <Row className={styles.header} >
        <Col className={styles.name_column}>Name</Col>
        {isDetailedView && <>
          <Col>{'Uptime (hour)'}</Col>
          <Col>{'CPU (%)'}</Col>
          <Col>{'Mem (%)'}</Col>
          <Col>{'Disk (%)'}</Col>
          <Col>{'Temp (°C)'}</Col>
        </>}
        <Col>Connect</Col>
        {isDetailedView && <>
          <Col>Status</Col>
          <Col/>
        </>
         }
      </Row>
      {data.data && data.data
        .map((val, index) => (
          <Item
            key = {index}
            index={index}
            name={val.name}
            polledTime={val.polled_time}
            currentTime={data.current_time}
            uptime={val.uptime}
            cpuUsage={val.cpu_usage}
            memoryUsage={val.memory_usage}
            diskUsage={val.disk_usage}
            temperature={val.temperature}
          />
        ))}
    </>
  )
}
