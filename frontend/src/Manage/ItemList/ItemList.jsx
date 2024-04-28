
import  Item  from '../Item'
import { useContext } from 'react'
import { DataContext } from '../Manage'
import styles from './ItemList.module.scss'


export const ItemList = ({ data }) => {
  const { isDetailedView } = useContext(DataContext)
  return (
    <table className={styles.table}>
      <thead className={styles.header}>
        <tr>
          <th>Name</th>
          {isDetailedView && <>
            <th>{'Uptime (hour)'}</th>
            <th>{'CPU (%)'}</th>
            <th>{'Mem (%)'}</th>
            <th>{'Disk (%)'}</th>
            <th>{'Temp (°C)'}</th>
          </>}
          <th>Connect</th>
          <th>Status</th>
          {isDetailedView && <>
            <th>Remove</th>
          </>
          }
        </tr>
      </thead>
      <tbody>
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
      </tbody>
    </table>
  )
}
