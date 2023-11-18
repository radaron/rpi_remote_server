import { useState } from 'react'

const useToken = () => {
  const getToken = () => {
    const userToken = localStorage.getItem('token') // eslint-disable-line
    return userToken && userToken
  }

  const [token, setToken] = useState(getToken())

  const saveToken = (userToken) => {
    localStorage.setItem('token', userToken) // eslint-disable-line
    setToken(userToken)
  }

  const removeToken = () => {
    localStorage.removeItem('token') // eslint-disable-line
    setToken(null)
  }

  return {
    setToken: saveToken,
    token,
    removeToken
  }
}

export default useToken
