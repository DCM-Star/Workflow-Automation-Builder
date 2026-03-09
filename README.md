# Workflow Automation Builder

A full-stack workflow automation platform that allows users to visually create and execute automated workflows using a drag-and-drop node-based interface.

The application enables users to design automation pipelines by connecting nodes that represent different workflow steps. Workflows can be saved, loaded, and executed through a backend execution engine.

This project demonstrates full-stack architecture, API development, authentication systems, and graph-based workflow design.

---

## Features

- User authentication (JWT)
- Create and manage workflows
- Drag-and-drop visual workflow builder
- Connect nodes to define execution flow
- Save workflow graphs to database
- Load existing workflows
- Execute workflows from the backend
- Node deletion via keyboard interaction
- Protected API routes

---

## Tech Stack

### Frontend
- React
- React Router
- React Flow (visual graph builder)
- Vite

### Backend
- Python
- Flask
- Flask-JWT-Extended
- REST API architecture

### Database
- SQLite (development)
- PostgreSQL ready (production)

---

## Architecture Overview
- Frontend (React + ReactFlow)

- Backend API (Flask)

- Workflow Storage

- Database 

The frontend provides a visual interface for building workflows, while the backend stores workflow graphs and executes them through a workflow engine.

---

## How Workflows Work

Workflows are represented as directed graphs consisting of:

- **Nodes** – individual workflow steps
- **Edges** – connections defining execution order

Example workflow structure:

Node A -> Node B -> Node C 

The backend execution engine traverses the graph and executes nodes sequentially.

---

## Running the Project Locally

### Backend

Install dependencies:

pip install -r requirements.txt

Run the Flask server:

python main.py

---

### Frontend

Install dependencies:

npm install

Start development server:

npm run dev

---

## Future Improvements

- Node configuration panels
- Workflow execution logs
- Custom node types
- Real-time workflow monitoring
- Docker containerization
- Cloud deployment

---

## Learning Goals

This project was built to explore:

- Full-stack application architecture
- Graph-based workflow systems
- API design and authentication
- React state management
- Visual node editors

---

## Author

Danny Miguel


