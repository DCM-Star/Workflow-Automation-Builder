from app.extensions import db

class WorkflowStep(db.Model):
    __tablename__ = "workflow_steps"

    id = db.Column(db.Integer, primary_key=True)

    workflow_id = db.Column(
        db.Integer,
        db.ForeignKey("workflows.id", ondelete="CASCADE"),
        nullable=False
    )

    step_type = db.Column(
        db.String(50),
        nullable=False
    )

    position = db.Column(
        db.Integer,
        nullable=False
    )

    config = db.Column(
        db.JSON,
        nullable=True
    )

    created_at = db.Column(
        db.DateTime,
        server_default=db.func.now()
    )