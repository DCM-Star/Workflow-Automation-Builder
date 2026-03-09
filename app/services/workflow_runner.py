from app.models import Workflow


class WorkflowRunner:
    def __init__(self, workflow: Workflow):
        self.workflow = workflow
        self.results = []

    def run(self):
        for step in self.workflow.steps:
            result = self.execute_step(step)
            self.results.append(result)

        return {
            "workflow_id": self.workflow.id,
            "status": "completed",
            "steps": self.results
        }

    def execute_step(self, step):
        if step.step_type == "send_email":
            return self.run_send_email(step)

        return {
            "step_id": step.id,
            "type": step.step_type,
            "status": "skipped",
            "output": "Unknown step type"
        }

    def run_send_email(self, step):
        config = step.config or {}

        to = config.get("to")
        subject = config.get("subject")

        # 🔥 Simulated execution
        return {
            "step_id": step.id,
            "type": step.step_type,
            "status": "success",
            "output": f"Email sent to {to} with subject '{subject}'"
        }