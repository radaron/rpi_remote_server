import './App.scss'
import { BrowserRouter, Routes, Route } from 'react-router-dom'
import Login from './Login'
import Manage from './Manage'

function App () {
  return (
    <BrowserRouter>
      <Routes>
        <Route path='/login' element={<Login />}/>
        <Route path='/manage' element={<Manage />}/>
      </Routes>
    </BrowserRouter>
  )
}

export default App
