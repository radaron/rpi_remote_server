import React, { useState, useEffect, createContext } from 'react'
import { Container, Button, Navbar } from 'react-bootstrap'
import { ReactComponent as RpiIcon } from '../rpi.svg'
import Terminal from './Terminal'
import ItemList from './ItemList'
import useWindowSize from './useWindowSize'
import styles from './Manage.module.scss'

export const DataContext = createContext()

export const Manage = () => {
  const [connectTarget, setConnectTarget] = useState('')
  const [data, setData] = useState({})
  const windowSize = useWindowSize()

  useEffect(() => {
    fetchData()
    const interval = setInterval(() => {
      fetchData()
    }, 5000)
    return () => clearInterval(interval)
  }, [])

  const fetchData = async () => {
    try {
      const reponse = await fetch('/rpi/api/data', {
        method: 'GET',
        headers: {
          'Content-Type': 'application/json',
        }
      })
      const data = await reponse.json()
      setData(data)
    } catch(err) {
      console.log(err)
    }
  }

  const deleteItem = async (name) => {
    try {
      await fetch('/rpi/api/data', {
        method: 'DELETE',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ name })
      })
      fetchData()
    } catch (error) {
      console.log(error)
    }
  }

  const isDetailedView = windowSize.width >= 770;
  const isPhoneLandscapeView = windowSize.height <= 400;
  const logOut = async () => {
    const response = await fetch('/rpi/logout', {
      method: 'POST',
    })
    if (response.redirected) {
      window.location.href = response.url;
      return;
   }
  }
  return (
    <DataContext.Provider value={
        {connectTarget, setConnectTarget, isDetailedView, deleteItem, isPhoneLandscapeView}
    }>
      <Navbar expand='lg' bg='dark' data-bs-theme='dark' className='bg-body-tertiary'>
        <Container fluid>
          <Navbar.Brand><RpiIcon />Rpi remote server</Navbar.Brand>
          <Button variant='danger' onClick={logOut}>Logout</Button>
        </Container>
      </Navbar>
      <Container className={styles.mainContainer}>
        <Container className={styles.dataContainer}>
          <ItemList data={data} />
        </Container>
      </Container>
      {connectTarget && <Terminal/>}
    </DataContext.Provider>
  )
}
