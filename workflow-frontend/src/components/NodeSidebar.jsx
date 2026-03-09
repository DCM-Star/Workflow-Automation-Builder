import React from "react"

function NodeSidebar() {

  const onDragStart = (event, nodeType) => {
    event.dataTransfer.setData("application/reactflow", nodeType)
    event.dataTransfer.effectAllowed = "move"
  }

  return (
    <aside
      style={{
        width: 220,
        padding: 15,
        borderRight: "1px solid #1f2937",
        background: "#111827",
        color: "#ffffff"
      }}
    >
      <h3 style={{ marginBottom: 15 }}>Nodes</h3>

      <div
        onDragStart={(event) => onDragStart(event, "trigger")}
        draggable
        style={{
          padding: 10,
          borderRadius: 6,
          marginBottom: 10,
          cursor: "grab",
          background: "#1f2937",
          border: "1px solid #374151"
        }}
      >
        Trigger
      </div>

      <div
        onDragStart={(event) => onDragStart(event, "email")}
        draggable
        style={{
          padding: 10,
          borderRadius: 6,
          marginBottom: 10,
          cursor: "grab",
          background: "#1f2937",
          border: "1px solid #374151"
        }}
      >
        Send Email
      </div>

      <div
        onDragStart={(event) => onDragStart(event, "delay")}
        draggable
        style={{
          padding: 10,
          borderRadius: 6,
          marginBottom: 10,
          cursor: "grab",
          background: "#1f2937",
          border: "1px solid #374151"
        }}
      >
        Delay
      </div>

    </aside>
  )
}

export default NodeSidebar