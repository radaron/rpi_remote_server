import './App.scss';
import { BrowserRouter, Routes, Route } from "react-router-dom";
import Login from './Login/Login';
import Manage from './Manage/Manage';
import useToken from './useToken'


function App() {
  const { token, setToken, removeToken } = useToken();

  return (
    <BrowserRouter>
      <Routes>
        <Route path="rpi/login" element={<Login setToken={setToken} /> } />
        <Route path="rpi/manage" element={<Manage setToken={setToken} 
                                                  token={token} 
                                                  removeToken={removeToken}
                                          />} 
        />
      </Routes>
    </BrowserRouter>
  );
}

export default App;
