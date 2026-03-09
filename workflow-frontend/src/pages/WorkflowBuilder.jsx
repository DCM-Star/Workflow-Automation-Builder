import React, { useCallback, useEffect, useState } from "react"
import { useParams, useNavigate } from "react-router-dom"

import ReactFlow, {
  Background,
  Controls,
  addEdge,
  useNodesState,
  useEdgesState
} from "reactflow"

import "reactflow/dist/style.css"
import NodeSidebar from "../components/NodeSidebar"

const getId = () => `node_${Date.now()}`

export default function WorkflowBuilder() {

  const { id } = useParams()
  const navigate = useNavigate()

  const [nodes, setNodes, onNodesChange] = useNodesState([])
  const [edges, setEdges, onEdgesChange] = useEdgesState([])
  const [selectedNode, setSelectedNode] = useState(null)

  // -------------------------
  // LOAD WORKFLOW
  // -------------------------
  const loadWorkflow = async () => {

    const token = localStorage.getItem("token")

    try {

      const res = await fetch(
        `${import.meta.env.VITE_API_URL}/workflows/${id}`,
        {
          headers: {
            Authorization: `Bearer ${token}`
          }
        }
      )

      if (!res.ok) {
        console.error("Failed to load workflow")
        return
      }

      const workflow = await res.json()

      if (workflow.nodes) setNodes(workflow.nodes)
      if (workflow.edges) setEdges(workflow.edges)

    } catch (err) {

      console.error("Load workflow failed", err)

    }

  }

  useEffect(() => {
    loadWorkflow()
  }, [])

  // -------------------------
  // DELETE KEY SUPPORT
  // -------------------------
  useEffect(() => {

    const handleKeyDown = (event) => {

      if (event.key === "Delete" && selectedNode) {

        setNodes((nds) => nds.filter(n => n.id !== selectedNode.id))

        setEdges((eds) =>
          eds.filter(e =>
            e.source !== selectedNode.id &&
            e.target !== selectedNode.id
          )
        )

        setSelectedNode(null)

      }

    }

    window.addEventListener("keydown", handleKeyDown)

    return () => window.removeEventListener("keydown", handleKeyDown)

  }, [selectedNode])

  const onConnect = useCallback(
    (params) => setEdges((eds) => addEdge(params, eds)),
    [setEdges]
  )

  const onNodeClick = (_, node) => {
    setSelectedNode(node)
  }

  const onDragOver = useCallback((event) => {
    event.preventDefault()
    event.dataTransfer.dropEffect = "move"
  }, [])

  const onDrop = useCallback((event) => {

    event.preventDefault()

    const type = event.dataTransfer.getData("application/reactflow")

    const position = {
      x: event.clientX - 250,
      y: event.clientY - 50
    }

    const newNode = {
      id: getId(),
      type: "default",
      position,
      data: { label: type }
    }

    setNodes((nds) => nds.concat(newNode))

  }, [setNodes])

  // -------------------------
  // SAVE WORKFLOW
  // -------------------------
  const saveWorkflow = async () => {

    const token = localStorage.getItem("token")

    try {

      const res = await fetch(
        `${import.meta.env.VITE_API_URL}/workflows/${id}/graph`,
        {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
            Authorization: `Bearer ${token}`
          },
          body: JSON.stringify({
            nodes,
            edges
          })
        }
      )

      if (!res.ok) {
        throw new Error("Server error")
      }

      await res.json()

      alert("Workflow saved successfully!")

    } catch (err) {

      console.error("Save failed", err)
      alert("Error saving workflow")

    }

  }

  // -------------------------
  // DELETE WORKFLOW
  // -------------------------
  const deleteWorkflow = async () => {

    const token = localStorage.getItem("token")

    if (!confirm("Delete this workflow?")) return

    try {

      const res = await fetch(
        `${import.meta.env.VITE_API_URL}/workflows/${id}`,
        {
          method: "DELETE",
          headers: {
            Authorization: `Bearer ${token}`
          }
        }
      )

      if (!res.ok) {
        throw new Error("Delete failed")
      }

      alert("Workflow deleted")

      navigate("/")

    } catch (err) {

      console.error(err)
      alert("Delete failed")

    }

  }

  return (
    <div style={{ display: "flex", width: "100vw", height: "100vh" }}>

      <NodeSidebar />

      <div style={{ flexGrow: 1 }}>

        {/* TOP BAR */}
        <div style={{
          padding: "10px",
          borderBottom: "1px solid #333",
          background: "#1f2937",
          display: "flex",
          gap: "10px",
          alignItems: "center"
        }}>

          <button
            onClick={() => navigate("/")}
            style={{
              background: "#3b82f6",
              color: "white",
              border: "none",
              padding: "8px 14px",
              borderRadius: "6px",
              cursor: "pointer"
            }}
          >
            Back
          </button>

          <button
            onClick={saveWorkflow}
            style={{
              background: "#22c55e",
              color: "white",
              border: "none",
              padding: "8px 14px",
              borderRadius: "6px",
              cursor: "pointer"
            }}
          >
            Save Workflow
          </button>

          <button
            onClick={deleteWorkflow}
            style={{
              background: "#ef4444",
              color: "white",
              border: "none",
              padding: "8px 14px",
              borderRadius: "6px",
              cursor: "pointer"
            }}
          >
            Delete Workflow
          </button>

          <span style={{ color: "#9ca3af", marginLeft: "20px" }}>
            Tip: Select a node and press DELETE to remove it
          </span>

        </div>

        <ReactFlow
          nodes={nodes}
          edges={edges}
          onNodesChange={onNodesChange}
          onEdgesChange={onEdgesChange}
          onConnect={onConnect}
          onNodeClick={onNodeClick}
          onDrop={onDrop}
          onDragOver={onDragOver}
          fitView
        >
          <Background />
          <Controls />
        </ReactFlow>

      </div>

    </div>
  )
}