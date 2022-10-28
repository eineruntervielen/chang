from orm import BaseModel, IntegerField, TextField


class Task(BaseModel):
    table_name = "task"

    task_id = IntegerField()
    label = TextField()
    summary = TextField()

    def __repr__(self) -> str:
        return f"Task(id={self.task_id}, label={self.label}), summary={self.summary}"

    def __str__(self) -> str:
        return f"Task(id={self.task_id}, label={self.label}), summary={self.summary}"
