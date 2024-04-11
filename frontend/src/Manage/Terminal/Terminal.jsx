import React, { useEffect, useState } from 'react'
import { io } from 'socket.io-client'
import styles from './Terminal.module.scss'
import CloseButton from 'react-bootstrap/CloseButton';

export const Terminal = ({ connectTarget, setConnectTarget }) => {
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
  const ConsoleTextComponent = consoleLines.map((text, index) => <p className={styles.line} key={index}>{text}</p>)
  return (
    <div className={styles.footer}>
      <div className={styles.text}>
        {ConsoleTextComponent}
      </div>
      <div className={styles.close}>
        <CloseButton
          onClick={() => {setConnectTarget('')}}
          variant='white'
        />
      </div>
    </div>
  )
}