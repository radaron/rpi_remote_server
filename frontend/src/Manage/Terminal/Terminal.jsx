import React, { useEffect, useState, useContext } from 'react'
import { io } from 'socket.io-client'
import CloseButton from 'react-bootstrap/CloseButton';
import { DataContext } from '../Manage'
import styles from './Terminal.module.scss'

export const Terminal = () => {
  const { connectTarget, setConnectTarget, deleteItem } = useContext(DataContext)
  const [consoleLines, setConsoleLines] = useState(['', '', '', '', '', ''])
  useEffect(() => {
    const addLine = (line) => {
      setConsoleLines((prevConsoleLines) => [...prevConsoleLines, line].slice(1))
    }
    if (connectTarget) {
      const socket = io('/', { path: '/rpi/socket.io' })
      socket.on("forward_resp", (msg) => {
        addLine(msg.data)
      })
      socket.on('connect', () => {
        socket.emit("start_forward", {"name": connectTarget})
      })
      socket.on("disconnect", () => {
        socket.off('forward_resp')
        socket.disconnect()
      })
      return () => {
        socket.off('forward_resp')
        socket.disconnect()
      }
    }
  }, [connectTarget, setConnectTarget])
  const closeTerminal = () => {
    deleteItem(connectTarget)
    setConnectTarget('')
  }

  const ConsoleTextComponent = consoleLines.map((text, index) => <p className={styles.line} key={index}>{text}</p>)
  return (
    <div className={styles.footer}>
      <div className={styles.text}>
        {ConsoleTextComponent}
      </div>
      <div className={styles.close}>
        <CloseButton
          onClick={() => {closeTerminal()}}
          variant='white'
        />
      </div>
    </div>
  )
}
