from orm import BaseModel, IntegerField, TextField


class Task(BaseModel):
    table_name = "task"

    task_id = IntegerField()
    title = TextField()
    summary = TextField()
    label = TextField()
    state = TextField()

    def __repr__(self) -> str:
        return f"Task(id={self.task_id},title={self.title}, summary={self.summary},label={self.label}), state={self.state})"

    def __str__(self) -> str:
        return f"Task(id={self.task_id},title={self.title}, summary={self.summary},label={self.label}), state={self.state})"
