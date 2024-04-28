import './App.scss'
import { BrowserRouter, Routes, Route } from 'react-router-dom'
import Login from './Login'
import Manage from './Manage'

function App () {
  return (
    <BrowserRouter>
      <Routes>
        <Route path='rpi/login' element={<Login />}/>
        <Route path='rpi/manage' element={<Manage />}/>
      </Routes>
    </BrowserRouter>
  )
}

export default App
