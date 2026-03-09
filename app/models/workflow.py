from app.extensions import db


class Workflow(db.Model):
    __tablename__ = "workflows"

    id = db.Column(db.Integer, primary_key=True)

    name = db.Column(
        db.String(255),
        nullable=False
    )

    description = db.Column(
        db.Text,
        nullable=True
    )

    user_id = db.Column(
        db.Integer,
        db.ForeignKey("users.id"),
        nullable=False
    )

    created_at = db.Column(
        db.DateTime,
        server_default=db.func.now()
    )

    # NEW: store React Flow graph
    nodes = db.Column(
        db.JSON,
        nullable=True
    )

    edges = db.Column(
        db.JSON,
        nullable=True
    )

    steps = db.relationship(
        "WorkflowStep",
        backref="workflow",
        cascade="all, delete-orphan",
        order_by="WorkflowStep.position"
    )