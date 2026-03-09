from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity

from app.extensions import db
from app.models import Workflow, WorkflowStep

workflow_steps_bp = Blueprint(
    "workflow_steps",
    __name__,
    url_prefix="/workflows/<int:workflow_id>/steps"
)

# --------------------
# CREATE step
# --------------------
@workflow_steps_bp.route("/", methods=["POST"])
@jwt_required()
def create_workflow_step(workflow_id):
    user_id = int(get_jwt_identity())

    workflow = Workflow.query.filter_by(
        id=workflow_id,
        user_id=user_id
    ).first()

    if not workflow:
        return jsonify({"error": "Workflow not found"}), 404

    data = request.get_json() or {}
    step_type = data.get("step_type")
    config = data.get("config", {})

    if not step_type:
        return jsonify({"error": "step_type is required"}), 400

    next_position = len(workflow.steps) + 1

    step = WorkflowStep(
        workflow_id=workflow.id,
        step_type=step_type,
        position=next_position,
        config=config
    )

    db.session.add(step)
    db.session.commit()

    return jsonify({
        "id": step.id,
        "workflow_id": step.workflow_id,
        "step_type": step.step_type,
        "position": step.position,
        "config": step.config,
        "created_at": step.created_at.isoformat()
    }), 201


# --------------------
# GET steps
# --------------------
@workflow_steps_bp.route("/", methods=["GET"])
@jwt_required()
def get_workflow_steps(workflow_id):
    user_id = int(get_jwt_identity())

    workflow = Workflow.query.filter_by(
        id=workflow_id,
        user_id=user_id
    ).first()

    if not workflow:
        return jsonify({"error": "Workflow not found"}), 404

    return jsonify([
        {
            "id": step.id,
            "workflow_id": step.workflow_id,
            "step_type": step.step_type,
            "position": step.position,
            "config": step.config,
            "created_at": step.created_at.isoformat()
        }
        for step in workflow.steps
    ]), 200


# --------------------
# REORDER steps
# --------------------
@workflow_steps_bp.route("/reorder", methods=["PUT"])
@jwt_required()
def reorder_workflow_steps(workflow_id):
    user_id = int(get_jwt_identity())

    workflow = Workflow.query.filter_by(
        id=workflow_id,
        user_id=user_id
    ).first()

    if not workflow:
        return jsonify({"error": "Workflow not found"}), 404

    data = request.get_json() or {}
    order = data.get("order")

    if not order or not isinstance(order, list):
        return jsonify({"error": "order must be a list of step IDs"}), 400

    steps = WorkflowStep.query.filter_by(
        workflow_id=workflow.id
    ).all()

    step_map = {step.id: step for step in steps}

    if set(order) != set(step_map.keys()):
        return jsonify({
            "error": "Order list must include all workflow step IDs"
        }), 400

    for index, step_id in enumerate(order, start=1):
        step_map[step_id].position = index

    db.session.commit()

    return jsonify({
        "message": "Workflow steps reordered successfully"
    }), 200


# --------------------
# UPDATE step
# --------------------
@workflow_steps_bp.route("/<int:step_id>", methods=["PATCH"])
@jwt_required()
def update_workflow_step(workflow_id, step_id):
    user_id = int(get_jwt_identity())

    workflow = Workflow.query.filter_by(
        id=workflow_id,
        user_id=user_id
    ).first()

    if not workflow:
        return jsonify({"error": "Workflow not found"}), 404

    step = WorkflowStep.query.filter_by(
        id=step_id,
        workflow_id=workflow.id
    ).first()

    if not step:
        return jsonify({"error": "Step not found"}), 404

    data = request.get_json() or {}

    if "step_type" in data:
        step.step_type = data["step_type"]

    if "config" in data:
        step.config = data["config"]

    db.session.commit()

    return jsonify({
        "id": step.id,
        "workflow_id": step.workflow_id,
        "step_type": step.step_type,
        "position": step.position,
        "config": step.config,
        "created_at": step.created_at.isoformat()
    }), 200


# --------------------
# DELETE step
# --------------------
@workflow_steps_bp.route("/<int:step_id>", methods=["DELETE"])
@jwt_required()
def delete_workflow_step(workflow_id, step_id):
    user_id = int(get_jwt_identity())

    workflow = Workflow.query.filter_by(
        id=workflow_id,
        user_id=user_id
    ).first()

    if not workflow:
        return jsonify({"error": "Workflow not found"}), 404

    step = WorkflowStep.query.filter_by(
        id=step_id,
        workflow_id=workflow.id
    ).first()

    if not step:
        return jsonify({"error": "Step not found"}), 404

    deleted_position = step.position

    db.session.delete(step)

    WorkflowStep.query.filter(
        WorkflowStep.workflow_id == workflow.id,
        WorkflowStep.position > deleted_position
    ).update(
        {WorkflowStep.position: WorkflowStep.position - 1}
    )

    db.session.commit()

    return jsonify({"message": "Step deleted"}), 200