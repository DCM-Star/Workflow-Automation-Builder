from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from flask_cors import cross_origin
from app.extensions import db
from app.models import Workflow

from app.services.workflow_runner import WorkflowRunner

workflows_bp = Blueprint("workflows", __name__, url_prefix="/workflows")


# --------------------
# CREATE workflow
# --------------------
@workflows_bp.route("/", methods=["POST"])
@jwt_required()
def create_workflow():
    user_id = int(get_jwt_identity())

    data = request.get_json() or {}

    name = data.get("name")
    description = data.get("description")
    nodes = data.get("nodes", [])
    edges = data.get("edges", [])

    if not name:
        return jsonify({"error": "Workflow name is required"}), 400

    workflow = Workflow(
        name=name,
        description=description,
        user_id=user_id,
        nodes=nodes,
        edges=edges
    )

    db.session.add(workflow)
    db.session.commit()

    return jsonify({
        "id": workflow.id,
        "name": workflow.name,
        "description": workflow.description,
        "nodes": workflow.nodes,
        "edges": workflow.edges,
        "user_id": workflow.user_id,
        "created_at": workflow.created_at.isoformat()
    }), 201


# --------------------
# GET all workflows
# --------------------
@workflows_bp.route("/", methods=["GET"])
@jwt_required()
def get_workflows():
    user_id = int(get_jwt_identity())

    workflows = Workflow.query.filter_by(user_id=user_id).all()

    return jsonify([
        {
            "id": w.id,
            "name": w.name,
            "description": w.description,
            "nodes": w.nodes,
            "edges": w.edges,
            "created_at": w.created_at.isoformat()
        }
        for w in workflows
    ]), 200


# --------------------
# GET single workflow
# --------------------
@workflows_bp.route("/<int:workflow_id>", methods=["GET"])
@jwt_required()
def get_workflow(workflow_id):
    user_id = int(get_jwt_identity())

    workflow = Workflow.query.filter_by(
        id=workflow_id,
        user_id=user_id
    ).first()

    if not workflow:
        return jsonify({"error": "Workflow not found"}), 404

    return jsonify({
        "id": workflow.id,
        "name": workflow.name,
        "description": workflow.description,
        "nodes": workflow.nodes,
        "edges": workflow.edges,
        "created_at": workflow.created_at.isoformat()
    }), 200


# --------------------
# UPDATE workflow
# --------------------
@workflows_bp.route("/<int:workflow_id>", methods=["PUT"])
@jwt_required()
def update_workflow(workflow_id):
    user_id = int(get_jwt_identity())

    workflow = Workflow.query.get_or_404(workflow_id)

    if workflow.user_id != user_id:
        return jsonify({"error": "Forbidden"}), 403

    data = request.get_json() or {}

    if "name" in data:
        workflow.name = data["name"]

    if "description" in data:
        workflow.description = data["description"]

    if "nodes" in data:
        workflow.nodes = data["nodes"]

    if "edges" in data:
        workflow.edges = data["edges"]

    db.session.commit()

    return jsonify({
        "id": workflow.id,
        "name": workflow.name,
        "description": workflow.description,
        "nodes": workflow.nodes,
        "edges": workflow.edges,
        "updated": True
    }), 200


# --------------------
# DELETE workflow
# --------------------
@workflows_bp.route("/<int:workflow_id>", methods=["DELETE"])
@jwt_required()
def delete_workflow(workflow_id):
    user_id = int(get_jwt_identity())

    workflow = Workflow.query.get_or_404(workflow_id)

    if workflow.user_id != user_id:
        return jsonify({"error": "Forbidden"}), 403

    db.session.delete(workflow)
    db.session.commit()

    return jsonify({"message": "Workflow deleted"}), 200


# --------------------
# SAVE workflow graph (nodes + edges)
# --------------------
@workflows_bp.route("/<int:workflow_id>/graph", methods=["POST", "OPTIONS"])
@jwt_required(optional=True)
def save_workflow_graph(workflow_id):

    # Handle browser CORS preflight
    if request.method == "OPTIONS":
        return jsonify({"ok": True}), 200

    user_identity = get_jwt_identity()

    if not user_identity:
        return jsonify({"error": "Unauthorized"}), 401

    user_id = int(user_identity)

    workflow = Workflow.query.filter_by(
        id=workflow_id,
        user_id=user_id
    ).first()

    if not workflow:
        return jsonify({"error": "Workflow not found"}), 404

    data = request.get_json() or {}

    nodes = data.get("nodes", [])
    edges = data.get("edges", [])

    workflow.nodes = nodes
    workflow.edges = edges

    db.session.commit()

    return jsonify({
        "message": "Workflow graph saved",
        "workflow_id": workflow.id,
        "nodes": workflow.nodes,
        "edges": workflow.edges
    }), 200


# --------------------
# RUN workflow
# --------------------
@workflows_bp.route("/<int:workflow_id>/run", methods=["POST"])
@jwt_required()
def run_workflow(workflow_id):
    user_id = int(get_jwt_identity())

    workflow = Workflow.query.filter_by(
        id=workflow_id,
        user_id=user_id
    ).first()

    if not workflow:
        return jsonify({"error": "Workflow not found"}), 404

    runner = WorkflowRunner(workflow)
    result = runner.run()

    return jsonify(result), 200