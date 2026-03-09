import { useState, useEffect } from "react"
import { useNavigate } from "react-router-dom"

function Dashboard({ token, onLogout }) {

  const navigate = useNavigate()

  const [workflows, setWorkflows] = useState([])
  const [workflowName, setWorkflowName] = useState("")

  useEffect(() => {

    const loadWorkflows = async () => {

      try {

        const res = await fetch("http://127.0.0.1:5000/workflows/", {
          headers: {
            Authorization: `Bearer ${token}`
          }
        })

        if (!res.ok) {
          console.error("Failed to load workflows")
          setWorkflows([])
          return
        }

        const data = await res.json()

        if (Array.isArray(data)) {
          setWorkflows(data)
        } else {
          setWorkflows([])
        }

      } catch (error) {
        console.error(error)
      }

    }

    loadWorkflows()

  }, [token])

  const createWorkflow = async () => {

    try {

      const res = await fetch("http://127.0.0.1:5000/workflows/", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
          Authorization: `Bearer ${token}`
        },
        body: JSON.stringify({
          name: workflowName
        })
      })

      const data = await res.json()

      setWorkflows([...workflows, data])
      setWorkflowName("")

    } catch (error) {
      console.error(error)
    }

  }

  const deleteWorkflow = async (id) => {

    try {

      const res = await fetch(`http://127.0.0.1:5000/workflows/${id}`, {
        method: "DELETE",
        headers: {
          Authorization: `Bearer ${token}`
        }
      })

      if (!res.ok) {
        throw new Error("Delete failed")
      }

      setWorkflows(workflows.filter((wf) => wf.id !== id))

    } catch (error) {
      console.error(error)
    }

  }

  return (
    <div style={{ padding: 40 }}>
      <h1>Dashboard</h1>

      <button onClick={onLogout}>
        Logout
      </button>

      <h2>Create Workflow</h2>

      <input
        type="text"
        placeholder="Workflow name"
        value={workflowName}
        onChange={(e) => setWorkflowName(e.target.value)}
      />

      <button onClick={createWorkflow}>
        Create
      </button>

      <h2>Your Workflows</h2>

      <ul>
        {workflows.map((wf) => (
          <li key={wf.id}>

            {wf.name}

            <button
              onClick={() => deleteWorkflow(wf.id)}
              style={{ marginLeft: 10 }}
            >
              Delete
            </button>

            <button
              onClick={() => navigate(`/builder/${wf.id}`)}
              style={{ marginLeft: 10 }}
            >
              Open Workflow Builder
            </button>

          </li>
        ))}
      </ul>

    </div>
  )
}

export default Dashboard