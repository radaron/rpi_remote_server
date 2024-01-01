import React, { useState } from 'react'
import { Container, Form, Button, FloatingLabel } from 'react-bootstrap'
import styles from './Login.module.scss'

function Login () {
  const [errorText, setErrorText] = useState(null)
  const [loginForm, setloginForm] = useState({
    username: '',
    password: ''
  })
  const logMeIn = async (event) => {
    event.preventDefault()
    try {
      const response = await fetch('/rpi/session', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(loginForm)
      })
      if (response.status !== 200) {
        throw new Error(response.status)
      }
      if (response.redirected) {
        window.location.href = response.url;
      }
    } catch(error) {
      if (error.message === '401') {
        setErrorText('Invalid username or password')
      } else {
        setErrorText('Something went wrong')
      }
    }

    setloginForm(({
      username: '',
      password: ''
    }))

  }

  const handleChange = (event) => {
    const { value, name } = event.target
    setloginForm(prevNote => ({ ...prevNote, [name]: value })
    )
  }

  return (
    <Container className={styles['main-container']}>
      <Container className={styles['form-container']}>
        <Form>
          <FloatingLabel
            name='username'
            controlId='userName'
            label='Username'
            className='mb-2'
          >
            <Form.Control
              placeholder='Username'
              onChange={handleChange}
              name='username'
            />
          </FloatingLabel>
          <FloatingLabel controlId='password' label='Password'>
            <Form.Control
              type='password'
              placeholder='Password'
              onChange={handleChange}
              name='password'
            />
            {errorText && <p>{errorText}</p>}
          </FloatingLabel>
          <Button
            variant='secondary'
            type='submit'
            className='submit-button'
            onClick={logMeIn}
          >
            Login
          </Button>
        </Form>
      </Container>
    </Container>
  )
}

export default Login
