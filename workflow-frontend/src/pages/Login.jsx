import { useState } from "react"
import { useNavigate } from "react-router-dom"

function Login({ onLogin }) {

  const navigate = useNavigate()

  const [email, setEmail] = useState("")
  const [password, setPassword] = useState("")
  const [message, setMessage] = useState("")

  const handleLogin = async (e) => {
    e.preventDefault()

    try {

      const res = await fetch("http://127.0.0.1:5000/auth/login", {
        method: "POST",
        headers: {
          "Content-Type": "application/json"
        },
        body: JSON.stringify({
          email,
          password
        })
      })

      const data = await res.json()

      if (data.access_token) {

        onLogin(data.access_token)

      } else {

        setMessage(data.error || "Login failed")

      }

    } catch (error) {

      console.error(error)
      setMessage("Server error")

    }

  }

  return (
    <div style={{ padding: 40 }}>

      <h1>Login</h1>

      <form onSubmit={handleLogin}>

        <input
          placeholder="Email"
          value={email}
          onChange={(e)=>setEmail(e.target.value)}
        />

        <br/><br/>

        <input
          placeholder="Password"
          type="password"
          value={password}
          onChange={(e)=>setPassword(e.target.value)}
        />

        <br/><br/>

        <button type="submit">
          Login
        </button>

      </form>

      <p>{message}</p>

      <br/>

      <p>
        Don't have an account?
      </p>

      <button
        onClick={()=>navigate("/signup")}
      >
        Create Account
      </button>

    </div>
  )
}

export default Login