import React, { useState, useEffect } from 'react'
import { Container, Button, Navbar, Row, Col } from 'react-bootstrap'
import styles from './Manage.module.scss'
import { ReactComponent as XIcon } from '../xicon.svg'
import { ReactComponent as ConnectIcon } from '../connect.svg'
import { ReactComponent as RpiIcon } from '../rpi.svg'
import useWindowSize from './useWindowSize'
import { Terminal } from './Terminal'

const fetchData = async (onDataChanged) => {
  try {
    const reponse = await fetch('/rpi/api/data', {
      method: 'GET',
      headers: {
        'Content-Type': 'application/json',
      }
    })
    const data = await reponse.json()
    onDataChanged(data)
  } catch(err) {
    console.log(err)
  }
}

const ItemList = ({ data, onDataChanged, connectTarget, setConnectTarget }) => {
  const windowSize = useWindowSize();
  const isDetailedView = windowSize.width >= 770;
  const deleteItem = (name) => async () => {
    try {
      await fetch('/rpi/api/data', {
        method: 'DELETE',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ name })
      })
      fetchData(onDataChanged)
    } catch (error) {
      console.log(error)
      }
  }
  const startForward = (name) => () => {
    setConnectTarget(name)
  }
  const getItem = (
      index,
      name,
      polledTime,
      currentTime,
      uptime,
      cpuUsage,
      memoryUsage,
      diskUsage,
      temperature,
    ) => {
    const getStatusCss = (currentTime, polledTime) => {
      const statusMap = {
        true: 'statusGreen',
        false: 'statusRed'
      }
      return statusMap[currentTime - polledTime < 60]
    }

    return (
      <Row key={index} className={styles.element} >
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
              onClick={deleteItem(name)}
            >
              <XIcon />
            </Button>
          </Col>
        </>}
      </Row>
    )
  }
  return (
    <div>
      <Row className={styles.header} >
        <Col className={styles.name_column}>Name</Col>
        {isDetailedView && <>
          <Col>{'Uptime (hour)'}</Col>
          <Col>{'CPU (%)'}</Col>
          <Col>{'Mem (%)'}</Col>
          <Col>{'Disk (%)'}</Col>
          <Col>{'Temp (°C)'}</Col>
        </>}
        <Col/>
        {isDetailedView && <>
          <Col>Status</Col>
          <Col/>
        </>
         }
      </Row>
      {data.data && data.data
        .map((val, index) => getItem(
          index,
          val.name,
          val.polled_time,
          data.current_time,
          val.uptime,
          val.cpu_usage,
          val.memory_usage,
          val.disk_usage,
          val.temperature,
        ))}
    </div>
  )
}

const Manage = () => {
  const [connectTarget, setConnectTarget] = useState('')
  const [data, setData] = useState({})

  const logOut = async () => {
    const response = await fetch('/rpi/logout', {
      method: 'POST',
    })
    if (response.redirected) {
      window.location.href = response.url;
      return;
   }
  }
  const onDataChanged = (data) => {
    setData(data)
  }
  useEffect(() => {
    fetchData(onDataChanged)
    const interval = setInterval(() => {
      fetchData(onDataChanged)
    }, 5000)
    return () => clearInterval(interval)
  }, [])
  return (
    <>
      <Navbar expand='lg' bg='dark' data-bs-theme='dark' className='bg-body-tertiary'>
        <Container fluid>
          <Navbar.Brand><RpiIcon />Rpi remote server</Navbar.Brand>
          <Button variant='danger' onClick={logOut}>Logout</Button>
        </Container>
      </Navbar>
      <Container className={styles.mainContainer}>
        <Container className={styles.dataContainer}>
          <ItemList
            data={data}
            onDataChanged={onDataChanged}
            connectTarget={connectTarget}
            setConnectTarget={setConnectTarget}
          />
        </Container>
      </Container>
      {connectTarget && <Terminal connectTarget={connectTarget} setConnectTarget={setConnectTarget}/>}
    </>
  )
}

export default Manage
