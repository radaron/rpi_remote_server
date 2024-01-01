import React, { useState, useEffect } from 'react'
import { Container, Button, Navbar, Row, Col } from 'react-bootstrap'
import styles from './Manage.module.scss'
import { ReactComponent as ReactLogo } from '../xicon.svg'
import { ReactComponent as RpiIcon } from '../rpi.svg'

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

const ItemList = ({ data, onDataChanged }) => {
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
  const getItem = (
      name, 
      polledTime, 
      currentTime,
      uptime,
      cpuUsage,
      memoryUsage,
      diskUsage,
      temperature
    ) => {
    const getStatusCss = (currentTime, polledTime) => {
      const statusMap = {
        true: 'statusGreen',
        false: 'statusRed'
      }
      return statusMap[currentTime - polledTime < 60]
    }

    return (
      <Row className={styles.element} key={name}>
        <Col md={2}>{name}</Col>
        <Col md={2}>{uptime}</Col>
        <Col md={1}>{cpuUsage}</Col>
        <Col md={2}>{memoryUsage}</Col>
        <Col md={1}>{diskUsage}</Col>
        <Col md={2}>{temperature}</Col>
        <Col md={1}>
          <div className={styles[`status--${getStatusCss(currentTime, polledTime)}`]} />
        </Col>
        <Col className={styles.xbutton} md={1}>
          <Button
            variant='outline-danger'
            onClick={deleteItem(name)}
          >
            <ReactLogo />
          </Button>
        </Col>
      </Row>
    )
  }
  return (
    <div>
      <Row className={styles.header}>
        <Col md={2}>Name</Col>
        <Col md={2}>{'Uptime (hour)'}</Col>
        <Col md={1}>{'CPU (%)'}</Col>
        <Col md={2}>{'Memory (%)'}</Col>
        <Col md={1}>{'Disk (%)'}</Col>
        <Col md={2}>{'Temperature (°C)'}</Col>
        <Col md={1}>Status</Col>
        <Col md={1}/>
      </Row>
      {data.data && data.data
        .map(val => getItem(
          val.name, 
          val.polled_time, 
          data.current_time, 
          val.uptime, 
          val.cpu_usage, 
          val.memory_usage, 
          val.disk_usage, 
          val.temperature
        ))}
    </div>
  )
}

const Manage = () => {
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
          />
        </Container>
      </Container>
    </>
  )
}

export default Manage
