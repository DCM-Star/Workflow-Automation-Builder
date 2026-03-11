import { useState } from "react"
import { useNavigate } from "react-router-dom"
const API_URL = import.meta.env.VITE_API_URL

function Signup() {

  const navigate = useNavigate()

  const [email, setEmail] = useState("")
  const [password, setPassword] = useState("")
  const [confirmPassword, setConfirmPassword] = useState("")
  const [message, setMessage] = useState("")

  const handleSignup = async (e) => {

    e.preventDefault()

    if (password !== confirmPassword) {
      setMessage("Passwords do not match")
      return
    }

    try {


const res = await fetch(`${API_URL}/auth/register`, {
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

      if (res.status === 201) {

        alert("Account created! Please login.")
        navigate("/")

      } else {

        setMessage(data.error || "Signup failed")

      }

    } catch (err) {

      console.error(err)
      setMessage("Server error")

    }

  }

  return (
    <div style={{ padding: 40 }}>

      <h1>Create Account</h1>

      <form onSubmit={handleSignup}>

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

        <input
          placeholder="Confirm Password"
          type="password"
          value={confirmPassword}
          onChange={(e)=>setConfirmPassword(e.target.value)}
        />

        <br/><br/>

        <button type="submit">
          Create Account
        </button>

      </form>

      <p>{message}</p>

      <br/>

      <button onClick={()=>navigate("/")}>
        Back to Login
      </button>

    </div>
  )
}

export default Signup