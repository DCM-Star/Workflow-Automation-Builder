import { useState } from "react"
import { BrowserRouter, Routes, Route, Navigate } from "react-router-dom"

import Login from "./pages/Login"
import Signup from "./pages/Signup"
import Dashboard from "./pages/Dashboard"
import WorkflowBuilder from "./pages/WorkflowBuilder"

function App() {

  const [token, setToken] = useState(localStorage.getItem("token"))

  const handleLogin = (newToken) => {
    localStorage.setItem("token", newToken)
    setToken(newToken)
  }

  const handleLogout = () => {
    localStorage.removeItem("token")
    setToken(null)
  }

  return (
    <BrowserRouter>

      <Routes>

        {/* LOGIN */}
        <Route
          path="/login"
          element={
            token
              ? <Navigate to="/" />
              : <Login onLogin={handleLogin} />
          }
        />

        {/* SIGNUP */}
        <Route
          path="/signup"
          element={
            token
              ? <Navigate to="/" />
              : <Signup />
          }
        />

        {/* DASHBOARD */}
        <Route
          path="/"
          element={
            token
              ? <Dashboard token={token} onLogout={handleLogout} />
              : <Navigate to="/login" />
          }
        />

        {/* WORKFLOW BUILDER */}
        <Route
          path="/builder/:id"
          element={
            token
              ? <WorkflowBuilder />
              : <Navigate to="/login" />
          }
        />

      </Routes>

    </BrowserRouter>
  )
}

export default App